from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.core.files.storage import FileSystemStorage

# @login_required(login_url='login')
def create_payment(request):
    if request.method == "POST":
        amount_payed_str = request.POST["amount_payed"]
        amount_payed = amount_payed_str.replace('#', '')
        medium_of_payment = request.POST["medium_of_payment"]
        debtor_id = request.POST["debtor"]
        
        debtor = Debtor.objects.get(id=debtor_id)
        payment = Payment.objects.filter(debtor_id=debtor_id).last()
        
        if payment:
            balance_left = payment.balance_left
            
            if balance_left <= 0:
                messages.success(request, "This debtor has already completed their payment")
                return redirect('payments')
            
            new_payment = Payment()
            new_payment.amount_payed = amount_payed
            new_payment.medium_of_payment = medium_of_payment
            new_payment.balance_left = int(balance_left) - int(amount_payed)
            new_payment.debtor_id = debtor
            new_payment.client_id = debtor.client_id  # Assign the client instance as the client_id
            new_payment.status = "In Progress"
            new_payment.save()
            messages.success(request, "Payment details were successfully captured")
            return redirect('payments')
        else:
            amount_owed = debtor.amount_owed
            client = User.objects.get(id=debtor.client_id)

            payment = Payment()
            payment.amount_payed = amount_payed
            payment.medium_of_payment = medium_of_payment
            payment.balance_left = int(amount_owed) - int(amount_payed)
            payment.debtor_id = debtor
            payment.client_id = client  # Assign the client instance as the client_id
            payment.status = "In Progress"
            payment.save()
            messages.success(request, "Payment details were successfully captured")
            return redirect('payments')

    all_debtors = Debtor.objects.all()
    return render(request, "admins_dashboard/payments/create_payment.html", {'debtors': all_debtors})



def create_payment(request):
    if request.method == "POST":
        amount_payed_str = request.POST["amount_payed"]
        amount_payed = amount_payed_str.replace('#', '')
        medium_of_payment = request.POST["medium_of_payment"]
        debtor_id = request.POST["debtor"]
        
        debtor = Debtor.objects.get(id=debtor_id)
        payment = Payment.objects.filter(debtor_id=debtor_id).last()
        if payment:
            balance_left = payment.balance_left
            if balance_left <= 0:
                messages.success(request, "This debtor has already completed his payment")
                return redirect('payments')
                # What if the person made an overpaid last payment
            new_payment = Payment()
            new_payment.amount_payed = amount_payed
            new_payment.medium_of_payment = medium_of_payment
            new_payment.balance_left = int(balance_left) - int(amount_payed)
            new_payment.debtor_id = debtor
            new_payment.status = "In Progress"
            new_payment.save()
            messages.success(request, "Payment details were successfully captured")
            return redirect('payments')
        else:
            debtor = Debtor.objects.get(id=debtor_id)
            amount_owed = debtor.amount_owed
            client = User.objects.get(id=debtor.client_id)

            payment = Payment()
            payment.amount_payed = amount_payed
            payment.medium_of_payment = medium_of_payment
            payment.balance_left = int(amount_owed) - int(amount_payed)
            payment.debtor_id = debtor
            payment.client_id = client  # Corrected this line to assign the client instance
            payment.status = "In Progress"
            payment.save()
            messages.success(request, "Payment details were successfully captured")
            return redirect('payments')

    all_debtors = Debtor.objects.all()
    return render(request, "payments/create_payment.html", {'debtors': all_debtors})



def index(request):
    current_user = request.user
    if current_user.is_staff:
        all_debtors = Debtor.objects.all()[:5]
        all_payments = Payment.objects.all().order_by('date_payed').reverse()[:5]
        debtors = Debtor.objects.all()
        payments = Payment.objects.all()

        total = debtors.aggregate(Sum('amount_owed'))['amount_owed__sum']
        retrieved = payments.aggregate(Sum('amount_payed'))['amount_payed__sum']

        if total is None or retrieved is None:    
            return render(request, 'error_pages/admin_index.html', {})

        debt = total - retrieved
        return render(request, 'index.html', {'payments': all_payments, 'debtors': all_debtors, "total": total, "retrieved": retrieved, "debt": debt})

    else:

        my_payments = Payment.objects.filter(client_id=current_user.id).order_by('date_payed').reverse()[:5]
        my_debtors = Debtor.objects.filter(client_id=current_user.id)[:5]
        payments = Payment.objects.filter(client_id=current_user.id)
        debtors = Debtor.objects.filter(client_id=current_user.id)
        total = debtors.aggregate(Sum('amount_owed'))['amount_owed__sum']
        retrieved = payments.aggregate(Sum('amount_payed'))['amount_payed__sum']

        if total is None or retrieved is None:
            return render(request, 'error_pages/client_index.html', {})

        debt = total - retrieved
        return render(request, 'clients_dashboard/index.html', {'payments': my_payments, 'debtors': my_debtors, "total": total, "retrieved": retrieved, "debt": debt}) 



