from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

# 获取自定义User
User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册
    """

    class Meta:
        model = User
        fields = ('username', 'password', 'name', 'email')

    username = serializers.CharField(label="用户名", help_text="用户名", required=True, allow_blank=False,
                                     validators=[
                                         UniqueValidator(queryset=User.objects.all(), message="用户已经存在")
                                     ])

    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,
    )

    def create(self, validated_data):
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户信息
    """

    class Meta:
        model = User
        fields = ('id', 'username')
