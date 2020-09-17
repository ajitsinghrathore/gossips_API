from .serializors import  gossip_accountSerializer,auth_token_serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import  gossips_account
from django.shortcuts import  get_object_or_404
from .permissions import  Account_view_permission,full_profile_view_permission,signup_or_token_generator_view_permission
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.generics import  ListAPIView
from rest_framework.pagination import  PageNumberPagination
from .encrypt_and_decrypt import  My_crypto_handler
from twilio.rest import Client
from .validators import  username_validator
from rest_framework.validators import ValidationError
from gossips_api_project.settings import  (auth_token_for_twilio,account_sid_for_twilio)
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework_simplejwt.views import  TokenObtainPairView
from django.core import signing







class Accounts_view(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly,Account_view_permission,]

    def get(self,request):
        user = get_object_or_404(gossips_account , username =self.request.query_params.get('username',None) )
        if not user.is_active:
            return Response(status = 404)
        return Response( data = gossip_accountSerializer(user , fields  = gossip_accountSerializer.normal_access_level).data ,status = status.HTTP_200_OK)
        
    def put(self,request):
        print(request)
        user =  get_object_or_404(gossips_account , username = self.request.query_params.get("username",None))
        self.check_object_permissions(request,user)
        serialized_user = gossip_accountSerializer(instance = user , data = request.data ,context = {'updating':True}, partial = True)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(status = status.HTTP_200_OK)
        return Response(data = serialized_user.errors , status = 400)        

class signup_view(APIView):
    authentication_classes = []
    permission_classes = [signup_or_token_generator_view_permission,]



    def post(self,request):
        serialized_user = gossip_accountSerializer(data = request.data , context={'updating':True})
        if serialized_user.is_valid():
            serialized_user.save()
            refresh = RefreshToken.for_user(serialized_user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response( data = data ,status  = status.HTTP_201_CREATED)
        return Response(data = serialized_user.errors ,status = 400)

class Verify_phone_number(APIView):

    authentication_classes = []
    permission_classes = []

    def  sign_verify(self,number):
        d = {"phone_number":number , "number_verified":True}
        return  signing.dumps(d)


    def send_otp(self,otp,number):
        try:
            twilio_client = Client(account_sid_for_twilio, auth_token_for_twilio)
            message = twilio_client.messages.create(
                body='OTP for gossips sign in is {}'.format(otp),
                from_='+16605704915',
                to="+" + number
            )
            return True
        except Exception as e:
            print(e)
            return None
    def get(self, request):
        phone_number = request.query_params.get("phone_number",None)
        if not phone_number:
            return Response(status=400)
        token,otp = My_crypto_handler().give_otp(phone_number)
        if not self.send_otp(otp,phone_number):
            return Response(data={"phone_number":"enter a valid phone number of india without +91 prefix"} , status = 400)
        return Response(data={"OTP_TOKEN": token},status=200)
    def  post(self,request):
         otp_given = request.data.get('otp',None)
         signed_token = request.data.get('signed_token' , None)
         if not otp_given  or not signed_token:
             return Response(data="incorrect or missing otp", status = 401)
         otp_JSON = My_crypto_handler().verify_otp(signed_token,otp_given)
         if otp_JSON:
             user = gossips_account.objects.get(phone_number=otp_JSON.get("phone_number",None))
             signed_token = self.sign_verify(otp_JSON.get("phone_number",None))
             if user:
                 return Response(data= {"user":True,"signed_token":signed_token},status=200)
             return  Response(data = {"user":False , "signed_token":signed_token} , status=200)
         return  Response(data="failed", status=401)

class full_profile(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly,full_profile_view_permission,]

    def get(self,request):
        target_user = get_object_or_404(gossips_account , username  = self.request.query_params.get("username",None))
        self.check_object_permissions(request,target_user)
        return Response(data = gossip_accountSerializer(target_user, fields = gossip_accountSerializer.access_with_phone_number_level)  ,status = 200)
#NEED TO DO THIS NEXT-------------------------------------------------------------
class  Filter_gossips_contacts_view(APIView):


     

    def filter_users(self,list_of_numbers):
        filtered_users = gossips_account.objects.filter(phone_number__in=list_of_numbers) 
        print(filtered_users , list_of_numbers)
        return filtered_users


     
    def post(self,request):
        list_of_phone_number_to_check = self.request.data.get("list_of_phone_numbers",None)
        if not list_of_phone_number_to_check :
             return Response(data = "invalid data",status = 400)
        return Response(data = gossip_accountSerializer(self.filter_users(list_of_phone_number_to_check),
                         fields = gossip_accountSerializer.normal_access_level,
                         many=True).data , status = status.HTTP_200_OK)

class search_users(ListAPIView):
    
    serializer_class = gossip_accountSerializer
    pagination_classe = PageNumberPagination
    permission_classes = [IsAuthenticated,]


    def get_queryset(self):
        username = self.request.query_params.get("username",None)
        try:
            username_validator(username)
        except  Exception as e:
            return []
        return gossips_account.objects.filter(username__startswith = username).filter(is_active=True)
     
class MY_auth_token_generator(TokenObtainPairView):
     permission_classes = [signup_or_token_generator_view_permission,]
     serializer_class = auth_token_serializer
