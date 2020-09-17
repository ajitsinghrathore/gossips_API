from rest_framework import  permissions
from  django.core import signing



class  Account_view_permission(permissions.BasePermission):
        
        message = "You can update only your profile"
        def has_object_permission(self , request,view , obj):
            print("entered permissions",obj.username,request.user)
            if not request.method in permissions.SAFE_METHODS:
                if request.user.username != obj.username  :
                    return False
                elif  request.data.get('username',None):
                    self.message = "you cannot update your username"
                    return False  

            return True


class full_profile_view_permission(permissions.BasePermission):


    
    message = "your permission is invalid"
    def check_eligible(self,target_user_profile,request):
        key = target_user_profile.get('public_key',None)
        document_to_decrypted = request.headers.get('signed_doc')
        try:
            doc = signing.loads(document_to_decrypted , key = key )
            if doc.username == request.user.username:
                 return True
            return False
        except signing.BadSignature:
            return False



    def has_object_permission(self , request , view , obj):
        return self.check_eligible(obj , request)



class  signup_or_token_generator_view_permission(permissions.BasePermission):
    message = "verify your phone number first"


    def has_permission(self, request, view):
        signed_token = request.data.get('signed_token',None)
        print(signed_token)
        my_phone_number = request.data.get("phone_number",None)
        try:
            JSON  = signing.loads(signed_token)
            print(JSON)
            if JSON.get('number_verified',False) and JSON.get("phone_number") == my_phone_number:
                return True
            return  False

        except Exception as e:
            print(e)
            return  False


