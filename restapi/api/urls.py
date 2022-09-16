from api import views
from django.urls import path,include

urlpatterns = [
    path('',views.index,name="index"),
    path('create',views.create,name="create"),
    path('update/<int:id>',views.update,name="update"),
    path('delete/<int:id>',views.delete,name="delete"),
    path('register/',views.Registerview.as_view(),name="register"),
    path('login/',views.Loginview.as_view(),name="login"),
    path('profile/',views.ProfileView.as_view(),name="profile"),
    path('password_change/',views.PasswordChange.as_view(),name="password_change"),
    path('password_reset/',views.PasswordResetView.as_view(),name="password_reset"),
    path('reset_password/<uid>/<token>/',views.UserPasswordResetSerial.as_view(),name="reset_password"),
    path('product_add',views.ProductView.as_view(),name="product_add"),
    path('cart_show',views.CartView.as_view(),name="cart_show"),
    path('cart_add',views.CartView.as_view(),name="cart_add"),
    path('cart_delete/<int:id>',views.CartView.as_view(),name="cart_delete"),
    path('personlc',views.PersonListCreate.as_view(),name="personlc"),
    path('personrud/<int:pk>',views.Personrud.as_view(),name="personrud"),\
]
