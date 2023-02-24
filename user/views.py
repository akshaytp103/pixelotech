from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserSignupAPIView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        name = request.data.get('name')
        if otp == '00000': # hardcoded static OTP for demo purposes
            user, created = User.objects.get_or_create(username=mobile)
            if created:
                user.set_password('password') # set a default password
                user.first_name = name
                user.save()
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

class UserSigninAPIView(APIView):
    def post(self, request):
        mobile = request.data.get('mobile')
        otp = request.data.get('otp')
        user = authenticate(username=mobile, password='password') # authenticate with a default password
        if user is not None and otp == '00000': # hardcoded static OTP for demo purposes
            login(request, user)
            serializer = UserSerializer(user)
            return Response({'message': f'Welcome {user.first_name}', 'user': serializer.data})
        else:
            return Response({'message': 'Invalid mobile number or OTP'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         mobile = request.POST.get('mobile')
#         otp = request.POST.get('otp')
#         name = request.POST.get('name')
#         if otp == '00000': # hardcoded static OTP for demo purposes
#             user, created = User.objects.get_or_create(username=mobile)
#             if created:
#                 user.set_password('password') # set a default password
#                 user.first_name = name
#                 user.save()
#                 return JsonResponse({'message': 'User created successfully'})
#             else:
#                 return JsonResponse({'message': 'User already exists'})
#         else:
#             return JsonResponse({'message': 'Invalid OTP'})

# @csrf_exempt
# def signin(request):
#     if request.method == 'POST':
#         mobile = request.POST.get('mobile')
#         otp = request.POST.get('otp')
#         user = authenticate(username=mobile, password='password') # authenticate with a default password
#         if user is not None and otp == '00000': # hardcoded static OTP for demo purposes
#             login(request, user)
#             return JsonResponse({'message': f'Welcome {user.first_name}'})
#         else:
#             return JsonResponse({'message': 'Invalid mobile number or OTP'})