from multiprocessing import context
from turtle import title
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from . import forms, models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from library.models import Book
from django.contrib import messages


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/index.html')

# for showing signup/login button for student


def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/studentclick.html')

# for showing signup/login button for Librarian


def librarianclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'library/librarianclick.html')


def librariansignup_view(request):
    form = forms.LibrarianSigupForm()
    if request.method == 'POST':
        form = forms.LibrarianSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            messages.success(request,'You have successfully registered, Now you can login as a Librarian')

            my_librarian_group = Group.objects.get_or_create(name='LIBRARIAN')
            my_librarian_group[0].user_set.add(user)

            return HttpResponseRedirect('librarianlogin')
       
    return render(request, 'library/librariansignup.html', {'form': form})


def studentsignup_view(request):
    form1 = forms.StudentUserForm()
    form2 = forms.StudentExtraForm()
    mydict = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.StudentUserForm(request.POST)
        form2 = forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
            messages.success(request,'You have successfully registered, Now you can login as a Student')

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
       

        return HttpResponseRedirect('studentlogin')
    return render(request, 'library/studentsignup.html', context=mydict)


def is_librarian(user):
    return user.groups.filter(name='LIBRARIAN').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()



def afterlogin_view(request):
    if is_librarian(request.user):
        messages.success(request,'You have succesfully logged in')
        return render(request, 'library/librarianafterlogin.html')
    else:
        messages.success(request,'You have succesfully logged in')
        return render(request, 'library/studentafterlogin.html')


@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def addbook_view(request):
    # now it is empty book form for sending to html
    form = forms.BookForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.BookForm(request.POST)
        if form.is_valid():
            user = form.save()
            return render(request, 'library/bookadded.html')
    return render(request, 'library/addbook.html', {'form': form})


def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})


@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def issuebook_view(request):
    form = forms.IssuedBookForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj = models.IssuedBook()
            obj.bookid = request.POST.get('bookid2')
            obj.save()
            return render(request, 'library/bookissued.html')
    return render(request, 'library/issuebook.html', {'form': form})


@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def viewissuedbook_view(request):
    issuedbooks = models.IssuedBook.objects.all()
    li = []
   
    for m in issuedbooks:
        issdate = str(m.issuedate.day)+'-' + \
            str(m.issuedate.month)+'-'+str(m.issuedate.year)
        expdate = str(m.expirydate.day)+'-' + \
            str(m.expirydate.month)+'-'+str(m.expirydate.year)
        # fine calculation
        days = (date.today()-m.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d-3
            fine = day*(5000/3)
        elif d>15:
            day= d-10
            fine = day*(5000)


        books = list(models.Book.objects.filter(bookid=m.bookid))
        i = 0
        for l in books:
            t = (
             books[i].title, books[i].bookid, books[i].author, books[i].edition, issdate, expdate, fine)
            i = i+1
            li.append(t)

    return render(request, 'library/viewissuedbook.html', {'li': li})


@login_required(login_url='librarianlogin')
@user_passes_test(is_librarian)
def viewstudent_view(request):
    students = models.StudentExtra.objects.all()
    return render(request, 'library/viewstudent.html', {'students': students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student = models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook = models.IssuedBook.objects.filter(
        bookid=student[0].bookid)
    li=[]

    li1 = []

    li2 = []
    for m in issuedbook:
        books = models.Book.objects.filter(bookid=m.bookid)
        for book in books:
            t = (request.user,
                 student[0].branch, book.name, book.author)
            li1.append(t)
        issdate = str(m.issuedate.day)+'-' + \
            str(m.issuedate.month)+'-'+str(m.issuedate.year)
        expdate = str(m.expirydate.day)+'-' + \
            str(m.expirydate.month)+'-'+str(m.expirydate.year)
        # fine calculation
        days = (date.today()-m.issuedate)
        print(date.today())
        d = days.days
        fine = 0
        if d > 15:
            day = d-15
            fine = day*10
        t = (issdate, expdate, fine)
        li2.append(t)

        books=list(models.Book.objects.filter(bookid=m.bookid))
        students=list(models.StudentExtra.objects.filter(userid=m.userid))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].userid,books[i].name,books[i].author,issdate,expdate,fine)
            i=i+1
            li.append(t)

    return render(request, 'library/viewissuedbookbystudent.html', {'li1': li1, 'li2': li2})


def search_book(request):
    q=request.GET.get('q')
    searchedBook=Book.objects.filter(title__icontains=q)
    if searchedBook is not None:
        context={'searchedBook':searchedBook}
        return render(request,'library/search.html',context)
    else:
        return render(request,'library/search.html',{'book':"none"})

    
def logout_view(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out!!')
    return render(request,'library/index.html')

