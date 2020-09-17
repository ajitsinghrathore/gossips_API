from django.contrib import admin
from django.urls import path,include
from .views import  (Accounts_view ,
                     Filter_gossips_contacts_view,
                     full_profile,
                     search_users,
                     Verify_phone_number,
                     MY_auth_token_generator,
                     signup_view)




urlpatterns = [
        path('' ,Accounts_view.as_view()),
        path('signup/',signup_view.as_view()),
        path('filter_gossips_contacts/' , Filter_gossips_contacts_view.as_view()),
        path('full_profile/',full_profile.as_view()),
        path('search/',search_users.as_view()),
        path('verify/',Verify_phone_number.as_view()),
        path('get_session_token/',MY_auth_token_generator.as_view())
]