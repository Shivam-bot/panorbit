from django.urls import path
from . import views

urlpatterns = [
    path('sign-up', views.signup, name="signup"),
    path('verify-otp', views.verifyotp, name="verify-otp"),
    path('home_page', views.home_page, name="home_page"),
    path('login', views.login, name="login"),
    path('send_otp', views.send_otp, name="send_otp"),
    path('get_search_result', views.get_search_result, name="get_search_result"),
    path('search_value', views.search_value, name="search_value"),
    path('log_out', views.logout, name="log_out"),
]