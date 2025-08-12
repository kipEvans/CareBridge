import json

import requests
from django.shortcuts import render,redirect, get_object_or_404

from hospitalapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from hospitalapp.models import*
from django.contrib.auth.models import User
from  django.contrib import messages
from django.contrib.auth import authenticate, login
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse



# Create your views here.
def index(request):
    return render(request,'index.html')

def service(request):
    return render(request,'service-details.html')

def starter(request):
    return render(request,'starter-page.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def departments(request):
    return render(request,'departments.html')

def doctors(request):
    return render(request,'doctors.html')



def Appointment(request):
   if request.method == 'POST':
       myappointment= Appoint(
           name = request.POST["name"],
           email = request.POST["email"],
           phone = request.POST["phone"],
           date = request.POST["date"],
           department = request.POST["department"],
           doctor = request.POST["doctor"],
           message = request.POST["message"],
       )

       myappointment.save()
       return redirect('/')

   else:
       return render(request, 'appointment.html')


def contacts(request):
  if request.method == 'POST':
    mycontact=Contact(
        name = request.POST["name"],
        email = request.POST["email"],
        subject = request.POST["subject"],
        message = request.POST["message"],
    )

    mycontact.save()
    return redirect('/')

  else:
      return render(request, 'contacts.html')

def show(request):
    all = Appoint.objects.all()
    return render(request, 'show.html',{"all":all})

def showcontacts(request):
    all = Contact.objects.all()
    return render(request, 'contacts.html',{"all":all})


def delete(request,id):
    deleteappointment = Appoint.objects.get(id=id)
    deleteappointment.delete()
    return redirect('/show')

def edit(request,id):
    edit_appointment = get_object_or_404(Appoint, id=id)

    if request.method == 'POST':
        edit_appointment.name = request.POST.get("name")
        edit_appointment.email = request.POST.get("email")
        edit_appointment.phone = request.POST.get("phone")
        edit_appointment.date = request.POST.get("date")
        edit_appointment.department = request.POST.get("department")
        edit_appointment.doctor = request.POST.get("doctor")
        edit_appointment.message = request.POST.get("message")

        edit_appointment.save()
        return redirect('/show')
    else:
        return render(request, 'edit.html',{"edit_appointment":edit_appointment})

def register(request):
    """ Show the registration form """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')

def loginview(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')


#Mpesa API VIEWS
def token(request):
    consumer_key = 't2zeWY1F3h3WUOZ56kAVDWvAOP088gDT6b1BiEyUtk8OJtek'
    consumer_secret = 'oCloE9E2PPBO9Xix3p0CHP4tcSBdgYcrMnyS9ypEtsTfEBuDBxRPPDMvjEiynpU8'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request,):
     return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/callback",
            "AccountReference": "Medilab",
            "TransactionDesc": "Appointment"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        if result_code == "0":
            # Only save transaction if it was successful
            transaction = Transaction(
                phone_number=phone,
                amount=amount,
                transaction_id=transaction_id,
                status="Success"
            )
            transaction.save()

            return HttpResponse(f"Transaction ID: {transaction_id}, Status: Success")
        else:
            return HttpResponse(f"Transaction Failed. Error Code: {result_code}")




def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})