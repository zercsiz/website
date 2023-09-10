from django import forms
from . import models


class TransactionInfoForm(forms.ModelForm):

    class Meta:

        model = models.Transaction
        fields = ('date', 'hour', 'minute', 'card4Digits', 'transactionId', 'amount')