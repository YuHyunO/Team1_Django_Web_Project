from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import Board, Member
from django.urls import reverse
from django.utils import timezone
from django.core.paginator import Paginator
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
    if request.method == 'POST':
        template = loader.get_template('login.html')
        email = request.POST['email']
        pwd = request.POST['pwd']
        email.strip()
        pwd.strip()
        
        email_len = False
        pwd_len = False
        
        if len(email) != 0:
            email_len = True
        if len(pwd) != 0:
            pwd_len = True
        
        empty_val = email_len and pwd_len                
        status = 0
        
        if empty_val == True:
            try:
                member = Member.objects.get(email=email)
                if member.pw == pwd:
                    request.session['member_id'] = member.email
                    status = 1
                    print('success')
                    return render(request, 'index.html')
                else:
                    status = 2
            except Member.DoesNotExist:
                status = 3
                
            context = {
                'email_len':email_len,
                'pwd_len':pwd_len,
                'status':status
            }
            return HttpResponse(template.render(context, request))
        else:
            context = {
                'email_len':email_len,
                'pwd_len':pwd_len,
                'status':status,
                'email':email
            }
            return HttpResponse(template.render(context, request))
    else:
        return render(request, 'login.html')
    
def signup(request):
    template = loader.get_template('signup.html')
    if request.method == 'POST':
        name = request.POST['name']
        nickname = request.POST['nickname']
        email = request.POST['email']
        pwd_1 = request.POST['pwd_1']
        pwd_2 = request.POST['pwd_2']
        phone = '01012345678'
        print(len(' abc '))
        print(len(name))
        regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
            
        nickname_val = False
        email_regex = False
        email_val = False
        pwd2_val = False
        
        if re.match(regex_email, email):
            email_regex = True
            
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
            
        all_validation = nickname_val and email_regex and email_val and pwd2_val             
        if all_validation == False:           
            context = {
                'nickname_val':nickname_val,
                'email_val':email_val,
                'email_regex':email_regex,
                'pwd2_val':pwd2_val,
                'name':name,
                'pwd_1':pwd_1,
                'pwd_2':pwd_2,
                'nickname':nickname,
                'email':email
            }
            return HttpResponse(template.render(context, request))
        else:
            nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            member = Member(email=email, pw=pwd_1, name=name, nickname=nickname, phone=phone, rdate=nowDatetime, udate=nowDatetime)
            member.save()
            print('회원가입됨')
            return render(request, 'index.html')
    else:
        return render(request, 'signup.html')

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return redirect(reverse('index'))
def mypage(request):
    return render(request,'mypage.html') 


########################## 공지사항 게시판  ##########################
def b_notice(request):
    template = loader.get_template('b_notice.html')
    board = Board.objects.filter(type='공지사항').values()
    page = request.GET.get('page', '1') #게시판 목록 들어가면 페이지 1번이 디폴트 
    paginator = Paginator(board, 10) #한 페이지에 글 몇개 보이는지 !!
    b_notice_lists = paginator.page(page)
    context = {
       'b_notice_lists' : b_notice_lists,
    }
    return HttpResponse(template.render(context, request))

def b_notice_read(request, no):
    template = loader.get_template('b_notice_read.html') 
    boardcontent = Board.objects.get(no=no)
    context = {
       'boardcontent' : boardcontent,
    }
    return HttpResponse(template.render(context, request))

def b_notice_write(request):
    if request.method == 'POST':
        email = Member.objects.get(email=str(request.session['member_id']))
        nickname = email.nickname

        title = request.POST['title']
        content = request.POST['content']
        type = '공지사항'
        
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        post = Board(email=email, name=nickname, type=type, title=title, content=content, rdate=nowDatetime, udate=nowDatetime)
        post.save()
        
        return HttpResponseRedirect(reverse('b_notice'))
    else:
        return render(request, 'b_notice_write.html')
    
def b_notice_delete(request, no):
    boarddelete = Board.objects.get(no=no)
    boarddelete.delete()
    return HttpResponseRedirect(reverse('b_notice'))

def b_notice_update(request, no):
    template = loader.get_template('b_notice_update.html')
    boardupdate = Board.objects.get(no=no)
    context = {
        'boardupdate': boardupdate, 
    }
    return HttpResponse(template.render(context, request))