def create_payment(request):
    if request.method == "POST":
        amount_payed_str = request.POST["amount_payed"]
        amount_payed = amount_payed_str.replace('#', '')
        medium_of_payment = request.POST["medium_of_payment"]
        debtor_id = request.POST["debtor"]
        
        payment = Payment.objects.filter(debtor_id=debtor_id).last()
        if payment:
            balance_left = payment.balance_left
            if balance_left <= 0:
                messages.success(request, "This debtor has already completed his payment")
                return redirect('payments')
                # What if the person made an overpaid last payment
            new_payment = Payment()
            new_payment.amount_payed = amount_payed
            new_payment.medium_of_payment = medium_of_payment
            new_payment.balance_left = int(balance_left) - int(amount_payed)
            new_payment.debtor_id = debtor_id
            # payment.client_id = related_client_id
            new_payment.status = "In Progress"
            new_payment.save()
            messages.success(request, "Payment details were successfully captured")
            return redirect('payments')
        else:
            debtor = Debtor.objects.get(id=debtor_id)
            amount_owed = debtor.amount_owed
            related_client_id = debtor.client_id

            payment = Payment()
            payment.amount_payed = amount_payed
            payment.medium_of_payment = medium_of_payment
            payment.balance_left = int(amount_owed) - int(amount_payed)
            payment.debtor_id = debtor_id
            payment.client_id = related_client_id
            payment.status = "In Progress"
            payment.save()
            messages.success(request, "Payment details were successfully captured")
            return redirect('payments')

    all_debtors = Debtor.objects.all
    return render(request, "payments/create_payment.html", {'debtors': all_debtors})


def create_payment(request):
    if request.method == "POST":
        amount_payed_str = request.POST["amount_payed"]
        amount_payed = amount_payed_str.replace('#', '')
        medium_of_payment = request.POST["medium_of_payment"]
        debtor_id = int(request.POST["debtor"])
        
        try:
            debtor = Debtor.objects.get(id=debtor_id)  # Get the Debtor instance
            # debtor = Debtor.objects.get(id=debtor_id)
            # Calculate the balance_left
            last_payment = Payment.objects.filter(debtor_id=debtor).last()
            if last_payment:
                balance_left = last_payment.balance_left
                if balance_left <= 0:
                    messages.success(request, "This debtor has already completed their payment")
                    return redirect('payments')
            else:
                balance_left = debtor.amount_owed

            client = User.objects.get(id=debtor.client_id)  # Get the client's instance
            # client = User.objects.get(id=debtor.client_id)
            # Create a new Payment instance
            new_payment = Payment()
            new_payment.amount_payed = amount_payed
            new_payment.medium_of_payment = medium_of_payment
            new_payment.balance_left = max(balance_left - int(amount_payed), 0)  # Ensure balance_left is not negative
            new_payment.debtor_id = debtor  # Assign the Debtor instance to the ForeignKey field
            # new_payment.debtor_id = debtor_id
            new_payment.client_id = client  # Assign the User instance to the ForeignKey field
            new_payment.status = "In Progress"
            new_payment.save()
            messages.success(request, "Payment details were successfully captured")
        except Debtor.DoesNotExist:
            messages.error(request, "Debtor does not exist.")
        except User.DoesNotExist:
            messages.error(request, "Client does not exist.")

    all_debtors = Debtor.objects.all()
    return render(request, "payments/create_payment.html", {'debtors': all_debtors})



def debtors(request):
    all_debtors = Debtor.objects.all().order_by('date_captured').reverse()
    all_clients = User.objects.filter(is_superuser=False, is_staff=False)
    return render(request, 'debtors/debtors.html', {'debtors': all_debtors, 'clients': all_clients})


