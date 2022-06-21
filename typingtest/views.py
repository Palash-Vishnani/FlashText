from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Userstatistic,Contact
import random

# Create your views here.
def index(request):
    return render(request,"typingtest/index.html")

def about(request):
    return render(request,"typingtest/about.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        feedback=request.POST.get("feedback")
        if len(name)<3 or len(email)<4 or len(feedback)<2:
            messages.warning(request,"Please fill out all the fields correctly.")
        else:
            contact_message=Contact(name=name,email=email,number=phone,feedback=feedback)
            contact_message.save()
            messages.success(request," Thank you for your query or feedback.")
    return render(request,"typingtest/contact.html")

def test(request):
    with open("typingtest\\static\\typingtest\\randomtext.txt","r") as f:
        text=f.readlines()
    guess1=random.choice(text)
    guess2=random.choice(text)
    prestatement=guess1.replace("\n","")
    poststatement=guess2.replace("\n","")
    # print(statement)
    # if "stats" in request.session:
    #     pass
    # else:
    #     request.session["stats"] = Userstatistic.objects.all()

    if request.user.is_authenticated:
        if request.method == "POST":
            global loginusername
            loginusername=request.POST.get("log_username")
            wpmcount=request.POST.get("wpmcount")
            keycount=request.POST.get("keycount")
            accurate=request.POST.get("accurate")
            rcount=request.POST.get("rcount")
            wcount=request.POST.get("wcount")
            # next_session=request.POST.get("next_session")
            if "stats" not in request.session:
                if len(Userstatistic.objects.filter(login_username=loginusername).all()) == 0:
                    save_stats=Userstatistic(login_username=loginusername,test_wpm=wpmcount,test_keystrokes=keycount,test_accuracy=accurate,correct_count=rcount,wrong_count=wcount)
                    save_stats.save()
                    request.session["stats"] = list(Userstatistic.objects.filter(login_username=loginusername).values('test_id','login_username','test_wpm','test_keystrokes','test_accuracy','correct_count','wrong_count'))
                    print(request.session["stats"])
                    return redirect('/typingtest')
                else:
                    Userstatistic.objects.filter(login_username=loginusername).first().delete()
                    save_stats=Userstatistic(login_username=loginusername,test_wpm=wpmcount,test_keystrokes=keycount,test_accuracy=accurate,correct_count=rcount,wrong_count=wcount)
                    save_stats.save()
                    request.session["stats"] = list(Userstatistic.objects.filter(login_username=loginusername).values('test_id','login_username','test_wpm','test_keystrokes','test_accuracy','correct_count','wrong_count'))
                    print(request.session["stats"])
                    # param={'nextkey':request.session.session_key}
                    # def postsession():
                    #     nextsession = request.session.session_key
                    #     return nextsession
                    global next_session
                    next_session = request.session.session_key
                    return redirect('/typingtest')
            else:
                print("Yes it is.")
                if len(request.session["stats"]) == 4:
                    save_stats=Userstatistic(login_username=loginusername,test_wpm=wpmcount,test_keystrokes=keycount,test_accuracy=accurate,correct_count=rcount,wrong_count=wcount)
                    save_stats.save()
                    saved_list = request.session["stats"]
                    saved_list.append(Userstatistic.objects.filter(login_username=loginusername).values('test_id','login_username','test_wpm','test_keystrokes','test_accuracy','correct_count','wrong_count').last())
                    request.session["stats"] = saved_list
                    print(request.session["stats"])
                    messages.warning(request," Data saved but your session trials are over. Please logout and login again to continue typing test.")
                    return redirect('/')
                elif len(request.session["stats"]) < 4:
                    save_stats=Userstatistic(login_username=loginusername,test_wpm=wpmcount,test_keystrokes=keycount,test_accuracy=accurate,correct_count=rcount,wrong_count=wcount)
                    save_stats.save()
                    saved_list = request.session["stats"]
                    saved_list.append(Userstatistic.objects.filter(login_username=loginusername).values('test_id','login_username','test_wpm','test_keystrokes','test_accuracy','correct_count','wrong_count').last())
                    request.session["stats"] = saved_list
                    print(request.session["stats"])
                    if request.user.is_authenticated !=True:
                        print("User logged out.")
                    return redirect('/typingtest')
                elif len(request.session["stats"]) > 4:
                    print(request.session["stats"])
                    if request.session.session_key == next_session:
                        Userstatistic.objects.filter(login_username=loginusername).first().delete()
                        save_stats=Userstatistic(login_username=loginusername,test_wpm=wpmcount,test_keystrokes=keycount,test_accuracy=accurate,correct_count=rcount,wrong_count=wcount)
                        save_stats.save()
                        saved_list = request.session["stats"]
                        saved_list.append(Userstatistic.objects.filter(login_username=loginusername).values('test_id','login_username','test_wpm','test_keystrokes','test_accuracy','correct_count','wrong_count').last())
                        request.session["stats"] = saved_list
                        print(request.session["stats"])
                        return redirect('/typingtest')
                    else:    
                        messages.error(request," Data cannot be saved because your session trials are over. Please logout and login again to continue typing test.")
                        return redirect('/')
        
        if "stats" in request.session:             
            if len(request.session["stats"]) < 4:
                if request.user.is_authenticated != True:
                    print("You have logged out")
            # request.session.modified = True
        previous_stats=Userstatistic.objects.filter(login_username=request.user).last()
        params={"statement1":prestatement,"statement2":poststatement,"previous_stats":previous_stats}
        return render(request,"typingtest/test.html",params)
    else:
        params={"statement1":prestatement,"statement2":poststatement}
        return render(request,"typingtest/test.html",params)


def handlesignup(request):
    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        fname=request.POST.get("firstname")
        lname=request.POST.get("lastname")
        pass1=request.POST.get("password")
        pass2=request.POST.get("confirmpass")

        if len(username) > 20:
            messages.error(request," Try again. Please enter a short and precise username.")
            return redirect('/')
        if pass1!=pass2:
            messages.error(request," Try again. Passwords do not match.")
            return redirect('/')
        if not username.isalnum():
            messages.error(request," Try again. Username should contain only letters and numbers.")
            return redirect('/')
        
        newuser = User.objects.create_user(username,email,pass1)
        newuser.first_name = fname
        newuser.last_name = lname
        newuser.save()
        messages.success(request," Account successfully created.")
        return redirect('/')

    else:
        return HttpResponse("Error 404 - Page not found")

def handlelogin(request):
    if request.method == "POST":
        logusername=request.POST.get("logusername")
        logpassword=request.POST.get("logpassword")
        user = authenticate(username=logusername,password=logpassword)

        if user is not None:
            login(request,user)
            messages.success(request,f" Hello {user} you have successfully logged in.")
            return redirect('/')

        else:
            messages.error(request," Login failed. Please try again.")
            return redirect('/')

    return HttpResponse("Error 404 - Page not found")

def handlelogout(request):
    logout(request)
    messages.success(request," You have successfully logged out.")
    return redirect('/')