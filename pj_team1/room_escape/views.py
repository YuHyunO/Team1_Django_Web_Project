from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import Member, Board, Room, Theme, CafeReview, ThemeReview
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import date, datetime, timedelta
from django.urls import reverse
import random
import re

def index(request):
    template = loader.get_template('index.html')
    
    rooms = Room.objects.all().values()
    rooms_random = []
    while True:
        if len(rooms_random) == 3:
            break
        x = random.randint(0, len(rooms)-1)
        try:
            rooms_random.index(rooms[x])
        except:
            rooms_random.append(rooms[x])
            
    themes = Theme.objects.all().values()
    themes_random = []
    while True:
        if len(themes_random) == 3:
            break
        x = random.randint(0, len(themes)-1)
        try:
            themes_random.index(themes[x])
        except:
            themes_random.append(themes[x])
            
    context = {
        'rooms_random': rooms_random,
        'themes_random': themes_random
    }
    return HttpResponse(template.render(context, request))

def cafe(request):
    template = loader.get_template('cafe.html')
    rooms = Room.objects.all().values()
    context = {
        'rooms': rooms
    }
    return HttpResponse(template.render(context, request))

def theme(request):
    template = loader.get_template('theme.html')
    themes = Theme.objects.all().values()
    context = {
        'themes': themes
    }
    return HttpResponse(template.render(context, request))

def theme_detail(request, no):
    template = loader.get_template('theme_detail.html')
    theme = Theme.objects.get(no=no)
    room = Theme.objects.filter(no=no).values('room').get()['room']
    loc = Room.objects.filter(room=room).values('loc').get()['loc']
    context = {
        'theme': theme,
        'room': room,
        'loc': loc
    }
    return HttpResponse(template.render(context, request))

def cafe_detail(request, room):
    template = loader.get_template('cafe_detail.html')
    cafe = Room.objects.get(room=room)
    theme = Theme.objects.filter(room=room).values()
    context = {
        'cafe': cafe,
        'theme': theme
    }
    return HttpResponse(template.render(context, request))

def login(request):
    if request.method == 'POST':
        template = loader.get_template('login.html')
        email = request.POST['email']
        pwd = request.POST['email']
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

    if request.method == 'POST':
        name = request.POST['name']
        nickname = request.POST['nickname']
        email = request.POST['email']
        pwd_1 = request.POST['pwd_1']
        pwd_2 = request.POST['pwd_2']
        phone = request.POST['phone']
        
        name = name.strip()
        nickname = nickname.strip()
        email = email.strip()
        pwd_1 = pwd_1.strip()
        pwd_2 = pwd_2.strip()
        phone = phone.strip()
        
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
        
        template = loader.get_template('signup.html')
        
        all_validation = email_regex and email_val and pwd2_val             
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
                'phone':phone,
            }
            return HttpResponse(template.render(context, request))
        
        else:
            nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            member = Member(email=email, pw=pwd_2, name=name, nickname=nickname, phone=phone, rdate=nowDatetime, udate=nowDatetime)
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
    posts = Board.objects.filter(type='공지사항').order_by('-no')
    
    page = request.GET.get('page', '1') 
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    b_notice_lists = paginator.page(page)
    context = {
       'b_notice_lists':b_notice_lists,
       'page_obj':page_obj 
    }
    return HttpResponse(template.render(context,request))

def b_notice_read(request, no):
    post = Board.objects.get(no=no)
    context = {
       'post' : post,
    }
    response = render(request, 'b_notice_read.html', context)
    
    expire_date,now = datetime.now(),datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    
    cookie_value = request.COOKIES.get('hitboard','_')
    
    if f'_{no}_' not in cookie_value:
        cookie_value += f'{no}_'
        response.set_cookie('hitboard',value=cookie_value, max_age=max_age, httponly=True)
        post.hit +=1
        post.save()

    return response

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
    post = Board.objects.get(no=no)
    post.delete()
    return HttpResponseRedirect(reverse('b_notice'))

def b_notice_update(request, no):
    template = loader.get_template('b_notice_update.html')
    post = Board.objects.get(no=no)
    
    if request.method == 'POST':
        a = request.POST['title']
        b = request.POST['content']
        post = Board.objects.get(no=no)
        post.title = a
        post.content = b
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') 
        post.udate = nowDatetime 
        post.save()
        return HttpResponseRedirect(reverse("b_notice"))
    else:
        context = {
            'post': post, 
        }        
        return HttpResponse(template.render(context, request))
    
 ########################## 자유게시판  ##########################   
def b_free(request):
    template = loader.get_template('b_free.html')
    posts = Board.objects.filter(type='자유게시판').values()
    
    page = request.GET.get('page', '1')
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)
    b_free_lists = paginator.page(page)
    context = {
       'b_free_lists' : b_free_lists,
       'page_obj':page_obj 
    }
    return HttpResponse(template.render(context, request))

def b_free_read(request, no):
    post = Board.objects.get(no=no)
    context = {
       'post' : post,
    }
    response = render(request, 'b_free_read.html', context)
    
    expire_date,now = datetime.now(),datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    
    cookie_value = request.COOKIES.get('hitboard','_')
    
    if f'_{no}_' not in cookie_value:
        cookie_value += f'{no}_'
        response.set_cookie('hitboard',value=cookie_value, max_age=max_age, httponly=True)
        post.hit +=1
        post.save()

    return response

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

def b_free_delete(request, id):
    post = Board.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect(reverse('b_free'))

def b_free_update(request, no):
    template = loader.get_template('b_free_update.html')
    post = Board.objects.get(no=no) 
    
    if request.method == 'POST':
        a = request.POST['title']
        b = request.POST['content']
        post = Board.objects.get(no=no)
        post.title = a
        post.content = b
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') 
        post.udate = nowDatetime 
        post.save()
        return HttpResponseRedirect(reverse("b_free"))
    else:
        context = {
            'post': post, 
        }           
        return HttpResponse(template.render(context, request))

 ########################## 익명게시판  ##########################
def b_anony(request):
    template = loader.get_template('b_anony.html')
    posts = Board.objects.filter(type='익명게시판').values()
    
    page = request.GET.get('page', '1') 
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)    
    b_anony_lists = paginator.page(page)
    context = {
       'b_anony_lists' : b_anony_lists,
       'page_obj':page_obj        
    }
    return HttpResponse(template.render(context, request))

def b_anony_read(request, no):
    post = Board.objects.get(no=no)
    context = {
       'post' : post,
    }
    response = render(request, 'b_anony_read.html', context)
    
    expire_date,now = datetime.now(),datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    
    cookie_value = request.COOKIES.get('hitboard','_')
    
    if f'_{no}_' not in cookie_value:
        cookie_value += f'{no}_'
        response.set_cookie('hitboard',value=cookie_value, max_age=max_age, httponly=True)
        post.hit +=1
        post.save()

    return response

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
    post = Board.objects.get(no=no)
    post.delete()
    return HttpResponseRedirect(reverse('b_anony'))

def b_anony_update(request, no):
    template = loader.get_template('b_anony_update.html')
    posts = Board.objects.get(no=no)    
    
    if request.method == 'POST':
        a = request.POST['title']
        b = request.POST['content']
        posts = Board.objects.get(no=no)
        posts.title = a
        posts.content = b
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        posts.udate = nowDatetime
        posts.save()
        return HttpResponseRedirect(reverse("b_anony"))
    else:
        context = {
            'posts': posts, 
        }
        return HttpResponse(template.render(context, request))        