def b_notice_update_ok(request, no): 
    a = request.POST['title']
    b = request.POST['content']
    boardupdateok = Board.objects.get(no=no)
    boardupdateok.title = a
    boardupdateok.content = b
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') 
    boardupdateok.udate = nowDatetime 
    boardupdateok.save()
    return HttpResponseRedirect(reverse("b_notice"))

########################## 자유게시판 ##############################
def b_free(request):
    template = loader.get_template('b_free.html')
    board = Board.objects.filter(type='자유게시판').values()
    page = request.GET.get('page', '1') #페이지 1번이 디폴트 값..
    paginator = Paginator(board, 10) #한페이지에 글 몇개 보이는지 !!
    b_free_lists = paginator.page(page)
    context = {
       'b_free_lists' : b_free_lists,
    }
    return HttpResponse(template.render(context, request))

def b_free_read(request, no):
    template = loader.get_template('b_free_read.html')
    boardcontent = Board.objects.get(no=no)
    context = {
       'boardcontent' : boardcontent,
    }
    return HttpResponse(template.render(context, request))

def b_free_write(request):
    if request.method == 'POST':
        email = Member.objects.get(email=str(request.session['member_id']))
        nickname = email.nickname

        title = request.POST['title']
        content = request.POST['content']
        type = '자유게시판'
        
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        post = Board(email=email, name=nickname, type=type, title=title, content=content, rdate=nowDatetime, udate=nowDatetime)
        post.save()
        return HttpResponseRedirect(reverse('b_free'))
    else:
        return render(request, 'b_free_write.html')

def b_free_delete(request, no):
    boarddelete = Board.objects.get(no=no)
    boarddelete.delete()
    return HttpResponseRedirect(reverse('b_free'))

def b_free_update(request, no):
    template = loader.get_template('b_free_update.html')
    boardupdate = Board.objects.get(no=no)
    context = {
        'boardupdate': boardupdate, 
    }
    return HttpResponse(template.render(context, request))

def b_free_update_ok(request, no):
    a = request.POST['title']
    b = request.POST['content']
    boardupdateok = Board.objects.get(no=no)
    boardupdateok.title = a
    boardupdateok.content = b
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') 
    boardupdateok.udate = nowDatetime 
    boardupdateok.save()
    return HttpResponseRedirect(reverse("b_free"))

########################### 익명게시판 ######################################
def b_anony(request):
    template = loader.get_template('b_anony.html')
    board = Board.objects.filter(type='익명게시판').values()
    page = request.GET.get('page', '1') #게시판 목록 들어가면 페이지 1번이 디폴트 
    paginator = Paginator(board, 10) #한페이지에 글 몇개 보이는지 !!
    b_anony_lists = paginator.page(page)
    context = {
       'b_anony_lists' : b_anony_lists,
    }
    return HttpResponse(template.render(context, request))

def b_anony_read(request, no):
    template = loader.get_template('b_anony_read.html') 
    boardcontent = Board.objects.get(no=no)
    context = {
       'boardcontent' : boardcontent,
    }
    return HttpResponse(template.render(context, request))

def b_anony_write(request):
    if request.method == 'POST':
        email = Member.objects.get(email=str(request.session['member_id']))
        nickname = email.nickname

        title = request.POST['title']
        content = request.POST['content']
        type = '익명게시판'
        
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        post = Board(email=email, name=nickname, type=type, title=title, content=content, rdate=nowDatetime, udate=nowDatetime)
        post.save()
        return HttpResponseRedirect(reverse('b_anony'))
    else:
        return render(request, 'b_anony_write.html')
    
def b_anony_delete(request, no):
    boarddelete = Board.objects.get(no=no)
    boarddelete.delete()
    return HttpResponseRedirect(reverse('b_anony'))

def b_anony_update(request, no):
    template = loader.get_template('b_anony_update.html')
    boardupdate = Board.objects.get(no=no)
    context = {
        'boardupdate': boardupdate, 
    }
    return HttpResponse(template.render(context, request))

def b_anony_update_ok(request, no):  
    a = request.POST['title']
    b = request.POST['content']
    boardupdateok = Board.objects.get(no=no)
    boardupdateok.title = a
    boardupdateok.content = b
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boardupdateok.udate = nowDatetime
    boardupdateok.save()
    return HttpResponseRedirect(reverse("b_anony"))