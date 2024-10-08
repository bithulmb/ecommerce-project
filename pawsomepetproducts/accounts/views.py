import time

import requests
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from cart.models import Cart, CartItem
from cart.views import _cart_id

from .decorators import superuser_required
from .forms import (AddAddressForm, CustomUserUpdateForm, LoginForm,
                    OTPVerificationForm, RegisterForm, UserProfileForm)
from .models import Address, CustomUser, MobileOTP
from .utils import generate_otp, send_otp_email, send_otp_mobile

# Create your views here.


# Admin Side views
# -------------------------Admin side views----------------------------------


# view function for listing the users in admin panel
@never_cache
@superuser_required
def admin_users_view(request):
    query = request.GET.get("q")
    if query:  # if there is search query
        users = CustomUser.objects.filter(is_superadmin=False).filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
        )
    else:
        users = CustomUser.objects.filter(is_superadmin=False).order_by("-id")

    # for including paginator
    paginator = Paginator(users, 8)
    page = request.GET.get("page")

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, "admin/admin_users.html", {"users": users})


@superuser_required
@never_cache
def admin_edit_user_view(request, pk):
    object = CustomUser.objects.get(id=pk)
    if request.method == "POST":
        form = CustomUserUpdateForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.success(request, "User status updated succesfully")
            return redirect("admin_users")
    else:
        form = CustomUserUpdateForm(instance=object)
    return render(request, "admin/admin_edit_user.html", {"form": form})


# User side views


# -------------------------User side views----------------------------------
@never_cache
def login_view(request):

    # if already loggedin redirect to home
    if request.user.is_authenticated:
        return redirect("home_page")

    # Getting the details for signing in
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:

                if not user.is_blocked:

                    # checking whether there are any items in cart in current session
                    try:
                        cart = Cart.objects.get(cart_id=_cart_id(request))
                        is_cart_item_exists = CartItem.objects.filter(
                            cart=cart
                        ).exists()
                        if is_cart_item_exists:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

                    except:
                        pass

                    login(request, user)

                    # for redirecting to the url mentioned in next while logging in
                    url = request.META.get("HTTP_REFERER")
                    try:
                        query = requests.utils.urlparse(url).query
                        params = dict(x.split("=") for x in query.split("&"))
                        if "next" in params:
                            nextPage = params["next"]
                            return redirect(nextPage)
                    except:
                        pass

                    return redirect("home_page")
                else:
                    messages.error(
                        request,
                        "Your account has been blocked. Please contact the admin",
                    )
                    return redirect("login_page")
            else:
                messages.error(request, "Invalid Credentials. Try Again")
                return redirect("login_page")
        else:

            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, "user_home/login.html", {"form": form})


@never_cache
def signup_view(request):
    # if already loggedin redirect to home
    if request.user.is_authenticated:
        return redirect("home_page")

    # if request is POST check for form validation, send the otp and redirect to otp verification page
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data  # saving the validated form data dictionary
            otp = generate_otp()
            otp_created_at = int(time.time())  # Current timestamp
            print(otp)
            send_otp_email(user_data["email"], otp)
            messages.success(
                request,
                "Check your mail and enter the otp for continuing registration ",
            )

            # Store user data and OTP in session
            request.session["user_data"] = {
                "first_name": user_data["first_name"],
                "last_name": user_data["last_name"],
                "email": user_data["email"],
                "phone_number": user_data["phone_number"],
                "password": user_data["password1"],
            }

            request.session["otp"] = otp
            request.session["otp_created_at"] = otp_created_at

            return redirect("verify_otp")
        else:
            return render(request, "user_home/signup.html", {"form": form})

    else:
        # if request is get render the registration form
        form = RegisterForm()
        return render(request, "user_home/signup.html", {"form": form})


# view function for verifying the otp and saving the details of user to database
@never_cache
def verify_otp_view(request):
    if request.method == "POST":
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            user_otp = form.cleaned_data["otp"]
            stored_otp = request.session.get("otp")
            otp_created_at = request.session.get("otp_created_at", 0)

            # if otp is expired (after 3 minutes) send error message
            if int(time.time()) - otp_created_at > 180:  # (180 seconds)
                form.add_error("otp", "OTP has expired. Please request a new one.")
                return render(
                    request,
                    "user_home/verify_otp.html",
                    {"form": form, "otp_expired": True},
                )

            if int(user_otp) == stored_otp:

                # OTP is correct, proceed with registration
                user_data = request.session.get("user_data")

                try:
                    user = CustomUser.objects.create_user(
                        first_name=user_data["first_name"],
                        last_name=user_data["last_name"],
                        email=user_data["email"],
                        phone_number=user_data["phone_number"],
                        password=user_data["password"],
                    )

                    # Clear session data
                    del request.session["user_data"]
                    del request.session["otp"]

                    messages.success(
                        request, "Account created succesfully. Please login to continue"
                    )
                    return redirect("login_page")

                except Exception as e:

                    form.add_error(None, str(e))

            else:
                form.add_error("otp", "Invalid OTP")
    else:
        form = OTPVerificationForm()
    return render(request, "user_home/verify_otp.html", {"form": form})


