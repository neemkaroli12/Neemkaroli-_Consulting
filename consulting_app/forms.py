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
    branches = forms.CharField(
    required=False,
    widget=forms.Textarea(attrs={
        'placeholder': 'Enter branch locations separated by commas',
        'rows': 2,
        'cols': 10
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
            'placeholder': 'Please specify',
            'id': 'id_type_other'
        })
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

    EXISTING_APPLI_CHOICES = [
        ('', 'Please select'),
        ('Tally', 'Tally'),
        ('SAP', 'SAP'),
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
        widget=forms.TextInput(attrs={'placeholder': 'Please specify',
                                      'id': 'id_existing_appli_other'})
    )

    no_of_users = forms.IntegerField(
        label="Number of Users",
        widget=forms.NumberInput(attrs={'placeholder': 'e.g. 10'})
    )

    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Product",
        widget=forms.Select(attrs={'id': 'id_product'}),
        empty_label="Select Product Type"
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