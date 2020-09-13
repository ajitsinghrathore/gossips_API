from .serializors import  gossip_accountSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import  gossips_account




class Accounts_view(APIView):

    def fetch_single_user(self,username):
        try:
            return gossips_account.objects.get(username = username)
        except gossips_account.DoesNotExist:
            return None   
    
    def get(self,request):
        user = self.fetch_single_user(self.request.query_params.get('username',None))
        if not user:
            return Response(data = "user not found " , status = status.HTTP_404_NOT_FOUND)
        return Response( data = gossip_accountSerializer(user).data ,status = status.HTTP_200_OK)

    def post(self,request):
        serialized_user = gossip_accountSerializer(data = request.data)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(data = serialized_user.data , status  = status.HTTP_201_CREATED)
        return Response(data = serialized_user.errors ,status = 400)    

    def put(self,request):
        user_requested = self.request.query_params.get("username",None)
        user = self.fetch_single_user(user_requested)
        if not user:
            return Response(data = "User does not exist" , status = status.HTTP_404_NOT_FOUND)

        serialized_user = gossip_accountSerializer(instance = user , data = request.data , partial = True)
        if serialized_user.is_valid():
            serialized_user.save()
            return Response(data = serialized_user.data , status = status.HTTP_200_OK)
        return Response(data = serialized_user.errors , status = 400)        
        



class  Filter_gossips_contacts_view(APIView):

     

    def filter_users(self,list_of_numbers):
        filtered_users = gossips_account.objects.filter(phone_number__in=list_of_numbers) 
        print(filtered_users , list_of_numbers)
        return filtered_users


     
    def post(self,request):
        list_of_phone_number_to_check = self.request.data.get("list_of_phone_numbers",None)
        if not list_of_phone_number_to_check :
             return Response(data = "invalid data",status = 400)
        return Response(data = gossip_accountSerializer(self.filter_users(list_of_phone_number_to_check),many=True).data , status = status.HTTP_200_OK)

        