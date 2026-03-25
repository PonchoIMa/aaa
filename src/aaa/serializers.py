from rest_framework import serializers
from .models import User
import bcrypt

class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only = True)

    class Meta:
        model           = User
        fields          = ['email', 'first_name',
                           'last_name', 'password', 'password_confirm']
        extra_kwargs    = {
                            'password': {'write_only': True} 
                          }

    def validate(self, data):
        if(data['password'] != data['password_confirm']):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # remove the unencrypted passwords
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        
        user = User(**validated_data)
        
        # overwriting djangos password methods
        salt            = bcrypt.gensalt()
        hashed          = bcrypt.hashpw(password.encode('utf-8'), salt)
        user.password   = hashed.decode('utf-8')
        
        user.save()
        return user
