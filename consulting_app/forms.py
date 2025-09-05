from django import forms
from .models import Product, CompanyType,Module
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from django.core.exceptions import ValidationError

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
    branches = forms.CharField(
    required=False,
    widget=forms.Textarea(attrs={
        'placeholder': 'Enter  your company branch locations separated by commas',
        'rows': 1,
        'cols': 1,
    })
)

    location = forms.CharField(
        max_length=100,
        label="Location",
        widget=forms.TextInput(attrs={'placeholder': 'Company Location'})
    )
    type = forms.ModelChoiceField(
        queryset=CompanyType.objects.all(),
        label="Company Type",
        widget=forms.Select(attrs={'id': 'id_type'}),
        required=False,
        empty_label="Select Company Type"
    )
    type_other = forms.CharField(
        max_length=100,
        label="Other Company Type",
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Please specify Other Company Type',
            'id': 'id_type_other'
        })
    )

    Employees_no = forms.IntegerField(
        label="Number of Employees",
        widget=forms.NumberInput(attrs={'placeholder': 'Number of Employees e.g. 50'})
    )
    turnover = forms.IntegerField(
        label="Turnover (in Crore)",
        widget=forms.NumberInput(attrs={'placeholder': 'Turnover (in Crore) e.g. 20'})
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

    EXISTING_APPLI_CHOICES = [
        ('', 'Please select Existing Application'),
        ('Acumatica', 'Acumatica'),
        ('ERPNext', 'ERPNext'),
        ('Epicor', 'Epicor'),
        ('IFS Applications', 'IFS Applications'),
        ('Infor CloudSuite', 'Infor CloudSuite'),
        ('Microsoft Dynamics 365', 'Microsoft Dynamics 365'),
        ('Oracle NetSuite', 'Oracle NetSuite'),
        ('Odoo', 'Odoo'),
        ('SAP S/4HANA', 'SAP S/4HANA'),
        ('SYSPRO', 'SYSPRO'),
        ('Tally', 'Tally'),
        ('Other', 'Other'),
    ]
    existing_appli = forms.ChoiceField(
        choices=EXISTING_APPLI_CHOICES,
        label="Existing Applications",
        widget=forms.Select(attrs={'id': 'id_existing_appli'}),
        required=True,
    )
    existing_appli_other = forms.CharField(
        max_length=100,
        label="Other Application",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Please specify Other Application',
                                      'id': 'id_existing_appli_other'})
    )

    no_of_users = forms.IntegerField(
        label="Number of Users",
        widget=forms.NumberInput(attrs={'placeholder': 'Number of Users e.g. 5,10,15,20'})
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product",
        widget=forms.Select(attrs={'id': 'id_product'}),
        empty_label="Select Product Type"
    )
    
    module = forms.ModelMultipleChoiceField(
        queryset=Module.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2-multi', 'id': 'id_module'}),
        required=False
    )
    
    TIMELINE_CHOICES = [
    ('', 'Fix Demo Date'),
    ('15 Days', '15 Days'),
    ('30 Days', '30 Days'),
    ('45 Days', '45 Days'),
    ]
    timeline = forms.ChoiceField(
    choices=TIMELINE_CHOICES,
    label="Timeline",
    widget=forms.Select(attrs={'placeholder': 'Number of Users e.g. 10'}),
    required=True,
    )

    demo_date = forms.DateField(
    label="Preferred Demo Date",
    widget=forms.DateInput(
        attrs={
            'type': 'text',             # Must be 'text' for Flatpickr
            'id': 'id_demo_date',       # Must match JS selector
            'placeholder': 'Select a Date for Demo'
        }
    ),
    required=False
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
        allowed_domains = ['gmail.com']
        domain = email.split('@')[-1]
        if domain not in allowed_domains:
            raise forms.ValidationError("Please use your company email address.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()

        # Validate Company Type or Other
        type_selected = cleaned_data.get('type')
        type_other = cleaned_data.get('type_other')
        if not type_selected and not type_other:
            raise forms.ValidationError("Please select a Company Type or specify in 'Other Company Type'.")

        # Validate Existing Application or Other
        existing_appli = cleaned_data.get('existing_appli')
        existing_appli_other = cleaned_data.get('existing_appli_other')
        if existing_appli == 'Other' and not existing_appli_other:
            self.add_error('existing_appli_other', "Please specify the other application.")

        return cleaned_data
    def clean_no_of_users(self):
        no_of_users = self.cleaned_data.get('no_of_users')
        if no_of_users is None:
            return no_of_users
        if no_of_users % 5 != 0:
            raise ValidationError("Please enter a number divisible by 5.")
        return no_of_users
