from rest_framework import  serializers
from .models import  gossips_account


class gossip_accountSerializer(serializers.ModelSerializer):
        class Meta:
            model =  gossips_account
            fields = ['username','real_name','profile_pic_url','bio','phone_number']
            