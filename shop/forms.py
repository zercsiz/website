from django import forms
from . import models
from django.utils.translation import gettext_lazy as _


class TransactionInfoForm(forms.ModelForm):

    class Meta:

        model = models.Transaction
        fields = ('date', 'hour', 'minute', 'card4Digits', 'transactionId', 'amount')

        labels = {
            'date': _('تاریخ پرداخت'),
            'hour': _('ساعت'),
            'minute': _('دقیقه'),
            'card4Digits': _('چهار رقم پایانی کارت پرداخت کننده'),
            'transactionId': _('شماره پیگیری یا کد رسید'),
            'amount': _('مبلغ پرداخت شده'),
        }
        widgets = {
            'date': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'hour': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'minute': forms.EmailInput(attrs={'class': 'form-control my-3'}),
            'card4Digits': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'transactionId': forms.TextInput(attrs={'class': 'form-control my-3'}),
            'amount': forms.Select(attrs={'class': 'form-control my-3'}),
        }