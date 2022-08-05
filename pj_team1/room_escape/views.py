from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import Board, Member
import re


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def cafe(request):
    template = loader.get_template('cafe.html')
    return HttpResponse(template.render({}, request))

def theme(request):
    template = loader.get_template('theme.html')
    return HttpResponse(template.render({}, request))

def theme_detail(request):
    template = loader.get_template('theme_detail.html')
    return HttpResponse(template.render({}, request))

def cafe_detail(request):
    template = loader.get_template('cafe_detail.html')
    return HttpResponse(template.render({}, request))

from django.shortcuts import redirect, render

def login(request):
    return render(request,'login.html')

def login_ok(request):
    pass

def signup(request): ##
    template = loader.get_template('signup.html')
    if request.method == 'POST':
        name = request.POST['name']
        nickname = request.POST['nickname']
        email = request.POST['email']
        pwd_1 = request.POST['pwd_1']
        pwd_2 = request.POST['pwd_2']
        print(len(' abc '))
        print(len(name))
        regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
        # regex_pwd_1 = '\S{8,25}'
            
        nickname_val = False
        email_re = False
        email_val = False
        pwd2_val = False
        
        if re.match(regex_email, email):
            email_re = True
        try:
            Member.objects.get(nickname=nickname) 
        except Member.DoesNotExist:
            nickname_val = True        
        try:
            Member.objects.get(email=email)
        except Member.DoesNotExist:
            email_val = True
                    
        if pwd_2 == pwd_1:
            pwd2_val = True
            
        all_validation = nickname_val and email_re and email_val and pwd2_val             
        if all_validation == False:           
            context = {
                'nickname_val':nickname_val,
                'email_val':email_val,
                # 'pwd1_val':pwd1_val,
                'pwd2_val':pwd2_val,
                'name':name,
                'nickname':nickname,
                'email':email
            }
            return HttpResponse(template.render(context, request))
        else:
            return render(request, 'index.html')
    else:
        return render(request, 'signup.html')

def logout(request):
    if request.session.get('login_ok_user'):
        request.session.flush() 
    return redirect("../")
def mypage(request):
    return render(request,'mypage.html') 


########################## 공지사항 게시판  ##########################
def b_announce(request):
    template = loader.get_template('b_announce.html')
    b_announce_lists = Board.objects.all().values()
    context = {
       'b_announce_lists' : b_announce_lists,
    }
    return HttpResponse(template.render(context, request))

def b_announce_read(request, id):
    template = loader.get_template('b_announce_read.html') 
    boardcontent = Board.objects.get(id=id)
    context = {
       'boardcontent' : boardcontent,
    }
    return HttpResponse(template.render(context, request))

def b_announce_write(request):
    template = loader.get_template('b_announce_write.html')
    return HttpResponse(template.render({}, request))

from django.urls import reverse
from django.utils import timezone

def b_announce_write_ok(request):
    x = request.POST['writer']  
    y = request.POST['email']
    z = request.POST['subject']
    a = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boardwrite = Board(name=x, email=Member.objects.get(pk=y), title=z, content=a, type='1', rdate=nowDatetime, udate=nowDatetime)
    boardwrite.save()
    return HttpResponseRedirect(reverse('b_announce')) 

def b_announce_delete(request, id):
    boarddelete = Board.objects.get(id=id)
    boarddelete.delete()
    return HttpResponseRedirect(reverse('b_announce'))

def b_announce_update(request, id):
    template = loader.get_template('b_announce_update.html')
    boardupdate = Board.objects.get(id=id)
    context = {
        'boardupdate': boardupdate, 
    }
    return HttpResponse(template.render(context, request))

def b_announce_update_ok(request, id): 
    x = request.POST['email'] 
    y = request.POST['subject']
    z = request.POST['content']
    boardupdateok = Board.objects.get(id=id)
    boardupdateok.email = x
    boardupdateok.subject = y
    boardupdateok.content = z
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') 
    boardupdateok.rdate = nowDatetime 
    boardupdateok.save()
    return HttpResponseRedirect(reverse("b_announce"))
    
    
def b_free(request):
    template = loader.get_template('b_free.html')
    b_free_lists = Board.objects.all().values()
    context = {
       'b_free_lists' : b_free_lists,
    }
    return HttpResponse(template.render(context, request))

def b_free_read(request, id):
    template = loader.get_template('b_free_read.html')
    boardcontent = Board.objects.get(id=id)
    context = {
       'boardcontent' : boardcontent,
    }
    return HttpResponse(template.render(context, request))

def b_free_write(request):
    template = loader.get_template('b_free_write.html')
    return HttpResponse(template.render({}, request))

def b_free_write_ok(request):
    x = request.POST['writer'] 
    y = request.POST['email']
    z = request.POST['subject']
    a = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boardwrite = Board(name=x, email=y, title=z, content=a, rdate=nowDatetime, udate=nowDatetime)
    boardwrite.save()
    return HttpResponseRedirect(reverse('b_free')) 

def b_free_delete(request, id):
    boarddelete = Board.objects.get(id=id)
    boarddelete.delete()
    return HttpResponseRedirect(reverse('b_free'))

def b_free_update(request, id):
    template = loader.get_template('b_free_update.html')
    boardupdate = Board.objects.get(id=id)
    context = {
        'boardupdate': boardupdate, 
    }
    return HttpResponse(template.render(context, request))

def b_free_update_ok(request, id):
    x = request.POST['email'] 
    y = request.POST['subject']
    z = request.POST['content']
    boardupdateok = Board.objects.get(id=id)
    boardupdateok.email = x
    boardupdateok.subject = y
    boardupdateok.content = z
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') 
    boardupdateok.rdate = nowDatetime 
    boardupdateok.save()
    return HttpResponseRedirect(reverse("b_free"))

def b_anony(request):
    template = loader.get_template('b_anony.html')
    b_anony_lists = Board.objects.all().values()
    context = {
       'b_anony_lists' : b_anony_lists,
    }
    return HttpResponse(template.render(context, request))

def b_anony_read(request, id):
    template = loader.get_template('b_anony_read.html') 
    boardcontent = Board.objects.get(id=id)
    context = {
       'boardcontent' : boardcontent,
    }
    return HttpResponse(template.render(context, request))

def b_anony_write(request):
    template = loader.get_template('b_anony_write.html')
    return HttpResponse(template.render({}, request))

def b_anony_write_ok(request):
    x = request.POST['writer']  
    y = request.POST['email']
    z = request.POST['subject']
    a = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boardwrite = Board(name=x, email=y, title=z, content=a, rdate=nowDatetime, udate=nowDatetime)
    boardwrite.save()
    return HttpResponseRedirect(reverse('b_anony'))

def b_anony_delete(request, id):
    boarddelete = Board.objects.get(id=id)
    boarddelete.delete()
    return HttpResponseRedirect(reverse('b_anony'))

def b_anony_update(request, id):
    template = loader.get_template('b_anony_update.html')
    boardupdate = Board.objects.get(id=id)
    context = {
        'boardupdate': boardupdate, 
    }
    return HttpResponse(template.render(context, request))

def b_anony_update_ok(request, id):  
    x = request.POST['email'] 
    y = request.POST['subject']  
    z = request.POST['content']
    boardupdateok = Board.objects.get(id=id)  
    boardupdateok.email = x
    boardupdateok.subject = y
    boardupdateok.content = z
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boardupdateok.rdate = nowDatetime
    boardupdateok.save()
    return HttpResponseRedirect(reverse("b_anony"))