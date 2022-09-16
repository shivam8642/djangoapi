
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Cart, Product, Student,Person
from .serializers import CartSerial, ProductSerial, StudentSerail,PersonSerial
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import Register,loginserial,Profileserial,UserPasswordSerial,PasswordResetemail,UserpasswordResetSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class PersonListCreate(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset=Person.objects.all()
    serializer_class=PersonSerial
    def get(self,request,*args, **kwargs):
        return self.list(request,*args,**kwargs)

    def post(self,request,*args, **kwargs):
        return self.create(request,*args,**kwargs)



class Personrud(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset=Person.objects.all()
    serializer_class=PersonSerial
    def get(self,request,*args, **kwargs):
        return self.retrieve(request,*args,**kwargs)
    def put(self,request,*args, **kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args, **kwargs):
        return self.destroy(request,*args,**kwargs)



   



















































# Create your views here.
class Registerview(APIView):
    def post(self,request,format=None):
        serial=Register(data=request.data)
        if serial.is_valid(raise_exception=True):
            user=serial.save()
            return Response({'msg':"Account Created Successfully"},status=status.HTTP_201_CREATED)
        return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)


class Loginview(APIView):
    def post(self,request,format=None):
        ser=loginserial(data=request.data)
        if ser.is_valid(raise_exception=True):
            email=ser.data.get('email')
            password=ser.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'token':token,'msg':'login succes'},status=status.HTTP_200_OK)
            else:
                return Response({'msg':'email or password in invalid'},status=status.HTTP_404_NOT_FOUND)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)

class ProductView(APIView):
    permission_classes=[IsAdminUser]
    def get(self, request):
        obj=Product.objects.all()
        ser=ProductSerial(obj,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)

    def post(self,request,format=None):
        proser=ProductSerial(data=request.data)
        if proser.is_valid():
            proser.save()
            return Response({"msg":"Admin Add to Product Successfully"},status=status.HTTP_201_CREATED)
        return Response(proser.errors,status=status.HTTP_400_BAD_REQUEST)

class CartView(APIView):
    permission_classes=[IsAuthenticated, ]
    def get(self,request,format=None):
        current_user=request.user.id
        obj=Cart.objects.filter(userid=current_user)
        ser=CartSerial(obj,many=True)
        return Response(ser.data,status=status.HTTP_200_OK)

    def post(self,request,format=None):
        data = request.data
        product = data.get("product")
        current_user=request.user.id
        quantity = data.get("quantity")
        user_id=data.get("userid")
        if user_id ==current_user:
            item=Cart.objects.filter(userid=current_user, product=product).exists()
        else:
                return Response({'msg':"Id not match with login user"})
        if not item:
            if user_id ==current_user:
                product = Product.objects.get(id=product)
                Cart.objects.create(product=product, userid=current_user, quantity=quantity)
                return Response({"msg":"data created"},status=status.HTTP_201_CREATED)
            else:
                return Response({'msg':"Id not match with login user"})
        return Response({"msg":"already exists."},status=status.HTTP_409_CONFLICT)
    


    def delete(self,request,id,format=None):
        current_user=request.user.id
        try:
            student=Cart.objects.get(id=id,userid=current_user)
            print(student)
        except Cart.DoesNotExist:
            return Response("id not found")
        if request.method=="DELETE":
            Cart.objects.get(id=id).delete()
            return Response({"msg":"Data deleted"}) 
    


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serail=Profileserial(request.user)
        return Response(serail.data,status=status.HTTP_200_OK)


class PasswordChange(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        serial=UserPasswordSerial(data=request.data,context={'user':request.user})
        if serial.is_valid(raise_exception=True):
            return Response({'msg':'Password Change Successfully'},status=status.HTTP_200_OK)
        return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    def post(self,request,format=None):
        serializer=PasswordResetemail(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset Link send successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserPasswordResetSerial(APIView):
    def post(self,request,uid,token,format=None):
        serializer=UserpasswordResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Password Reset successfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def index(request):
    stu=Student.objects.all()
    serail=StudentSerail(stu,many=True)
    return Response(serail.data,status=status.HTTP_200_OK)



@api_view(['POST'])
def create(request):
    data=request.data
    serial=StudentSerail(data=data)
    if serial.is_valid():
        serial.save()
        return Response(serial.data)
    else:
        return Response(serial.errors)


@api_view(['DELETE'])
def delete(request,id):
    try:
        student=Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response("id not found")
    if request.method=="DELETE":
        Student.objects.get(id=id).delete()
        return Response({"msg":"Data deleted"}) 

@api_view(['PUT'])
def update(request,id):
    try:
        student=Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response("id not found")
    if request.method=="PUT":
        data=request.data
        serial=StudentSerail(student,data=data)
        if serial.is_valid():
            serial.save()
            return Response({"msg":"Data Updated"})
        else:
            return Response(serial.errors)
