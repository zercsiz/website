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
            'date': forms.TextInput(attrs={'class': 'form-control my-3', 'required':'true'}),
            'hour': forms.TextInput(attrs={'class': 'form-control my-3', 'required':'true'}),
            'minute': forms.TextInput(attrs={'class': 'form-control my-3', 'required':'true'}),
            'card4Digits': forms.TextInput(attrs={'class': 'form-control my-3', 'required':'true'}),
            'transactionId': forms.TextInput(attrs={'class': 'form-control my-3', 'required':'true'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control my-3', 'required':'true'}),
        }