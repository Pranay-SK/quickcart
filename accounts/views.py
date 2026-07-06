from django.http import HttpResponse

from django.shortcuts import redirect, render

from .models import User

from .forms import UserForm

from django.contrib import messages
# Create your views here.

def registerUser(request):
    if request.method=='POST':
        form=UserForm(request.POST)
        if form.is_valid():
            #create the user using the form
            # password=form.cleaned_data.get('password')
            # user=form.save(commit=False)
            # user.set_password(password)
            # user.role=User.CUSTOMER
            # user.save()

            #create the user using create_user method

            first_name=form.cleaned_data.get('first_name')
            last_name=form.cleaned_data.get('last_name')
            username=form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=User.objects.create_user(first_name=first_name, last_name=last_name, username=username,email=email, password=password)
            user.role=User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully')

            return redirect('registerUser')
        else:
            print('Form is not valid')
            print(form.errors)
    else:
        form=UserForm()
    context={
        'form':form,
        }
    return render(request, 'accounts/registerUser.html', context)