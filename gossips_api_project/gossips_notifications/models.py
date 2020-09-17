from django.db import models


class  FCM_token(models.Model):
    username = models.CharField(blank = False , unique = True )
    
