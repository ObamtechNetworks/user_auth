from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            # make the pasword only writeonly purpose, so password is hidden after user is returned
            'password': {'write_only': True}  # the password is only for write only purpose , so when user is returned, password won't show
        }
    
    def validate_password(self, value):
        # Implement custom password validation rules here if needed
        # For example, checking for minimum length, special characters, etc.
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # extract/remove the password

        # Validate the password separately
        self.validate_password(password)

        instance = self.Meta.model(**validated_data)  # pass the validated datad without the extracted password
        if password is not None:
            instance.set_password(password)  # use password provided by django so it will be hashed
        instance.save()  # save the modification and return the instance
        return instance
