import json
from rest_framework import serializers
from cryptography.fernet import Fernet
from .models import CredentialDetail
from django.conf import settings
from utils.helpers import encrypt, decrypt


class CreateCredentialsSerailzier(serializers.Serializer):
    credential = serializers.CharField()
    website = serializers.URLField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = CredentialDetail
        fields = ('credential', 'website', 'password')

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        attrs['password'] = encrypt(attrs['password1'])
        return attrs

    def create(self, validated_data, **kwargs):
        credentail = validated_data['credential']
        website = validated_data['website']
        password = validated_data['password'].decode()
        user = self.request.user
        CredentialDetail.objects.create(
            credential=credentail,
            website=website,
            password=password,
            user=user
        )


class GetCredentials(serializers.Serializer):
    credential_list = serializers.SerializerMethodField()

    def get_credential_list(self, obj):
        request = self.context['request']
        data = CredentialDetail.objects.filter(user=request.user)
        cred_list = []
        for item in data:
            item_dicts = {}
            item_dicts['credential'] = item.credential
            item_dicts['website'] = item.website
            item_dicts['password'] = decrypt(item.password)

            cred_list.append(item_dicts)

        return cred_list
