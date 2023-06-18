
# Create your views here.
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm
from .tasks import send_verification_email  
from .utils import generate_token, generate_link, decode_token
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
            # send_verification_email.delay(user.email, 'Account Verification' ,verification_link) #TODO Schedule the email sending task asynchronously
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