from django import forms
from django.contrib.auth.models import User
from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class LibrarianSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class StudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']


class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra
        fields = ['branch'] 


class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['title', 'bookid', 'subjectArea',
                  'author', 'edition', 'publicationDate']


class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    bookid2=forms.ModelChoiceField(queryset=models.Book.objects.all(),empty_label="Title and bookid", to_field_name="bookid",label='Title and bookid')

    
