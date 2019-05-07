from django import http
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from pytz import unicode
from rest_framework.authentication import BasicAuthentication

from Mailer.settings import AUTH_USER_MODEL as User
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from MailServiceApp.Serializers import MailSerializer, AccountSerializer, SendingDataSerializer
from MailServiceApp.forms import MailForm, LoginForm
from MailServiceApp.models import Mail, Account
from Mailer.settings import EMAIL_HOST_USER


class MailDetails(APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        try:
            return Mail.objects.get(pk=pk)
        except Mail.DoesNotExist:
            raise Http404

    def get(self, request, pk ):
        mail = self.get_object(pk)
        serializer = MailSerializer(mail)
        return Response(serializer.data)

    def put(self, request, pk ):
        mail = self.get_object(pk)
        serializer = MailSerializer(mail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        mail = self.get_object(pk)
        mail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MailList(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        mails = Mail.objects.all()[:10]
        serializer = MailSerializer(mails, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendMail(APIView):
    permission_classes = (IsAuthenticated,)             # <-- And here
    def post(self, request):
        mailData = SendingDataSerializer(data = request.data)

        pk = request.data['mailpk']
        recipient = request.data['recipientMail']

        mail = Mail.objects.get(pk=pk)
        recipients = []
        recipients.append(recipient)
        send_mail(subject=mail.subject, message=mail.text,
                  recipient_list=recipients, from_email=EMAIL_HOST_USER, fail_silently=False)
        content = {'message': 'your email sent'}

        return Response(content)




class Something(APIView):

    def post(self, request):

        accSerializer = AccountSerializer(data = request.data)

        if accSerializer.is_valid():
            account = accSerializer.save()

            token = Token.objects.get(user=account)
            return Response({ "yourToken"  : str(token)})


        else:
            return Response(accSerializer.errors)



class Sendmail(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):

        account = request.user

        pk = request.data['mailpk']

        mail = Mail.objects.get(pk=pk)

        for f in account.friends.iterator():

            recipients = []

            recipients.append(str(f.email))


            send_mail(subject=mail.subject, message=mail.text,
                      recipient_list=recipients, from_email=EMAIL_HOST_USER, fail_silently=False)

        return Response({"info" : "massage sent", "subject": str(mail.subject)})