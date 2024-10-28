from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from transactions.models import Transaction
from .forms import DepositForm,ReviewForm
from django.shortcuts import render, redirect, get_object_or_404
from Book.models import BOOK
from django.core.mail import EmailMessage, EmailMultiAlternatives

from django.template.loader import render_to_string

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class DepositMoneyView(LoginRequiredMixin, CreateView):
    template_name = 'deposit_form.html'
    model = Transaction
    form_class = DepositForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount, "Deposite Message", "deposit_mail.html")
        return super().form_valid(form)
    

def add_review(request, book_id):
    book = get_object_or_404(BOOK, id=book_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('book_detail', pk=book.id)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form, 'book': book})