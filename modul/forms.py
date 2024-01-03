from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from modul.models.user import UserPelajaran
from modul.models.modul import Module
from django.forms import ModelForm, TextInput, FileInput, Select
from django.core.exceptions import ValidationError
from django.utils.text import slugify


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")
	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class FormKomentar(forms.Form):
	question = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control rounded-0'}))
	class Meta:
		model = UserPelajaran
		fields = 'question'

class CreateModule(forms.ModelForm):
    class Meta:
        model = Module
        exclude = ['rangkuman', 'dilihat', 'created_by', 'rilis', 'slug', 'urutan']

        widgets = {
            'nama': TextInput(attrs={'class': 'mb-2 form-control'}),
            'bahasa': Select(attrs={'class': 'mb-2 form-control'}),
            'photo': FileInput(attrs={'class': 'mb-2 form-control'}),
            'kategori': Select(attrs={'class': 'mb-2 form-control'}),
            'level': Select(attrs={'class': 'mb-2 form-control'}),
            'keterangan': TextInput(attrs={'class': 'mb-2 form-control'}),
            'premium': forms.CheckboxInput(attrs={'class': 'mb-2 form-check-input'}),
            'certificate': forms.CheckboxInput(attrs={'class': 'mb-2 form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CreateModule, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateModule, self).save(commit=False)
        instance.rilis = False  # Default value for rilis
        instance.created_by = self.request.user if self.request else None

        # Generate slug based on nama
        instance.slug = slugify(instance.nama)

        if commit:
            instance.save()

        return instance