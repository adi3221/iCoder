from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
# Create your views here.
def home(request):
    return render(request, 'home/home.html')
    

def about(request):
    messages.success(request, 'This is About')
    messages.error(request, 'This is About')
    messages.warning(request, 'This is About')
    messages.info(request, 'This is About')
    return render(request, 'home/about.html')

def contact(request):
    # messages.error(request, 'Welcome to Contact') 
    if request.method=="POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your message has been successfully sent')

    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        # allPosts = Post.objects.all()
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, 'No search results found. Please refine your query')
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

def handleSignup(request):
    if request.method == 'POST':
        # Get the post Parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous inputs
        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('home')
        if not username.isalnum():
            messages.error(request, 'Username should only contain letters and numbers')
            return redirect('home')

        if pass1 != pass2:
            messages.error(request, 'Your confirm password did not match with your Password')
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 Not Found')

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request,user)
            messages.success(request, "Successfully Logged In")
            params ={'username': loginusername, 'password': loginpassword}
            return render(request, 'home/user.html', params)
        else:
            messages.warning(request, "Invalid Credentials, Please try again")
            return redirect('home')

    return HttpResponse('404 - Not found')

def handleLogout(request):
    # if request.method=='POST':
        logout(request)
        messages.success(request, "Successfully Logged Out")
        return redirect('home')
     