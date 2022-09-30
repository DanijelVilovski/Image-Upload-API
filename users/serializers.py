from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ['id', 'username', 'password', 'is_active', 'is_staff', 'is_superuser']
        # extra_kwargs = {
        #     'password': {'write_only': True}
        # }
        
    def create(self, validated_data):
        user_pass = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if user_pass is not None:
            instance.set_password(user_pass)
        
        instance.is_active = False
        instance.save()
        return instance