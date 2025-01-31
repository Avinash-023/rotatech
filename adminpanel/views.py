from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.urls import  reverse
from django.contrib import messages
from .forms import contactform, registerform,resetpasswordform,loginform,forgotpasswordform,profileform
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import  send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from adminpanel.models import post,profile, words
import pdb
import logging
from django.http import JsonResponse
from .models import gameresult
import json
from django.views.decorators.csrf import csrf_exempt
def index(request):
    logger=logging.getLogger("testing")
    blogtitle="bjarath"
    posts=post.objects.all()
    logger.debug("Blog title: %s", blogtitle)
    print(blogtitle)
   
    
    


    
    return render(request,"index.html",{ 'blogtitle':blogtitle})
def index1(request):
    blogtitle="bjarath"
    posts=post.objects.all()
    return render(request,"index1.html",{ 'blogtitle':blogtitle,'posts':posts})
    

# Create your views here.
def register(request):
    form=registerform()
    blogtitle="bjarath" 
    if request.method =='POST':
        form=registerform(request.POST)
        if form.is_valid():

            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            """  print('registersucess') """
            messages.success(request,"registration succesfull")
            return redirect("login")
         
    
               
    return render (request,"register.html",{'form':form,'blogtitle':blogtitle})

def about(request):
    return render(request,'about.html')

def dyslexia(request):
     return render (request,"dyslexia.html")
def texttospeech(request):
    return render(request,'texttospeech.html')
def example(request):
    return render(request,'example.html')
def login(request):
    form=loginform()
    if request.method =="POST":
        form=loginform(request.POST)
        if form.is_valid():
           
           print("login success")
           username=form.cleaned_data['username']
           password=form.cleaned_data['password']
           user=authenticate(username=username,password=password)
           if user is not None:
            auth_login(request,user)
            messages.success(request,'you are successfully logged in')
            return redirect("index")
            
                
            
    return render (request,"login.html",{'form':form})
def logout(request):
    print("Logging out user")
    auth_logout(request)
    return redirect('login')
def forgotpassword(request):
    form=forgotpasswordform()
    if request.method=='POST':
        form=forgotpasswordform(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            user=User.objects.get(email=email)
            #send resnt email
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            currentsite=get_current_site(request)
            domain=currentsite.domain
            subject="reset password requsted"
            message=render_to_string('resetpassword.html',{
                'domain':domain,
                'uid':uid,
                'token':token
            })
            send_mail(subject,message,'noreply@hellojiohellojio.com',[email])
            messages.success(request,"your email is sent")





        
    return render(request,'forgotpassword.html',{'form':form})
def resetpassword(request,uidb64,token):
    form=resetpasswordform()
    if request.method=='POST':
        form=resetpasswordform(request.POST)
        if form.is_valid():
            newpassword=form.cleaned_data['newpassword']
            try:
                uid=urlsafe_base64_decode(uidb64)
                user=User.objects.get(pk=uid)
            except(TypeError,ValueError,OverflowError,User.DoesNotExist):
                user=None
            if user  is not None and default_token_generator.check_token(user,token):
                user.set_password(newpassword)  
                user.save()
                messages.success(request,'password changed correctly')    
                return redirect('login') 
            else:
                messages.error(request,'the password link is invalid')




    return render(request,'resetpassword2.html',{'form':form})

def game(request):
    return render (request,"game.html")
def spell(request):
    return render(request,"spell.html")

def index(request):
    return render(request,"index.html")
def profiles(request):
    posts=profile.objects.first()
    return render(request,"profile.html",{'posts':posts})
def game(request):
    # Fetch all the word posts
    posts = words.objects.all().values('name', 'image')  # Get 'name' and 'image' fields
    # Serialize the data to JSON format
    posts_json = json.dumps(list(posts))
    
    # Pass the serialized data to the template
    return render(request, "game.html", {'posts': posts_json, 'blogtitle': 'bjarath'})

def createprofile(request):
    form=profileform()
    if request.method=="POST":
        form=profileform(request.POST,request.FILES)
        if form .is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('profile')
    return render(request,"createprofile.html",{'form':form})

""" def newpost(request):
    
    form=profileform()
    if request.method=="POST":
        form=profileform(request.POST,request.FILES)
        if form .is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
            return redirect('adminpanel:dashboard')
    return render(request,'newpost.html',{'form':form}) """
def contact(request):
     form=contactform()
     if request.method=='POST':
        form=contactform( request.POST)
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        send_mail(name,message,'noreply@hellojiohellojio.com',[email])
        messages.success(request,"your email is sent")
     return render(request,'contact.html',{'form':form})  
 
def result(request):
    # Retrieve all game results
    oii = gameresult.objects.all()
    
    scores = []
    words = []
    
    # Collect words and their corresponding scores (1 for correct, 0 for incorrect)
    for result in oii:
        words.append(result.word)  # Add the word to the words list
        scores.append(1 if result.iscorrect else 0)  # Add 1 for correct answer, 0 for incorrect answer
    
        # Limit to the first 5 results
        if len(scores) > 4:
            break
    
    # Prepare for template rendering
    words = words  # List of words
    scores = scores  # List of scores (1 or 0)
    
    return render(request, 'result.html', {'words': words, 'scores': scores})




  # Ensure this is the correct model

  # Assuming the model is named GameResult





""" def graph(request):
    # Example data: words and corresponding scores (1 for correct, 0 for incorrect)
    words = ['Word1', 'Word2', 'Word3', 'Word4', 'Word5']
    scores = [1, 0, 0, 1, 1]  # 1 = correct, 0 = incorrect
    
    # Pass the data to the template
    return render(request, 'graph.html', {'words': words, 'scores': scores}) """




import logging

logger = logging.getLogger(__name__)

def graph(request):
    if request.method == 'POST':
        word = request.POST.get('word')
        correctanswer = request.POST.get('correct_answer')
        useranswer = request.POST.get('user_answer')

        if not useranswer or not correctanswer:
            return JsonResponse({'status': 'error', 'message': 'Missing answer(s).'}, status=400)

        is_correct = useranswer.lower() == correctanswer.lower()

        game_result = gameresult(
            word=word,
            correctanswer=correctanswer,
            useranswer=useranswer,
            iscorrect=is_correct
        )
        
        try:
            game_result.save()
            logger.info(f"Game result saved: {game_result}")
        except Exception as e:
            logger.error(f"Error saving game result: {e}")
            return JsonResponse({'status': 'error', 'message': 'Error saving result.'}, status=500)

       

        return JsonResponse({'status': 'success', 'message': 'Game result saved successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

