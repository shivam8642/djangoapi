from dataclasses import field
from pyexpat import model
from django.forms import ValidationError
from rest_framework import serializers
from .models import Person, Product, Student
from .models import User,Cart
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class StudentSerail(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=Student
        fields=["id","name","email"]

    def validate(self, attrs):
        email=attrs.get('email')
        if Student.objects.filter(email=email).exists():
            raise ValidationError("Email Already Exists")
        return attrs

class Register(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_tyepe':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','first_name','last_name','city','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password !=password2:
            raise serializers.ValidationError("Password Does not match")
        
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class loginserial(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=User
        fields=['email','password']



class ProductSerial(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['name','price']

class CartSerial(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields="__all__"


class PersonSerial(serializers.ModelSerializer):
    email=serializers.EmailField()
    class Meta:
        model=Person
        fields=['id','name','email','city','age']

    def validate(self, attrs):
        email=attrs.get('email')
        if Person.objects.filter(email=email).exists():
            raise ValidationError("Email Already Exists")
        return attrs

    





class Profileserial(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','first_name','last_name','city']

class UserPasswordSerial(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_tyepe':'password'},write_only=True)
    password2=serializers.CharField(style={'input_tyepe':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password !=password2:
            raise serializers.ValidationError("Password Does not match")
        user.set_password(password)
        user.save()
        return attrs

class PasswordResetemail(serializers.Serializer):
    email=serializers.EmailField()
    class Meta:
        fields=['email']
    
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encode',uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token',token)
            link='http://localhost:3000/reset/'+uid+'/'+token
            print('password reset link',link)
            return attrs

        else:
            raise ValidationError("Email Does not Exists")
        return super().validate(attrs)

class UserpasswordResetSerializer(serializers.Serializer):
    password=serializers.CharField(style={'input_tyepe':'password'},write_only=True)
    password2=serializers.CharField(style={'input_tyepe':'password'},write_only=True)
    class Meta:
       
        fields=['password','password2']
    
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')
            if password !=password2:
                raise serializers.ValidationError("Password Does not match")
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError("Token is Not valid")
                
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError("Token is not valid or expire")

        