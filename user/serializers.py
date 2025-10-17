from rest_framework import serializers
from user.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'is_staff')

    def create(self, validated_data):
        user = User(username=validated_data['username'], email=validated_data.get('email', ''))
        user.set_password(validated_data['password'])
        user.is_staff = validated_data.get('is_staff', False)
        user.save()
        return user
    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        # Change field names for clarity
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }
        user = User.objects.filter(email=credentials['email']).first()
        if user and not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'email': self.user.email,
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return data
