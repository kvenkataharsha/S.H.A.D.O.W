from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as log
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from blog.models import Post
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from .forms import *
from .models import *


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been successfully created')
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            log(request, new_user)
            return render(request, 'users/profile_complete.html')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def after_login(request):
    try:
        if request.user.authority.profile_complete:
            return redirect('blog-home')  # dashboard
    except:
        pass
    try:
        if request.user.anonymous.profile_complete:
            return redirect('blog-home')  # dashboard
    except:
        pass
    try:
        if request.user.journalist.profile_complete:
            return redirect('blog-home')  # dashboard
    except:
        pass
    return redirect('profile_page')  # profile complete page





def profile_page(request):
    if request.method == 'POST':
        role = request.POST.get('profile', '')
        if (role == "authority"):
            current_site = get_current_site(request)
            mail = request.POST['email']
            authority = Authority()
            authority.user = request.user
            user = authority.user
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            send_mail(mail_subject, message, 'shadowiiits2@gmail.com', [mail])
            return render(request, 'email_confirmation.html')

        elif (role == "journalist"):
            current_site = get_current_site(request)
            mail = request.POST['email']
            journalist = Journalist()
            journalist.user = request.user
            user = journalist.user
            user.save()
            mail_subject = 'Activate your account.'
            message = render_to_string('acc_activate_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            send_mail(mail_subject, message, 'shadowiiits2@gmail.com', [mail])
            return render(request, 'email_confirmation.html')
        else :
            anonymus = Anonymous()
            anonymus.user = request.user
            anonymus.profile_complete = True
            anonymus.save()
            return redirect('blog-home')
    return render(request, 'users/profile_complete.html', )



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        authority = Authority()
        authority.user = request.user
        journalist = Journalist()
        journalist.user = request.user
        user = authority.user or journalist.user
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        authority.profile_complete = True
        authority.save()
        journalist.profile_complete = True
        journalist.save()
        log(request, user)

        return redirect('blog-home')

    else:
        return HttpResponse('Activation link is invalid!')
            


def login(request):
    form = UserCreationForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your profile has been updated!')
            return redirect('profile')

    else:
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile)

    user_posts = Post.objects.filter(
        author=request.user).order_by('-date_posted')

    context = {
        'p_form': p_form,
        'user_posts': user_posts
    }
    return render(request, 'users/profile.html', context)


# Create your views here.
