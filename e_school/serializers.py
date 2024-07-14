from rest_framework import serializers
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

User = get_user_model()

class EmailConfirmationSerializer(serializers.Serializer):
    key = serializers.CharField()

    def validate(self, data):
        try:
            uidb64, token = data['key'].split(':')
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if not default_token_generator.check_token(user, token):
                raise serializers.ValidationError('Invalid token')
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError('Invalid key')

        email_address = EmailAddress.objects.get(user=user)
        if email_address.verified:
            raise serializers.ValidationError('Email already confirmed')
        data['user'] = user
        data['email_address'] = email_address
        return data

    def save(self, validated_data):
        user = validated_data['user']
        email_address = validated_data['email_address']
        email_address.verified = True
        email_address.save()
        user.is_active = True
        user.save()