# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site


from .forms import LoginForm, RegisterForm
from .tasks import send_email_func
from .utils import (
    generate_token,
    generate_link,
    decode_token,
    generate_password_reset_token,
)
from .models import User
from Log.models import Log


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "Auth/login.html", {"form": form})

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        # print(username, password, 'dtals')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_email_verified is False:
                return JsonResponse(
                    {"error": "Email is not verified.Please Verify Email"}, status=400
                )

            if user.is_approved is False:
                return JsonResponse(
                    {
                        "error": "Ouch 😮‍💨 Your Account is not Verified Yet.Please Contact Your Librarian 👨‍🏫"
                    },
                    status=400,
                )
                
            login(request, user)
            return JsonResponse({"success": True})  # Return success response
        else:
            return JsonResponse(
                {"error": "Invalid username or password"}, status=400
            )  # Return error response


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, "Auth/register.html", {"form": form})

    def post(self, request):
        try:
            # print(request.POST,"post-values")
            # form = RegisterForm(request.POST)

            username = request.POST["username"]
            email = request.POST["email"]

            # Check if username or email already exists
            if (
                User.objects.filter(username=username).exists()
                or User.objects.filter(email=email).exists()
            ):
                return JsonResponse(
                    {"error": "Username or Email already exists"}, status=400
                )

            user = User.objects.create(
                fullname=request.POST["fullname"],
                username=request.POST["username"],
                email=request.POST["email"],
            )
            user.set_password(request.POST["password1"])
            user.save(update_fields=["password"])
            # Generate verification token
            uid, token = generate_token(user)

            # Construct the verification URL
            verification_link = generate_link(request, uid, token)

            # print(verification_link, 'link')

            # Send verification email asynchronously
            send_email_func.delay(
                user.fullname,
                user.email,
                "Sta Archive Account Verification",
                verification_link,
                type_="verify",
                username=user.username
            )
            return JsonResponse(
                {
                    "success": "Registration Successful, Check Email to Verify \n check Spam Folder if you didnt find mail."
                },
                status=200,
            )  # Return sucess response
            # else:
            #     print(form,"form")
            #     return JsonResponse({'error': f'Error Encountered, Please check your Details again'}, status=400)  # Return error response
        except Exception as error_message:
            Log.objects.create(GeneratedBy="RegisterView", ExceptionMessage=error_message)
            return JsonResponse(
                {
                    "error": "An error Occurred which has been logged , We are sorry and would fix immediately, Try Again Later"
                },
                status=400,
            )  # Return error response


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        admin_site = f"{get_current_site(request)}/admin/Authentication/user/"
        try:
            user, token_generator = decode_token(uidb64)
            print(user,token_generator,uidb64)
            if token_generator.check_token(user, token):
                user.is_email_verified = True
                user.save()
                
                # Send verification email asynchronously
                send_email_func.delay(
                    user.fullname,
                    None,
                    "Sta Archive Account Verification",
                    admin_site,
                    type_="approve",
                    username=user.username
                )
                return render(request, "Auth/verification_sucess.html")
            else:
                return render(request, "Auth/verification_error.html")
        except (TypeError, ValueError, OverflowError, Exception):
            return render(request, "Auth/verification_error.html")


class ForgotPasswordView(View):
    def get(self, request):
        return render(request, "Auth/forgot_password.html")

    def post(self, request):
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)

            token, expiration_time, reset_url = generate_password_reset_token(
                request, user
            )

            # Save the token in the user's reset_token field
            user.reset_token = token
            user.reset_token_expiration = expiration_time
            user.save()

            # Send the password reset email
            message = f"Hello {user.fullname},\n\nTo reset your password, click on the following link:\n\n{reset_url}\n\nIf you did not request a password reset, please ignore this email.\n\nBest regards,\nStat-Archive Team"
            print("RESET password", message)
            send_email_func.delay(
                user.fullname,
                user.email,
                "Sta Archive Password Reset",
                reset_url,
                type_="reset",
                username=user.username
            )

            # Display a success message or redirect to a success page
            return JsonResponse(
                {
                    "success": "Password reset email sent. \n check Spam Folder if you didnt find mail."
                },
                status=200,
            )
        except User.DoesNotExist:
            # Display an error message if the email is not associated with any user account
            return JsonResponse(
                {"error": "The provided email does not exist in our records."},
                status=400,
            )


class ResetPasswordView(View):
    def get(self, request):
        token = request.GET.get("token")
        user = User.objects.filter(reset_token=token).first()
        # print('user', user)
        if user:
            # Check if the token is still valid (within the expiration time)
            if (
                user.reset_token_expiration
                and user.reset_token_expiration > timezone.now()
            ):
                # Render the password reset form
                return render(request, "Auth/reset_password.html")

        # Invalid token or expired, redirect to an error page or display an error message
        return render(request, "Auth/password_reset_error.html")

    def post(self, request):
        token = request.GET.get("token")
        user = User.objects.filter(reset_token=token).first()

        if user:
            # Check if the token is still valid (within the expiration time)
            if (
                user.reset_token_expiration
                and user.reset_token_expiration > timezone.now()
            ):
                # Update the user's password
                password = request.POST.get("password")
                user.set_password(password)
                user.reset_token = None
                user.reset_token_expiration = None
                user.save()
                # Redirect to a success page or display a success message
                return JsonResponse(
                    {"success": "Password reset successful."}, status=200
                )

        # Invalid token or expired, redirect to an error page or display an error message
        return render(request, "Auth/password_reset_error.html")
