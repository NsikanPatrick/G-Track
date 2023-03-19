from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages
from .models import UserProfile, Debtor, Payment
from django.core.files.storage import FileSystemStorage
# Imports for sending emails
# from django.http import HttpResponseBadRequest
from django.core.mail import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
# import ssl
# import smtplib
import smtplib
import ssl
from django.core.mail import EmailMessage
from django.http import HttpResponseBadRequest
import sched
import time
import datetime
import pytz


# @login_required(login_url='login')
@login_required
def index(request):
    # return HttpResponse('Halo')
    # return render(request, 'index.html', {})
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

@login_required
def admins(request):
    # Get the currently logged in user
    current_user = request.user
     # Fetch all admins from the database who are either super admins or staff admins 
    #  (editors) excluding the currently logged in admin
    all_admins = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True)).exclude(pk=current_user.pk).order_by('date_joined').reverse()
    all_admins_profiles = UserProfile.objects.all
    return render(request, 'admins_dashboard/admins.html', {'admins': all_admins, 'admin_profiles': all_admins_profiles})

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
            messages.success(request, "The " + role+"s account was created")
            return redirect('admins')

        elif role == "editor":
            user = User.objects.create_user(username, email, password)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.username = username
            user.is_staff = True
            user.save()
            messages.success(request, "The " + role+"s account was created")
            return redirect('admins')

    return render(request, "authentication/create_account2.html")

@login_required
def profile(request, user_id):
    if user_id:
        user_profile = UserProfile.objects.get(user=user_id)
        # return render(request, "profile/test.html", {'my_profile': user_profile})
        return render(request, "profile/user_profile.html", {'my_profile': user_profile})

@login_required
def profile_update(request, user_id):
    if request.method == 'POST':
        user_obj = User.objects.get(id=user_id)
        user_profile_obj = UserProfile.objects.get(user=user_id)

        if 'user_img' in request.FILES:
            user_img = request.FILES['user_img']
            fs_handle = FileSystemStorage()
            img_name = 'uploads/profile_pictures/user_{0}'.format(user_id)
            if fs_handle.exists(img_name):
                fs_handle.delete(img_name)
            fs_handle.save(img_name, user_img)
            user_profile_obj.profile_pic = img_name

        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        address = request.POST["address"]

        user_profile_obj.phone = phone
        user_profile_obj.address = address
        user_profile_obj.save()
        
        user_obj.username =  username
        user_obj.email = email
        user_obj.save()
        user_obj.refresh_from_db()
        

        return render(request, "profile/user_profile.html", {'my_profile': user_profile_obj})

    return render(request, "profile/profile_update.html", {})


@login_required
def edit_admin(request, user_id):
    details = User.objects.get(id=user_id)
    details_profile = UserProfile.objects.get(user=user_id)
    return render(request, "admins_dashboard/admin_edit.html", {'details_profile': details_profile, 'details': details})
    

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
            details_profile.profile_pic = img_name

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
        
        messages.success(request, username + "'s profile details have been updated")
        return redirect('admins')
        

    return render(request, "admins_dashboard/admin_edit.html", {})


@login_required
def delete_admin(request, user_id):
    data_to_delete = User.objects.filter(id=user_id).delete()
    messages.success(request, "The admin's record was successfully deleted")
    return redirect('admins')


def batch_delete_admins(request):
    # Get the list of selected records
    selected_records = request.POST.getlist('select_delete')

    # Convert the list of strings to a list of integers
    selected_records = [int(i) for i in selected_records]

    # Filter the records using the `id__in` lookup and delete them
    User.objects.filter(id__in=selected_records).delete()

    # Redirect to the success page
    messages.success(request, "The selected record(s) were successfully deleted from the database")
    return redirect('admins')


@login_required
def get_clients(request):
    all_clients = User.objects.filter(is_superuser=False, is_staff=False).order_by('date_joined').reverse()
    all_clients_profiles = UserProfile.objects.all
    return render(request, 'admins_dashboard/clients.html', {'clients': all_clients, 'client_profiles': all_clients_profiles})


