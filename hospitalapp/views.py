
from django.shortcuts import render,redirect, get_object_or_404
from hospitalapp.models import*
from django.contrib.auth.models import User
from  django.contrib import messages
from django.contrib.auth import authenticate, login

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