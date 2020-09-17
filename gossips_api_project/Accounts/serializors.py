from rest_framework import  serializers
from .models import  gossips_account
from .validators import  password_validator
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from  rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class gossip_accountSerializer(serializers.ModelSerializer):


        password = serializers.CharField(required = True ,validators=[password_validator])
        normal_access_level = ['username' , 'real_name','profile_pic_url','bio']
        access_with_phone_number_level = normal_access_level + ['phone_number']

        class Meta:
            model  =  gossips_account
            fields = ['is_active','username','real_name','profile_pic_url','bio','phone_number','password','public_key']

       
        
        def create(self,validated_data):
            validated_data['password'] = make_password(validated_data['password'])
            return super().create(validated_data)

        def __init__(self,*args,**kwargs):
            fields = kwargs.pop('fields' , None)
            super(gossip_accountSerializer,self).__init__(*args,**kwargs)

        
            if fields is not None:
                allowed = set(fields)
                existing = set(self.fields)
                for field_name in existing - allowed:
                    self.fields.pop(field_name)

            elif not self.context.get('updating',False):
                 allowed = set(self.normal_access_level)
                 existing = set(self.fields)
                 for field_name in existing - allowed:
                        self.fields.pop(field_name)



class  auth_token_serializer(TokenObtainPairSerializer):

        @classmethod
        def get_token(cls, user):
            token = super().get_token(user)
            return token