@login_required
def create_client(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if username == "" or email == "" or firstname == "" or lastname == "" or password == "":
            messages.success(request, "Please complete all input fields")
            return render(request, "authentication/create_client.html")

        if username != "" or email != "":
            if len(username) < 8:
                messages.success(request, "Username must not be less than 8 characters")
                return render(request, "authentication/create_client.html")

            if User.objects.filter(username=username).exists():
                messages.success(request, "Username already exists")
                return render(request, "authentication/create_client.html")

            # The email inputs needs to be validated as well
            if User.objects.filter(email=email).exists():
                messages.success(request, "Email already exists")
                return render(request, "authentication/create_client.html")   

        if not password == confirm_password:
            messages.success(request, "Your passwords did not match")
            return render(request, "authentication/create_client.html")

        user = User.objects.create_user(username, email, password)
        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.username = username
        user.save()
        messages.success(request, "The client's account was successfully created")
        return redirect('all_clients')

    return render(request, "authentication/create_client.html")


@login_required
def edit_client(request, user_id):
    details = User.objects.get(id=user_id)
    details_profile = UserProfile.objects.get(user=user_id)
    return render(request, "admins_dashboard/client_edit.html", {'details_profile': details_profile, 'details': details})


@login_required
def client_edited(request, user_id):
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
            details_profile.profile_pic = img_name

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
        
        messages.success(request, username + "'s profile details has been updated")
        return redirect('all_clients')
        

    return render(request, "admins_dashboard/client_edit.html", {})


@login_required
def delete_client(request, user_id):
    data_to_delete = User.objects.filter(id=user_id).delete()
    messages.success(request, "The client's record was successfully deleted")
    return redirect('all_clients')


def batch_delete_clients(request):
    # Get the list of selected records
    selected_records = request.POST.getlist('select_delete')

    # Convert the list of strings to a list of integers
    selected_records = [int(i) for i in selected_records]

    # Filter the records using the `id__in` lookup and delete them
    User.objects.filter(id__in=selected_records).delete()

    # Redirect to the success page
    messages.success(request, "The selected record(s) were successfully deleted from the database")
    return redirect('all_clients')


@login_required
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
        messages.success(request, "Details was successfully captured")
        return redirect('debtors')

    all_clients = User.objects.filter(Q(is_superuser=False) & Q(is_staff=False))
    # all_clients = User.objects.filter(is_superuser=False, is_staff=False)
    return render(request, "debtors/create_debtor.html", {'clients': all_clients})


@login_required
def edit_debtor(request, user_id):
    details = Debtor.objects.get(id=user_id)
    return render(request, "debtors/debtor_edit.html", {'details': details})


@login_required
def debtor_edited(request, user_id):
    if request.method == 'POST':
        details = Debtor.objects.get(id=user_id)

        firstname = request.POST["firstname"]
        surname = request.POST["surname"]
        email = request.POST["email"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        amount_owed = request.POST["amount_owed"]
        
        details.firstname =  firstname
        details.surname =  surname
        details.email = email
        details.address =  address
        details.phone =  phone
        details.amount_owed =  amount_owed
        details.save()
        # details.refresh_from_db()
        
        messages.success(request, "Details successfully updated")
        return redirect('debtors')
        

    return render(request, "debtors/debtor_edit.html", {})


def debtors_bulk_actions(request):
    if request.method == 'POST':
        action = request.POST["action"]

        if action == "send_notification":
            
            return redirect('multiple_recipients')
            # selected_user_ids = request.POST.getlist('selected_users')

            # debtors = Debtor.objects.filter(id__in=selected_user_ids)

            # emails = [debtor.email for debtor in debtors]
            
            # return render(request, "admins_dashboard/email_notifications/multiple_recipient.html", {'emails': emails})
                

        elif action == "delete":
            # Get the list of selected records
            selected_records = request.POST.getlist('selected_users')

            # Convert the list of strings to a list of integers
            selected_records = [int(i) for i in selected_records]

            # Filter the records using the `id__in` lookup and delete them
            Debtor.objects.filter(id__in=selected_records).delete()

            # Redirect to the success page
            messages.success(request, "The selected record(s) were successfully deleted from the database")
            return redirect('debtors')

    all_debtors = Debtor.objects.all
    all_clients = User.objects.filter(is_superuser=False, is_staff=False)
    return render(request, 'debtors/debtors.html', {'debtors': all_debtors, 'clients': all_clients})
   

@login_required
def payments(request):
    all_payments = Payment.objects.all().order_by('date_payed').reverse()
    all_debtors = Debtor.objects.all
    return render(request, 'payments/payments.html', {'payments': all_payments, 'debtors': all_debtors})

@login_required
def create_payment(request):
    if request.method == "POST":
        amount_payed = request.POST["amount_payed"]
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

@login_required
def approve_payment(request, user_id):
    payment = Payment.objects.get(id=user_id)
    payment.status = "Completed"
    payment.save()
    messages.success(request, "Payment was successfully approved")
    return redirect('payments')


def payments_bulk_actions(request):
    if request.method == 'POST':
        action = request.POST["action"]

        if action == "manage":
            selected_user_ids = request.POST.getlist('selected_users')

            debtors = Debtor.objects.filter(id__in=selected_user_ids)

            phone_numbers = [debtor.phone for debtor in debtors]
            
            return render(request, "debtors/compose_sm.html", {'phone_numbers': phone_numbers})

        elif action == "delete":
            # Get the list of selected records
            selected_records = request.POST.getlist('selected_users')

            # Convert the list of strings to a list of integers
            selected_records = [int(i) for i in selected_records]

            # Filter the records using the `id__in` lookup and delete them
            Payment.objects.filter(id__in=selected_records).delete()

            # Redirect to the success page
            messages.success(request, "The selected record(s) were successfully deleted from the database")
            return redirect('payments')

    all_debtors = Debtor.objects.all
    return render(request, "payments/create_payment.html", {'debtors': all_debtors})


@login_required
def analytics(request):
    payments = Payment.objects.all()
    all_clients = User.objects.filter(is_superuser=False, is_staff=False)
    context = {
        'payments': payments,
        'all_clients': all_clients
    }
    return render(request, 'admins_dashboard/analytics.html', context)


# Sending email notification to debtors
@login_required
def single_recipient(request, user_id):
    debtor = Debtor.objects.get(id=user_id)
    return render(request, 'admins_dashboard/email_notifications/single_recipient.html', {'debtor': debtor})


@login_required
def single_recipient_send_mail(request):
    if request.method == 'POST':
        email = request.POST["email"]
        email_subject = request.POST["email_subject"]
        email_message = request.POST["email_message"]
        attachment = request.FILES.get('email_file')
        content_type = attachment.content_type if attachment else None

        # validate form data
        if not email or not email_subject or not email_message:
            return HttpResponseBadRequest('Missing required fields')

        # create email message
        email_msg = MIMEMultipart()
        email_msg['Subject'] = email_subject
        email_msg['To'] = email
        email_msg.attach(MIMEText(email_message))

        # add attachment, if provided
        if attachment:
            file_data = attachment.read()
            if content_type.startswith('image/'):
                image = MIMEImage(file_data)
                image.add_header('Content-Disposition', 'attachment', filename='image.jpg')
                email_msg.attach(image)
            elif content_type == 'application/pdf':
                attachment_msg = MIMEApplication(file_data, _subtype='pdf')
                attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.pdf')
                email_msg.attach(attachment_msg)
            elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                attachment_msg = MIMEApplication(file_data, _subtype='docx')
                attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.docx')
                email_msg.attach(attachment_msg)
            else:
                return HttpResponseBadRequest('Unsupported file type')

        # send email
        email_sender = 'nsikanadaowo90@gmail.com'
        email_password = 'jduzadsuapibwahj'
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(email_msg)

        messages.success(request, "Email notification was successfully sent")
        return redirect('debtors')


@login_required
def multiple_recipients(request):
    selected_user_ids = request.POST.getlist('selected_users')

    debtors = Debtor.objects.all()

    emails = [debtor.email for debtor in debtors]
            
    return render(request, "admins_dashboard/email_notifications/multiple_recipient.html", {'emails': emails})
        
    # return render(request, "admins_dashboard/email_notifications/multiple_recipient.html")


@login_required
def multiple_recipient_send_mail(request):
    if request.method == 'POST':
        email_subject = request.POST["email_subject"]
        email_message = request.POST["email_message"]
        attachment = request.FILES.get('email_file')
        content_type = attachment.content_type if attachment else None

        # validate form data
        if not email_subject or not email_message:
            return HttpResponseBadRequest('Missing required fields')

        # create email message
        email_sender = 'nsikanadaowo90@gmail.com'
        email_password = 'jduzadsuapibwahj'
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)

            # get all debtors
            debtors = Debtor.objects.all()
            for debtor in debtors:
                email = debtor.email
                if email:
                    # create a new email_msg object for each debtor
                    email_msg = MIMEMultipart()
                    email_msg['Subject'] = email_subject
                    email_msg['To'] = email
                    email_msg.attach(MIMEText(email_message))

                    # add attachment, if provided
                    if attachment:
                        file_data = attachment.read()
                        if content_type.startswith('image/'):
                            image = MIMEImage(file_data)
                            image.add_header('Content-Disposition', 'attachment', filename='image.jpg')
                            email_msg.attach(image)
                        elif content_type == 'application/pdf':
                            attachment_msg = MIMEApplication(file_data, _subtype='pdf')
                            attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.pdf')
                            email_msg.attach(attachment_msg)
                        elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                            attachment_msg = MIMEApplication(file_data, _subtype='docx')
                            attachment_msg.add_header('Content-Disposition', 'attachment', filename='document.docx')
                            email_msg.attach(attachment_msg)
                        else:
                            return HttpResponseBadRequest('Unsupported file type')
                            
                    # send email to current debtor
                    smtp.send_message(email_msg)
                    
                    # reset attachment for the next email
                    attachment.seek(0)

        messages.success(request, "Your email was sent")
        return redirect('debtors')

# View functions for the client dashboard
@login_required
def my_debtors(request, user_id):
    my_debtors = Debtor.objects.filter(client_id=user_id)
    return render(request, 'clients_dashboard/my_debtors.html', {'debtors': my_debtors})


@login_required
def my_payments(request, user_id):
    my_payments = Payment.objects.filter(client_id=user_id)
    my_debtors = Debtor.objects.filter(client_id=user_id)
    return render(request, 'clients_dashboard/my_payments.html', {'payments': my_payments, 'debtors': my_debtors})


@login_required
def my_analytics(request, user_id):
    my_payments = Payment.objects.filter(client_id=user_id)
    context = {
        'payments': my_payments,
    }
    return render(request, 'clients_dashboard/my_analytics.html', context)



