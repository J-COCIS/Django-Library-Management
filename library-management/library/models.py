from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class StudentExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    branch = models.CharField(max_length=40)
    bookid = models.CharField(max_length=100)

    # used in issue book

    def __str__(self):
        return self.user.first_name

    @property
    def get_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi', 'Sci-Fi')
    ]
    title = models.CharField(max_length=100)
    bookid = models.CharField(max_length=100)
    subjectArea = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    edition = models.CharField(max_length=100)
    publicationDate = models.DateField()
    category = models.CharField(
        max_length=30, choices=catchoice, default='education')

    def __str__(self):
        return str(self.title)+"["+str(self.bookid)+']'

def get_expiry():
    return datetime.today() + timedelta(days=15)


class IssuedBook(models.Model):
    #bookid=[(str(book.bookid),book.name+' ['+str(book.bookid)+']') for book in Book.objects.all()]
    bookid = models.CharField(max_length=30)
    issuedate = models.DateField(auto_now=True,null=True, blank=True)
    expirydate = models.DateField(default=get_expiry)
    def __str__(self):
        return self.bookid


