from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

# My form for creating and updating tasks
class TaskForm(forms.ModelForm):
  due_date = forms.DateField(
    widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
    input_formats=['%Y-%m-%d', '%d/%m/%Y'],
    required=False
  )

  class Meta:
    model = Task
    fields = ['title', 'description', 'due_date', 'status', 'priority', 'category']
    widgets = {
      'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
      'title': forms.TextInput(attrs={'class': 'form-control'}),
      'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
      'priority': forms.Select(attrs={'class': 'form-control'}),
      'category': forms.Select(attrs={'class': 'form-control'}),
    }

    # title is required
    def clean_title(self):
      title = self.cleaned_data.get['title']
      if not title:
        raise forms.ValidationError('Task title is required')
      return title

  # account creation form
class RegisterForm(UserCreationForm):
  email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs['class']='form-control'
    self.fields['password1'].widget.attrs['class']='form-control'
    self.fields['password2'].widget.attrs['class']='form-control'

# Edit profile
class EditProfileForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email']
    widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control'}),
      'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }

# Password change
"""class PasswordChangeForm(forms.Form):
      old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
      new_password1 = forms
      new_password2 = """