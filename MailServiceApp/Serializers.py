from rest_framework import serializers

from MailServiceApp.models import Mail, Account


class MailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mail
        fields = ('subject' , 'text')


class SendingDataSerializer(serializers.Serializer) :
    mailpk = serializers.IntegerField()
    recepientMail = serializers.EmailField()

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('username', 'password', 'email')