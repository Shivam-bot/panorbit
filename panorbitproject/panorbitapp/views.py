from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .fetch_method import *


# Create your views here.

def home_page(request):
    if not request.session.get("authenticated"):
        return redirect("signup")
    return render(request, "home.html")


def signup(request):
    gender_choices = GenderEnum.gender_choices()
    data = {"gender_choices": gender_choices}
    if 'email' in request.session:
        return redirect("home_page")
    signup_form = UserForm(request.POST)
    if signup_form.is_valid() and signup_form.data.get("save_try") == "yes":
        signup_form = signup_form.save()
        request.session['username'] = signup_form.email
        request.session['email'] = signup_form.email
        request.session['first_name'] = signup_form.first_name
        request.session["request_for"] = "email"
        request.session["authenticated"] = False
        data["request_for"] = "email"
        data["email"] = signup_form.email
        return render(request, "otpverification.html", data)
    if signup_form.data.get("save_try") == "yes":
        data["form_error"] = signup_form.errors
        data["form_data"] = signup_form.data
    return render(request, 'signup.html', data)


def verifyotp(request):
    data = {}
    if not request.session.get("authenticated"):
        otp = request.POST.get("otp")
        email = request.session.get("email")

        request_for = request.session.get("request_for")
        user_otp = UserOTP.objects.get(user__email=email, request_for=request_for)
        if check_password(otp, user_otp.otp):
            del request.session["authenticated"]
            del request.session["request_for"]
            request.session["authenticated"] = True
            return redirect('/home_page', data)
        data['messages'] = ["Invalid Otp"]
    return render(request, "otpverification.html", data)


def send_otp(request):
    if not request.session.get("authenticated"):
        email = request.POST.get("email")
        save_try = request.POST.get("save_try")
        data = {}
        if save_try == "yes":
            try:
                user_data = CustomUser.objects.get(email=email)
            except Exception as e:
                return render(request, "login.html", {"messages": [f"Given email {email} not exists"]})
            otp = str(random_number(0000, 9999))
            send_email("Panorbit Email Verification ", f"Email verification code is : {otp} ", email)
            try:
                user_otp = UserOTP.objects.get(request_for="email", user=user_data)
                user_otp.otp = otp
                user_otp.save()
            except Exception as e:
                UserOTP.objects.create(otp=otp, request_for="email", user=user_data)
            data["request_for"] = "email"
            data["email"] = email
            data["success_messages"] = ["Email send successfully"]
            request.session['username'] = user_data.email
            request.session['email'] = user_data.email
            request.session['first_name'] = user_data.first_name
            request.session["request_for"] = "email"
            request.session["authenticated"] = False
            return render(request, "otpverification.html", data)
    return render(request, "login.html")


def login(request):
    if not request.session.get("authenticated"):
        return render(request, "login.html")
    else:
        return redirect("home_page")


def get_search_result(request):
    if not request.session.get("authenticated"):
        return render(request, "login.html")
    search_text = request.POST.get("search_text")
    country_data = Country.objects.filter(name__icontains=search_text)
    city_data = City.objects.filter(name__icontains=search_text)
    country_language = CountryLanguage.objects.filter(language__icontains=search_text).only('language')
    data = {}
    # data["status"]
    data["country"] = [(country.name, country.name) for country in country_data]
    data["city"] = [(city.name, city.name) for city in city_data]
    data["language"] = [(language.language, language.language) for language in country_language]
    return JsonResponse(data)


def search_value(request):
    data = {}
    data_list = []
    if not request.session.get("authenticated"):
        data["status"] = "failed"
        data["message"] = "Kindly log in"
        return render(request, "login.html",data)
    name = request.POST.get("name")
    search_for = request.POST.get("search_for")

    if search_for.lower() == 'country':
        country_data = Country.objects.filter(name__istartswith=name)
        for country in country_data:
            data_list.append(get_country_data(country.name))

    if search_for.lower() == 'city':
        city_data = City.objects.filter(name__istartswith=name)
        for city in city_data:
            data_list.append(get_country_data(city.country_code.name))
    if search_for.lower() == 'language':
        country_language = CountryLanguage.objects.filter(language__istartswith=name)
        for language in country_language:
            data_list.append(get_country_data(language.country_code.name))

    data["status"] = "success"
    data['country_data'] = data_list
    data['head'] = ['country_name', 'city_name', 'district', 'population', 'language', 'official',
                    'language_percentage']
    return JsonResponse(data)


def logout(request):
    if request.session.get("authenticated"):
        del request.session['username']
        del request.session['email']
        del request.session['first_name']
        del request.session["authenticated"]
    return redirect("signup")
