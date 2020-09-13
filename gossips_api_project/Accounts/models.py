from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from .validators import  username_validator , real_name_validator , phone_validator



class Account_Manager(BaseUserManager):
        
        def create_user(self ,username, real_name , phone_number , password):
                    if not username:
                        raise ValueError("User must have username")
                    if not real_name:
                        raise ValueError("users must have their names")
                    if not phone_number:
                        raise ValueError("phone number is required")
                    if not password:
                        raise ValueError("password is must")
                    

                    user =  self.model(
                           username = username,
                           phone_number = phone_number,
                           real_name = real_name,
                    )    

                    user.set_password(password)
                    user.save(using=self._db)
                    return user


        def create_superuser(self,username,real_name,phone_number,profile_pic_url,bio,password):
            user = self.create_user(username,real_name,phone_number,profile_pic_url,bio,password)
            user.is_staff = True
            user.is_superuser = True
            user.is_admin = True
            user.save(using=self._db)
            return user


                    









class gossips_account(AbstractBaseUser):


            username =  models.CharField(blank= False,max_length = 30 , unique=True , validators=[username_validator])
            real_name = models.CharField(blank = False , max_length=30 , unique = False , validators = [real_name_validator])
            profile_pic_url = models.URLField(default = "https://google.com",max_length=1000)
            fcm_token = models.CharField(blank = True,max_length = 2000 )
            bio = models.TextField(blank = True)
            phone_number = models.CharField(blank = False,max_length=20 , unique=True ,validators=[phone_validator])
            

            date_joined = models.DateTimeField(verbose_name="date added",auto_now_add=True)
            last_login = models.DateTimeField(verbose_name="last login" , auto_now=True)
            is_active = models.BooleanField(default=True)
            is_staff = models.BooleanField(default=False)
            is_superuser = models.BooleanField(default=False)
            is_admin = models.BooleanField(default = False)


            USERNAME_FIELD = 'username'
            REQUIRED_FIELDS = ['real_name','phone_number']


            objects = Account_Manager()

            def has_perm(self,perm,obj = None):
                    return self.is_admin

            def has_module_perms(self,app_label):
                    return True        




