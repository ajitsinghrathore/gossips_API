from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager



class Account_Manager(BaseUserManager):
        
        def create_user(self ,username, real_name , phone_number , profile_pic_url ,bio , password):
                    if not username:
                        raise ValueError("User must have username")
                    if not real_name:
                        raise ValueError("users must have their names")
                    if not phone_number:
                        raise ValueError("phone number is required")
                    if not password:
                        raise ValueError("password is must")
                    if not profile_pic_url:
                        profile_pic_url = " "
                    if not bio :
                        bio = " "

                    user =  self.model(
                           username = username,
                           phone_number = phone_number,
                           real_name = real_name,
                           profile_pic_url = profile_pic_url,
                           bio = bio
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
            username =  models.CharField(max_length = 30 , unique=True)
            real_name = models.CharField(max_length=30 , unique = False)
            profile_pic_url = models.URLField(max_length=1000)
            fcm_token = models.CharField(max_length = 2000 )
            bio = models.TextField()
            phone_number = models.CharField(max_length=20 , unique=True)
            

            date_joined = models.DateTimeField(verbose_name="date added",auto_now_add=True)
            last_login = models.DateTimeField(verbose_name="last login" , auto_now=True)
            is_active = models.BooleanField(default=True)
            is_staff = models.BooleanField(default=False)
            is_superuser = models.BooleanField(default=False)
            is_admin = models.BooleanField(default = False)


            USERNAME_FIELD = 'username'
            REQUIRED_FIELDS = ['real_name','phone_number','profile_pic_url' ,'bio']


            objects = Account_Manager()

            def has_perm(self,perm,obj = None):
                    return self.is_admin

            def has_module_perms(self,app_label):
                    return True        




