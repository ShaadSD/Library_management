from django import forms
from .models import Transaction
from .models import Review
class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None) 
        super().__init__(*args, **kwargs) 

    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
        return amount

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance + self.cleaned_data['amount']
        return super().save(commit=commit)
    


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']