@login_required
def create_debtor(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        surname = request.POST["surname"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        amount_owed = request.POST["amount_owed"]
        due_date = request.POST["due_date"]
        client_id = request.POST["client"]

        # return render(request, "debtors/test.html", {'client': client_id}) 

        if firstname == "" or surname == "" or address == "" or phone == "" or email == "" or client_id == "":
            messages.success(request, "Please complete all input fields")
            all_clients = User.objects.filter(Q(is_superuser=False) & Q(is_staff=False))
            return render(request, "debtors/create_debtor.html", {'clients': all_clients})

        if phone != "" or email != "":
            if len(phone) < 11:
                messages.success(request, "The inputed phone number is less than 11 characters")
                all_clients = User.objects.filter(Q(is_superuser=False) & Q(is_staff=False))
                return render(request, "debtors/create_debtor.html", {'clients': all_clients})

            # The email inputs needs to be validated as well
            if Debtor.objects.filter(email=email).exists():
                messages.success(request, "Email already exists")
                all_clients = User.objects.filter(Q(is_superuser=False) & Q(is_staff=False))
                return render(request, "debtors/create_debtor.html", {'clients': all_clients})  

        debtor = Debtor()
        debtor.firstname = firstname
        debtor.surname = surname
        debtor.address = address
        debtor.phone = phone
        debtor.email = email
        debtor.amount_owed = amount_owed
        debtor.due_date = due_date
        debtor.client_id = client_id
        debtor.save()
        messages.success(request, "Details were successfully captured")
        return redirect('debtors')

    all_clients = User.objects.filter(Q(is_superuser=False) & Q(is_staff=False))
    # all_clients = User.objects.filter(is_superuser=False, is_staff=False)
    return render(request, "debtors/create_debtor.html", {'clients': all_clients})


@login_required
def index(request):
    # return HttpResponse('Halo')
    return render(request, 'index.html', {})

@login_required
def admins(request):
    superusers = User.objects.filter(is_superuser=True)
    return render(request, 'admins.html', {'superusers': superusers})

@login_required
def create_admin(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        role = request.POST["role"]

        if username == "" or email == "" or firstname == "" or lastname == "" or password == "":
            messages.success(request, "Please complete all input fields")
            return render(request, "authentication/create_account2.html")

        if username != "" or email != "":
            if len(username) < 8:
                messages.success(request, "Username must not be less than 8 characters")
                return render(request, "authentication/create_account2.html")

            if User.objects.filter(username=username).exists():
                messages.success(request, "Username already exists")
                return render(request, "authentication/create_account2.html")

            # The email inputs needs to be validated as well
            if User.objects.filter(email=email).exists():
                messages.success(request, "Email already exists")
                return render(request, "authentication/create_account2.html")   

        if not password == confirm_password:
            messages.success(request, "Your passwords did not match")
            return render(request, "authentication/create_account2.html")

        if role == "superadmin":
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.username = username
            user.is_superuser = True
            user.is_staff = True
            user.save()
            messages.success(request, "The " + role + " account was created")
            return redirect('admins')

        elif role == "editor":
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.username = username
            user.save()
            messages.success(request, "The " + role + " account was created")
            return redirect('admins')

    return render(request, "authentication/create_account2.html")

@login_required
def profile(request):
    return render(request, "profile/user_profile.html", {})

@login_required
def profile_update(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        # profile_pic = request.FILES["profile_pic"]

        User.objects.filter(id=request.user.id).update(username=username, email=email)

        # user_profile = UserProfile.objects.create(phone, address, profile_pic)
        user_profile.phone = phone
        user_profile.address = address
        # user_profile.profile_pic = profile_pic
        user_profile.save()

        return redirect('profile')

    return render(request, "profile/profile_update.html", {})


@login_required
def user_profile(request, user_id):
    if request.method == 'POST':
        user_obj = User.objects.get(id=user_id)
        user_profile_obj = UserProfile.objects.get(id=user_id)
        user_img = request.FILES['user_img']
        fs_handle = FileSystemStorage()
        img_name = 'uploads/profile_pictures/user_{0}'.format(user_id)

        if fs_handle.exists(img_name):
            fs_handle.delete(img_name)
        fs_handle.save(img_name, user_img)
        user_profile_obj.profile_pic = img_name
        user_profile_obj.save()
        user_profile_obj.refresh_from_db()
        return render(request, "profile/user_profile.html", {'my_profile': user_profile_obj})

    if (request.user.is_authenticated and request.user.id == user_id):
        user_obj = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(id=user_id)
        return render(request, "profile/user_profile.html", {'my_profile': user_profile})



@login_required
def profile(request, user_id):
    if user_id:
        user_profile = UserProfile.objects.get(user=user_id)
        return render(request, "profile/test.html", {'my_profile': user_profile})
        # return render(request, "profile/user_profile.html", {'my_profile': user_profile})


path("update/<int:user_id>", views.profile, name="update"),
path("profile/<int:user_id>", views.profile_update, name="profile_update"),
path("profile/<int:user_id>", views.user_profile, name="user_profile"),

@login_required
def update(request, user_id):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        User.objects.filter(id=request.user.id).update(username=username, email=email)
        UserProfile.objects.filter(user=request.user.id).update(phone=phone, address=address)
        # user_profile_obj = UserProfile.objects.get(id=user_id)
        return redirect('profile')
    return render(request, "profile/test_update.html", {})

@login_required
def profile_update(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]
        # profile_pic = request.FILES["profile_pic"]

        User.objects.filter(id=request.user.id).update(username=username, email=email)

        # user_profile = UserProfile.objects.create(phone, address, profile_pic)
        user_profile.phone = phone
        user_profile.address = address
        # user_profile.profile_pic = profile_pic
        user_profile.save()

        return redirect('profile')

    return render(request, "profile/profile_update.html", {})


@login_required
def user_profile(request, user_id):
    if request.method == 'POST':
        user_obj = User.objects.get(id=user_id)
        user_profile_obj = UserProfile.objects.get(id=user_id)
        user_img = request.FILES['user_img']
        fs_handle = FileSystemStorage()
        img_name = 'uploads/profile_pictures/user_{0}'.format(user_id)

        if fs_handle.exists(img_name):
            fs_handle.delete(img_name)
        fs_handle.save(img_name, user_img)
        user_profile_obj.profile_pic = img_name
        user_profile_obj.save()
        user_profile_obj.refresh_from_db()
        return render(request, "profile/user_profile.html", {'my_profile': user_profile_obj})

    if (request.user.is_authenticated and request.user.id == user_id):
        user_obj = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(id=user_id)
        return render(request, "profile/user_profile.html", {'my_profile': user_profile})


# Updates everything without the image
@login_required
def profile_update(request, user_id):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        User.objects.filter(id=request.user.id).update(username=username, email=email)
        UserProfile.objects.filter(user=request.user.id).update(phone=phone, address=address)
        # user_profile_obj = UserProfile.objects.get(id=user_id)
        return render(request, "profile/user_profile.html")

    return render(request, "profile/profile_update.html", {})

# Updates only the image
@login_required
def profile_update(request, user_id):
    if request.method == 'POST':
        user_obj = User.objects.get(id=user_id)
        user_profile_obj = UserProfile.objects.get(user=user_id)
        user_img = request.FILES['user_img']
        fs_handle = FileSystemStorage()
        img_name = 'uploads/profile_pictures/user_{0}'.format(user_id)

        if fs_handle.exists(img_name):
            fs_handle.delete(img_name)
        fs_handle.save(img_name, user_img)
        user_profile_obj.profile_pic = img_name
        user_profile_obj.save()
        user_profile_obj.refresh_from_db()
        return render(request, "profile/user_profile.html", {'my_profile': user_profile_obj})

    return render(request, "profile/profile_update.html", {})


# Save all but has issues if image is not updated
@login_required
def profile_update(request, user_id):
    if request.method == 'POST':
        user_obj = User.objects.get(id=user_id)
        user_profile_obj = UserProfile.objects.get(user=user_id)

        user_img = request.FILES['user_img']
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        # User.objects.filter(id=request.user.id).update(username=username, email=email)
        # Image handling
        fs_handle = FileSystemStorage()
        img_name = 'uploads/profile_pictures/user_{0}'.format(user_id)
        if fs_handle.exists(img_name):
            fs_handle.delete(img_name)
        fs_handle.save(img_name, user_img)

        user_profile_obj.profile_pic = img_name
        
        user_profile_obj.phone = phone
        user_profile_obj.address = address
        user_profile_obj.save()
        # user_profile_obj.refresh_from_db()
        user_obj.username =  username
        user_obj.email = email
        user_obj.save()
        user_obj.refresh_from_db()
        

        return render(request, "profile/user_profile.html", {'my_profile': user_profile_obj})

    return render(request, "profile/profile_update.html", {})

    @login_required
def profile_update(request, user_id):
    if request.method == 'POST':
        user_obj = User.objects.get(id=user_id)
        user_profile_obj = UserProfile.objects.get(user=user_id)

        user_img = request.FILES['user_img']
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        # User.objects.filter(id=request.user.id).update(username=username, email=email)
        # Image handling
        fs_handle = FileSystemStorage()
        img_name = 'uploads/profile_pictures/user_{0}'.format(user_id)
        if fs_handle.exists(img_name):
            fs_handle.delete(img_name)
        fs_handle.save(img_name, user_img)

        user_profile_obj.profile_pic = img_name
        
        user_profile_obj.phone = phone
        user_profile_obj.address = address
        user_profile_obj.save()
        # user_profile_obj.refresh_from_db()
        user_obj.username =  username
        user_obj.email = email
        user_obj.save()
        user_obj.refresh_from_db()
        

        return render(request, "profile/user_profile.html", {'my_profile': user_profile_obj})

    return render(request, "profile/profile_update.html", {})

@login_required
def admin_edited(request, user_id):
    if request.method == 'POST':
        details = User.objects.get(id=user_id)
        details_profile = UserProfile.objects.get(user=user_id)

        if 'user_img' in request.FILES:
            user_img = request.FILES['user_img']
            fs_handle = FileSystemStorage()
            img_name = 'uploads/profile_pictures/user_{0}'.format(user_id)
            if fs_handle.exists(img_name):
                fs_handle.delete(img_name)
            fs_handle.save(img_name, user_img)
            details_profile_obj.profile_pic = img_name

        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        details_profile.phone = phone
        details_profile.address = address
        details_profile.save()
        
        details.username =  username
        details.email = email
        details.save()
        details.refresh_from_db()
        

        return render(request, "admins/admin_edit.html", {'details_profile': details_profile, 'details': details})

    return render(request, "admins/admin_edit.html", {})


# DELETE MULTIPLE OPERATION
<form method="post" action="{% url 'delete_view' %}">
  {% csrf_token %}
  <table>
    <thead>
      <tr>
        <th>Record ID</th>
        <th>Record Name</th>
        <th>Select</th>
      </tr>
    </thead>
    <tbody>
      {% for record in records %}
      <tr>
        <td>{{ record.id }}</td>
        <td>{{ record.name }}</td>
        <td>
          <input type="checkbox" name="selected_records" value="{{ record.id }}">
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <button type="submit">Delete Selected</button>
</form>



from django.shortcuts import redirect

def delete_view(request):
    # Get the list of selected records
    selected_records = request.POST.getlist('selected_records')

    # Convert the list of strings to a list of integers
    selected_records = [int(i) for i in selected_records]

    # Filter the records using the `id__in` lookup and delete them
    MyModel.objects.filter(id__in=selected_records).delete()

    # Redirect to the success page
    return redirect('success_url')


# FETCH DATA FROM THE DATABASE AND DISPLAY THEM AS VALUES OF A SELECT FORM FIELD
# This is to be implemented on the debtors module - when creating a debtor, to ensure 
# each debtor is linked to a client
def country_view(request):
    countries = Country.objects.all()
    return render(request, 'countries.html', {'countries': countries})


<form method="post">
    {% csrf_token %}
    <select name="country">
        {% for country in countries %}
        <option value="{{ country.id }}">{{ country.name }}</option>
        {% endfor %}
    </select>
    <input type="submit" value="Submit">
</form>


# SENDING AN SMS NOTIFICATION  TO A SINGLE USER
from twilio.rest import Client

def send_sms(request):
    # Your Twilio account SID and auth token
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # Send an SMS message
    message = client.messages \
                    .create(
                         body='Hello from Django!',
                         from_='your_twilio_number',
                         to='recipient_number'
                     )

    return HttpResponse('SMS sent!')

# SENDING AN SMS NOTIFICATION TO MULTIPLE USERS
# ACCOUNT SID: ACff725ea0e61eb2570afe3f717dadf3a9
# AUTH TOKEN: 7b1cc58d56b3e14dc292cc2ccb3a3b01
from twilio.rest import Client

def send_bulk_sms(request):
    # Your Twilio account SID and auth token
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # A list of phone numbers to send the SMS to
    recipient_numbers = ['+1234567890', '+0987654321', '+1231231234']

    # Loop through the list of numbers and send an SMS to each one
    for number in recipient_numbers:
        message = client.messages \
                        .create(
                             body='Hello from Django!',
                             from_='your_twilio_number',
                             to=number
                         )

    return HttpResponse('Bulk SMS sent!')

# A better way to do it
<form method="post" action="{% url 'send_sms' %}">
    {% csrf_token %}
    {% for user in users %}
        <input type="checkbox" name="selected_users" value="{{ user.id }}"> {{ user.username }}<br>
    {% endfor %}
    <input type="submit" value="Send SMS">
</form>

from django.shortcuts import render, redirect
from .models import User

def send_sms(request):
    if request.method == 'POST':
        selected_user_ids = request.POST.getlist('selected_users')
        users = User.objects.filter(id__in=selected_user_ids)
        phone_numbers = [user.phone_number for user in users]
        # Send an SMS to each phone number using a third-party SMS service such as Twilio or Nexmo
        return redirect('success')
    else:
        users = User.objects.all()
        return render(request, 'users.html', {'users': users})