# view function for sending the otp again
@never_cache
def resend_otp_view(request):
    user_data = request.session.get("user_data")
    if user_data:  # verify whether the session data is available
        otp = generate_otp()
        otp_created_at = int(time.time())
        print(otp)

        send_otp_email(
            user_data["email"], otp
        )  # generate and send a new otp to user email

        request.session["otp"] = otp
        request.session["otp_created_at"] = (
            otp_created_at  # stores new otp and otp creation time in session
        )

        messages.success(request, "A new OTP has been sent to your email.")
    else:
        messages.error(
            request, "User data not found. Please start the registration process again."
        )

    return redirect("verify_otp")


# view function for logging out user
@never_cache
def logout_view(request):
    logout(request)
    return redirect("home_page")


# view for displaying user profile
@login_required(login_url="login_page")
@never_cache
def user_profile_view(request):
    object = CustomUser.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.success(request, "User profile Updated succesfully")
            return redirect("user_profile")
    else:
        form = UserProfileForm(instance=object)
    return render(request, "user_home/user_profile.html", {"form": form})


# view for changing password of the user in profile section
@login_required(login_url="login_page")
@never_cache
def user_change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            messages.success(request, "Your Password has been Changed Succesfully")
            return redirect("change_password")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "user_home/change_password.html", {"form": form})


# view for adding new adress for user
@login_required(login_url="login_page")
@never_cache
def user_add_address_view(request):
    if request.method == "POST":
        form = AddAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)  # temporarly saves the form
            address.user = request.user
            address.save()  # adds the id of user and saves the address
            messages.success(request, "Address added successfully!")
            return redirect("user_addresses")
    else:
        form = AddAddressForm()
    return render(request, "user_home/add_address.html", {"form": form})


# view function for listing addresses of user
@login_required(login_url="login_page")
@never_cache
def user_addresses_view(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "user_home/user_addresses.html", {"addresses": addresses})


# view function for changing the default address when set default address button is pressed
@login_required(login_url="login_page")
@csrf_exempt  # The decorator marks a view as being exempt from the protection ensured by the middleware
def user_set_default_address_view(request):
    if request.method == "POST":
        address_id = request.POST.get("address_id")
        user = request.user

        # Reset all addresses to non-default
        Address.objects.filter(user=user, is_default=True).update(is_default=False)

        # Set the selected address as default
        Address.objects.filter(id=address_id, user=user).update(is_default=True)

        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)


# view function for editing address of user
@login_required(login_url="login_page")
@never_cache
def user_edit_address_view(request, pk):
    object = get_object_or_404(Address, id=pk)
    if request.method == "POST":
        form = AddAddressForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            messages.success(request, "User Address Updated Succesfully")
            return redirect("user_addresses")
    else:
        form = AddAddressForm(instance=object)
    return render(request, "user_home/edit_address.html", {"form": form})


# view function for deleting address of user
@login_required(login_url="login_page")
@never_cache
def user_delete_address_view(request, pk):
    object = get_object_or_404(Address, id=pk)
    if request.method == "POST":
        object.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect("user_addresses")
    return render(request, "user_home/confirm_delete_address.html", {"address": object})


# view function for requesting otp for mobile verification
@login_required(login_url="login_page")
def request_mobile_otp_view(request):
    if request.method == "POST":
        mobile_number = request.POST.get("mobile_number")
        otp = str(generate_otp())

        # Save OTP to database
        otp_record = MobileOTP.objects.create(
            user=request.user, otp=otp, mobile_number=mobile_number
        )

        # Send OTP via SMS
        send_otp_mobile(str(mobile_number), otp)
        print("2")

        messages.success(request, "OTP has been sent to your mobile number.")
        return redirect("verify_mobile_otp")

    return render(request, "user_home/request_mobile_otp.html")


# view function for verifying otp for mobile verification
@login_required(login_url="login_page")
def verify_mobile_otp_view(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        try:
            otp_record = MobileOTP.objects.get(
                user=request.user, otp=entered_otp, is_verified=False
            )
            otp_record.is_verified = True
            otp_record.save()
            messages.success(request, "Mobile number verified successfully!")
            return redirect("request_mobile_otp")
        except MobileOTP.DoesNotExist:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "user_home/verify_mobile_otp.html")
