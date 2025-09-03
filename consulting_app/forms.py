from django import forms
from .models import Product, CompanyType
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

class CareerApplicationForm(forms.Form):
    name = forms.CharField(max_length=100, label="Full Name", widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(label="Email Address", widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={'placeholder': 'Write a short message...'}), required=False)
    resume = forms.FileField(label="Upload Resume", required=False)


class EstimateForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'})
    )
    company_name = forms.CharField(
        max_length=100,
        label="Company Name",
        widget=forms.TextInput(attrs={'placeholder': 'Company Name'})
    )
    location = forms.CharField(
        max_length=100,
        label="Location",
        widget=forms.TextInput(attrs={'placeholder': 'Company Location'})
    )

    type = forms.ModelChoiceField(
        queryset=CompanyType.objects.all(),
        label="Company Type",
        widget=forms.Select(attrs={'id': 'id_type'})
    )

    Employees_no = forms.IntegerField(
        label="Number of Employees",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 50'})
    )
    turnover = forms.IntegerField(
        label="Turnover (in Crore)",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 20'})
    )
    designation = forms.CharField(
        max_length=100,
        label="Designation",
        widget=forms.TextInput(attrs={'placeholder': 'Your Designation'})
    )
    mobile_no = forms.CharField(
        label="Mobile Number",
        widget=forms.TextInput(attrs={'placeholder': '10-digit mobile number'})
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )

    existing_appli = forms.CharField(
        max_length=200,
        label="Existing Applications",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Tally, SAP, etc.'})
    )

    no_of_users = forms.IntegerField(
        label="Number of Users",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 10'})
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product",
        widget=forms.Select(attrs={'id': 'id_product'})
    )

    module = forms.MultipleChoiceField(
        choices=[],  
        label="Modules",
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_module'})
    )
    
    branches = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={'placeholder': 'Enter branch locations separated by commas'})
    )
    
    def clean_mobile_no(self):
        mobile = self.cleaned_data['mobile_no']
        try:
            parsed_number = phonenumbers.parse(str(mobile), "IN")
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid mobile number.")
        except NumberParseException:
            raise forms.ValidationError("Invalid mobile number format.")
        return mobile

    def clean_email(self):
        email = self.cleaned_data.get('email')
        allowed_domains = ['company.com', 'example.org']
        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError("Please use your company email address.")
        return email
