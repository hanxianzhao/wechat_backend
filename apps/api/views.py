import random

import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import redis
from api.serializer import MessageSerializer, LoginSerializer
from django_redis import get_redis_connection


# Create your views here.


class LoginView(APIView):
    def post(self, request, *args, **kwargs):

        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"message": "验证码错误", "status": False})
        user_code = ser.validated_data.get("code")
        user_phone = ser.validated_data.get("phone")
        # redis 获取先前保存的数据
        conn = get_redis_connection()
        # 对验证码进行比较
        # 对于数据库获取的内容为bytes 需要解码
        if user_code == conn.get(user_phone).decode("utf-8"):
            data = {"phone": user_phone, "token": "qwertyu"}
            return Response({"data": data, "status": True})
        else:
            return Response({"status": False})

class GetMessageView(APIView):
    def get(self, request, *args, **kwargs):
        """
        获取验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1、获取用户的手机号
        # 2、手机号格式校验，使用序列化校验
        # 3、生成一个随机验证码
        # 4、将验证码发送给用户手机
        # 5、将验证码保存到自己的redis中
        ser = MessageSerializer(data=request.query_params)
        # 如果没有校验通过 报错
        if not ser.is_valid():
            return Response({"message": "手机格式错误", "status": False})
        phone = ser.validated_data.get("phone")
        random_code = random.randint(1000, 9999)

        # redis 保存数据
        conn = get_redis_connection()
        conn.set(phone, random_code, ex=30)

        return Response({"message": str(random_code), "status": True})
