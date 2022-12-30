from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.core.files.storage import FileSystemStorage

# @login_required(login_url='login')
@login_required
def index(request):
    # return HttpResponse('Halo')
    return render(request, 'index.html', {})

@login_required
def admins(request):
    # superusers = User.objects.filter(is_superuser=True)

    # Get the currently logged in user
    current_user = request.user
     # Fetch all users from the database, excluding the currently logged in user since we
    #  only need the details of the other admins
    all_admins = User.objects.exclude(pk=current_user.pk)
    all_admins_profiles = UserProfile.objects.all
    return render(request, 'admins.html', {'admins': all_admins, 'admin_profiles': all_admins_profiles})

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
    return render(request, "admins/admin_edit.html", {'details_profile': details_profile, 'details': details})
    

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
        return render(request, "admins/admin_edit.html", {'details_profile': details_profile, 'details': details})
        

    return render(request, "admins/admin_edit.html", {})


@login_required
def delete_admin(request, user_id):
    data_to_delete = User.objects.filter(id=user_id).delete()
    messages.success(request, "The record was successfully deleted")
    return redirect('admins')


def batch_delete(request):
    # Get the list of selected records
    selected_records = request.POST.getlist('select_delete')

    # Convert the list of strings to a list of integers
    selected_records = [int(i) for i in selected_records]

    # Filter the records using the `id__in` lookup and delete them
    User.objects.filter(id__in=selected_records).delete()

    # Redirect to the success page
    messages.success(request, "The selected records were successfully deleted")
    return redirect('admins')

