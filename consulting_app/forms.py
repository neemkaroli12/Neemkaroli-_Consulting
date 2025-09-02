from django import forms
from .models import Estimate
class CareerApplicationForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'placeholder': 'Write a short message...'}), required=False)
    resume = forms.FileField(label="Upload Resume", required=False)


class estimateForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
   