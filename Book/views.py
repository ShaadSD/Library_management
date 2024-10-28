from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from .forms import RegisterForm
from django.utils import timezone
from transactions.views import send_transaction_email

from .models import BOOK,BorrowedBook
from django.contrib import messages
# Create your views here.
class RegisterView(FormView):
    template_name='register.html'
    form_class=RegisterForm
    success_url = reverse_lazy('register')

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        return super().form_valid(form)

class LoginView(LoginView):
    template_name='login.html'
    def get_success_url(self):
        return reverse_lazy('login')
    
def user_logout(request):
    logout(request)
    return redirect('login')

def borrow_book(request, pk):
    book = get_object_or_404(BOOK, pk=pk)
    account = request.user.account

    if book.quantity > 0 and account.balance >= book.Borrowing_Price:
        book.quantity -= 1
        book.save()
        account.balance -= book.Borrowing_Price
        account.save()

        borrowed_book, created = BorrowedBook.objects.get_or_create(
            user=request.user, book=book
        )
        if not created:
            borrowed_book.quantity += 1
        borrowed_book.borrow_date = timezone.now()
        borrowed_book.save()

        messages.success(request, f'You have successfully borrowed {book.Title}!')
        send_transaction_email(request.user, book, "Borrow Confirmation", "borrow_mail.html")
    elif book.quantity == 0:
        messages.error(request, 'Sorry, this book is out of stock.')
    else:
        messages.error(request, 'Insufficient balance to borrow this book.')

    return redirect('profile')
    