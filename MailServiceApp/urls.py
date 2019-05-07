from django.contrib import admin
from django.urls import path, include
from .views import submitMail, login, MailDetails, MailList, SendMail, Something, Sendmail

app_name = "MailServiceApp"
urlpatterns = [

    path('submit-account/' , Something.as_view()),
    path('sendmail/', Sendmail.as_view()),
    # path('register/', Register.as_view()),


    path('api/<pk>/', MailDetails.as_view()),
    path('api/', MailList.as_view())

]