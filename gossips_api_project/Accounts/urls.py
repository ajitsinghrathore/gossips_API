from django.contrib import admin
from django.urls import path,include
from .views import  Accounts_view ,Filter_gossips_contacts_view




urlpatterns = [
        path('' ,Accounts_view.as_view() , name = "get_user_account"),
        path('filter_gossips_contacts/' , Filter_gossips_contacts_view.as_view() , name = "filter_conctacts")
]