from django import forms 
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import BOOK
from acounts.models import UserAccount

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields= ['username','first_name','last_name','password1','password2','email']
    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save() 
            UserAccount.objects.create(
                user = our_user,
                account_no = 100000+ our_user.id
            )
        return our_user
      

