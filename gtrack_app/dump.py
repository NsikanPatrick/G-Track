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

