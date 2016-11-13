# from django.forms import ModelForm
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# from django import forms
#
#
# #Sign up
# class RegistrationForm(ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     username = forms.CharField(required=True)
#
#     location = forms.ChoiceField(label='Your Location', required=True, choices=(
#         ('SA', 'South America'),
#         ('NA', 'North America'),
#         ('AS', 'Asia'),
#         ('EU', 'Europe'),
#         ('AU', 'Australia'),
#         ('AF', 'Africa')
#     ))
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email', 'password']
#
#     def clean(self):
#         cleaned_data = super(RegistrationForm, self).clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get('confirm_password')
#
#         if password != confirm_password:
#             msg = 'Password confirmation failed'
#             self._errors['confirm_password'] = self.error_class([msg])
#
#
#
# # Sign in
# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=150, required=True)
#     password = forms.CharField(widget=forms.PasswordInput, required=True)
#
#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         print user
#         if not user or not user.is_active:
#             raise forms.ValidationError("Incorrect credentials. Please try again.")
#         return self.cleaned_data
#
#     def auth(self, request):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#         user = authenticate(username=username, password=password)
#         return user