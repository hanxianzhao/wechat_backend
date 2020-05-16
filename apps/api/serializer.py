import re

from rest_framework import serializers
# 导入序列化错误提示信息包
from rest_framework.exceptions import ValidationError


def phone_validators(value):
    """
    手机号校验钩子函数
    :param value: 需要校验的手机号
    :return:
    """
    if not re.search(r"^\d{11}$", value):
        return ValidationError("手机号格式错误")


class MessageSerializer(serializers.Serializer):
    """
    获取验证码时手机号的校验
    """
    # 由于使用的serializers.Serializer 不是 serializers.ModelSerializer 所以不能使用class Meta(),只能手动去增加每个字段
    phone = serializers.CharField(label="手机号", validators=[phone_validators, ])

    # 钩子函数
    # def validate_phone(self, value):
    #     pass


class LoginSerializer(serializers.Serializer):
    """
    登录时手机号及验证码的校验
    """
    phone = serializers.CharField(label="手机号", validators=[phone_validators, ])
    code = serializers.CharField(label="验证码")

    def validate_code(self, value):
        """
        验证码的钩子函数
        :param value: 用户传进的验证码
        :return:
        """
        if not re.search(r"^\d{4}$", value):
            raise ValidationError("验证码错误")
        return value

