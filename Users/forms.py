from django import forms
from django.contrib.auth.models import User




class CustomerForm(forms.Form):
    first_name = forms.CharField(max_length=200,       
                             label=False,
                             widget=forms.TextInput(
                               attrs={'id':'first_name',
                                      'class': '',
                                      'placeholder':'First Name'}))
    last_name = forms.CharField(max_length=200,       
                             label=False,
                             widget=forms.TextInput(
                               attrs={'id':'last_name',
                                      'class': '',
                                      'placeholder':'Last Name'}))
    username = forms.CharField(max_length=20,       
                             label=False,
                             widget=forms.TextInput(
                               attrs={'id':'username',
                                      'class': '',
                                      'placeholder':'Username'}))
    email    = forms.EmailField(max_length=250,
                                label =False,
                                widget=forms.EmailInput(
                                      attrs={'id':'email',
                                            'class': '',
                                            'placeholder':'E-mail'}))

    password = forms.CharField(max_length=30,
                               label=False,
                               widget=forms.PasswordInput(
                                      attrs={'id':'password',
                                            'placeholder':'Enter password',
                                            'class':''}))
    password2 = forms.CharField(max_length=30,
                               label=False,
                               widget=forms.PasswordInput(
                                      attrs={'id':'password2',
                                            'placeholder':'Repeat password',
                                            'class':''}))

    def clean_email(self):
        # cd == Cleaned_data
        cd = self.cleaned_data.get('email')
        cd = cd.lower()
        user = User.objects.filter(email=cd).exists()
        if user:
            raise forms.ValidationError('This e-mail address is already registered to another account')
        return cd



    def clean_username(self):
        cd = self.cleaned_data.get('username')
        cd = cd.lower()
        if len(cd) < 6:
            raise forms.ValidationError("Username must contain up to 6 characters")
        if ' ' in cd:
            raise forms.ValidationError("A blank space can not be included as part of username")
        user = User.objects.filter(username=cd).exists()
        if user:
            raise forms.ValidationError('Username is already taken. Please choose another username')
        return cd

  

    def clean(self):
        cleaned_data = super(CustomerForm, self).clean()
        first_password = self.cleaned_data.get('password')
        second_password = self.cleaned_data.get('password2')
        if first_password != second_password:
            self.add_error('password',"Passwords did not match")
        return cleaned_data



class SignInForm(forms.Form):
    
    email    = forms.EmailField(max_length=250,
                                label =False,
                                widget=forms.EmailInput(
                                      attrs={'id':'email',
                                            'class': '',
                                            'placeholder':'E-mail'}))
    password = forms.CharField(max_length=30,
                               label=False,
                               widget=forms.PasswordInput(
                                      attrs={'id':'password',
                                            'placeholder':'Enter password',
                                            'class':''}))
    def __init__(self,*args,**kwargs):
        super(SignInForm,self).__init__(*args,**kwargs)

    def clean_email(self):
        # cd == Cleaned_data
        cd = self.cleaned_data.get('email')
        cd = cd.lower()
        user = User.objects.filter(email=cd).exists()
        if not user:
            raise forms.ValidationError('Email address and password did not match')
        return cd
    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        return cleaned_data
  

   