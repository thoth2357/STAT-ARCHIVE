
# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.utils import timezone

from .forms import LoginForm, RegisterForm
from .tasks import send_email  
from .utils import generate_token, generate_link, decode_token, generate_password_reset_token
from .models import User

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active == False:
                return JsonResponse({'error': 'Email is not verified'}, status=400)
            else:
                login(request, user)
                return JsonResponse({'success': True})  # Return success response
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)  # Return error response
            

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'}, status=400)
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            user = form.save(commit=False)
            user.is_active = False  # Set the user as inactive until email verification
            user.save()

            # Generate verification token
            uid, token = generate_token(user)

            # Construct the verification URL
            verification_link = generate_link(request, uid, token)

            print(verification_link, 'link')
            
            # Send verification email asynchronously
            # send_email.delay(user.email, 'Account Verification' ,verification_link) #TODO Schedule the email sending task asynchronously
            return JsonResponse({'success': 'Registration Successful, Check Email to Verify'}, status=200)  # Return sucess response
        else:
            return JsonResponse({'error': f'Username or Email Already Exists'}, status=400)  # Return error response

class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            user,token_generator =  decode_token(uidb64)
            if token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return render(request, 'verification_sucess.html')
            else:
                return render(request, 'verification_error.html')  
        except (TypeError, ValueError, OverflowError, Exception):
            return render(request, 'verification_error.html')  
        
    
class ForgotPasswordView(View):
    def get(self, request):
        return render(request, 'forgot_password.html')

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            
            token,expiration_time,reset_url = generate_password_reset_token(request, user)
            
            # Save the token in the user's reset_token field
            user.reset_token = token
            user.reset_token_expiration = expiration_time
            user.save()

            # Send the password reset email
            message = f'Hello {user.fullname},\n\nTo reset your password, click on the following link:\n\n{reset_url}\n\nIf you did not request a password reset, please ignore this email.\n\nBest regards,\nStat-Archive Team'
            print("RESET password", message)
            # send_email.delay(user.email, 'Password Reset' ,message) #TODO Schedule the email sending task asynchronously
            
            # Display a success message or redirect to a success page
            return JsonResponse({'success': 'Password reset email sent.'}, status=200)
        except User.DoesNotExist:
            # Display an error message if the email is not associated with any user account
            return JsonResponse({'error': 'The provided email does not exist in our records.'}, status=400)

class ResetPasswordView(View):
    def get(self, request):
        token = request.GET.get('token')
        user = User.objects.filter(reset_token=token).first()
        print('user', user)
        if user:
            # Check if the token is still valid (within the expiration time)
            if user.reset_token_expiration and user.reset_token_expiration > timezone.now():
                # Render the password reset form
                return render(request, 'reset_password.html')
        
        # Invalid token or expired, redirect to an error page or display an error message
        return render(request, 'password_reset_error.html') 

    def post(self, request):
        token = request.GET.get('token')
        user = User.objects.filter(reset_token=token).first()

        if user:
            # Check if the token is still valid (within the expiration time)
            if user.reset_token_expiration and user.reset_token_expiration > timezone.now():
                # Update the user's password
                password = request.POST.get('password')
                user.set_password(password)
                user.reset_token = None
                user.reset_token_expiration = None
                user.save()
                # Redirect to a success page or display a success message
                return JsonResponse({'success': 'Password reset successful.'}, status=200)

        # Invalid token or expired, redirect to an error page or display an error message
        return render(request, 'password_reset_error.html') #TODO Create a password reset error page
