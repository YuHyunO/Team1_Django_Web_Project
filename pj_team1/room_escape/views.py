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
    query1 = request.GET.get('query1', None)
    query2 = request.GET.get('query2', None)
    if query1 and query2 != None:
        queryset1 = Room.objects.all().filter(loc__regex=rf'{query1}')
        queryset2 = queryset1.filter(loc__regex=rf'{query2}')
        context = {
            'rooms': queryset2
        }
        return HttpResponse(template.render(context, request))
    else:
        context = {
            'rooms': Room.objects.all()
        }        
        return HttpResponse(template.render(context, request))        

def theme(request):
    template = loader.get_template('theme.html')
    themes = Theme.objects.all().values()    
    if request.method == 'POST':
        
        context = {
            'themes': themes
        }
        return HttpResponse(template.render(context, request))
    else:
        context = {
            'themes': themes
        }
        return HttpResponse(template.render(context, request))

def theme_detail(request, no):
    if request.method == 'POST':
        try:
            request.session['member_id']
            get_title = request.POST['theme_review_title']
            get_contents = request.POST['theme_review_contents']
            get_email = request.session['member_id']
            ThemeReview(title=get_title, review=get_contents, email_id=get_email, theme_id=no).save()
            print('인서트 성공')
        except Exception as e:
            print('theme_detail 예외 발생, 로그인해주세요',e)
            pass
    
    template = loader.get_template('theme_detail.html')
    theme = Theme.objects.get(no=no)
    room = Theme.objects.filter(no=no).values('room').get()['room']
    loc = Room.objects.filter(room=room).values('loc').get()['loc']
    the_theme_review = ThemeReview.objects.filter(theme=no).values()
    
    list_found_nickname = []
    for inner in the_theme_review:
        seleted_email = inner['email_id']
        found_nickname = Member.objects.get(email=seleted_email).nickname
        list_found_nickname.append(found_nickname)
    
    context = {
        'theme': theme,
        'room': room,
        'loc': loc,
        'zipped': zip(the_theme_review, list_found_nickname)
    }
    return HttpResponse(template.render(context, request))

def cafe_detail(request, room):
    
    status = 0 
    if request.method == 'POST':   
        try:
            request.session['member_id']
            get_title = request.POST['review_title']            
            star = request.POST['score_input']            
            get_contents = request.POST['review_contents']
            get_email = request.session['member_id']
            star_width = 22*float(star)-6
            try:
                get_title in CafeReview.objects.filter(title=get_title).values('title').get()['title']      
                get_contents in CafeReview.objects.filter(review=get_contents).values('review').get()['review']
            except Exception as e:
                if len(get_title) == 0:
                    status = 1
                elif len(get_contents) == 0:
                    status = 1
                else:   
                    print(star_width)
                    CafeReview(title=get_title, review=get_contents, email_id=get_email, stars=star_width, room=Room.objects.get(pk=room)).save() 
                    print('인서트 성공')    
                   
        except Exception as e:
            print('cafe_detail 예외 발생',e)
            pass
   
    #index에서 접속
    template = loader.get_template('cafe_detail.html')
    cafe = Room.objects.get(room=room) # Room object (셜록홈즈 분당야탑점)
    theme = Theme.objects.filter(room=room).values() # 리스트형식으로 출력
    the_cafe_review = CafeReview.objects.filter(room=room).values()
    
    list_found_nickname = []    

    for inner in the_cafe_review:
        seleted_email = inner['email_id']
        #print("seleted_email",seleted_email)
        found_nickname = Member.objects.get(email=seleted_email).nickname
        #print("found_nickname",found_nickname)
        list_found_nickname.append(found_nickname)
    
    context = {
        'cafe': cafe,
        'theme': theme,
        'zipped' : zip(the_cafe_review, list_found_nickname),
        'room' : room,
        'status': status,
    }
    return HttpResponse(template.render(context, request)) 


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
        
        all_validation = email_regex and email_val and pwd2_val and  nickname_val           
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
            return redirect(reverse('login'))
            
    else:
        return render(request, 'signup.html')

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return redirect(reverse('index'))

def mypage(request): #내 정보 수정 
    template = loader.get_template('mypage.html')
    login_email = request.session['member_id'] # member_id 세션=str 타입의 이메일 주소
    info = Member.objects.get(email=login_email) #모델즈 필드 email이 email2와 일치할때 모든 회원정보를 변수 info에 담음
    #nickname = info.nickname #info에서 닉네임만 불러옴
    
    freeposts = Board.objects.all().filter(type='자유게시판')
    posts1 = freeposts.all().filter(email=info.email).order_by('-no')
    #print(posts1)
    page1 = request.GET.get('page', '1')
    paginator1 = Paginator(posts1, 5)
    page_obj1 = paginator1.get_page(page1)
    b_free_lists = paginator1.page(page1)
    
    anonyposts = Board.objects.all().filter(type='익명게시판')
    posts2 = anonyposts.all().filter(email=info.email).order_by('-no')
    page2 = request.GET.get('page', '1') 
    paginator2 = Paginator(posts2, 5)
    page_obj2 = paginator2.get_page(page2)    
    b_anony_lists = paginator2.page(page2)

    if request.method == 'POST': #이메일, 비번, 이름, 닉네임, 폰번호/ 유효성 검사:비번, 닉네임
        pw_1 = request.POST['pw_1']
        pw_2 = request.POST['pw_2']
        nickname = request.POST['nickname']
        phone = request.POST['phone']
        
        nickname = nickname.strip()
        pw_1 = pw_1.strip()
        pw_2 = pw_2.strip()
        phone = phone.strip()
        
        nickname_val = True #원래 False이나 문제 발생하여 임시적으로 True로 함
        pw_2_val = False
        phone_val = False
        
        #닉네임이 이미 존재할 경우 중복이므로 False, 존재하지 않다면 유효성 True (문제:내 닉네임과도 중복으로 인식함;;)
        try:
            Member.objects.get(nickname=nickname) 
        except Member.DoesNotExist:
            nickname_val = True
            
        if pw_2 == pw_1:
            pw_2_val = True
        
        if len(phone) == 10 or len(phone) == 11:
            phone_val = True

        all_validation = pw_2_val and nickname_val and phone_val
              
        if all_validation == False:           
            context = {
                'nickname_val':nickname_val,
                'pw_2_val':pw_2_val,
                'phone_val':phone_val,
            
                'pw_1':pw_1,
                'pw_2':pw_2,
                'nickname':nickname,
                'phone':phone,
            }
            return HttpResponse(template.render(context, request))
        else:
            nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            info.nickname = nickname
            info.pw = pw_2
            info.phone = phone
            info.udate = nowDatetime            
            info.save()
            return HttpResponseRedirect(reverse("mypage")) #내정보 수정 성공시 마이페이지로 전환
    else: # GET으로 읽어올 때
        context = {
            'info': info,
            
            'b_free_lists' : b_free_lists,
            'page_obj1':page_obj1,
            'b_anony_lists' : b_anony_lists,
            'page_obj2':page_obj2,    
        }        
        return HttpResponse(template.render(context, request))
    
def search(request):
    template = loader.get_template('search.html')
    str_search = str(request.GET['search'])
    print(str_search)
    posts_room = Room.objects.filter(room__contains=str_search) | Room.objects.filter(loc__contains=str_search) 
    posts_theme = Theme.objects.filter(theme__contains=str_search) | Theme.objects.filter(room__in=Room.objects.filter(room__contains=str_search).values('room')) | Theme.objects.filter(genre__contains=str_search) 
    
    
    context = {
        'posts_room': posts_room, 
        'posts_theme': posts_theme, 
        'str_search':str_search,
    }
    return HttpResponse(template.render(context, request))



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
    posts = Board.objects.filter(type='자유게시판').order_by('-no')
    
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
    post_email=post.email
    login_email = request.session['member_id'] # test1@test.com/ str 타입 <class 'str'>
    print(type(post.email)) # <class 'room_escape.models.Member'>
    print(type(post.name)) # <class 'str'>
    print(type(post.content)) # <class 'str'>
    print(login_email) #test2@test.com
    print(post_email)
    print(post.email)
    print(post)
    
    sameperson_val = False
    if post_email == login_email:
        sameperson_val = True # True는 로그인 아이디=게시글 아이디 동일인물일 때
        print("sameperson_val 참트루")
        
    context = {
       'post' : post,
       'post_email': post_email,
       'login_email' : login_email,
       'sameperson_val' : sameperson_val,
    }
    response = render(request, 'b_free_read.html', context)
    # return HttpResponse(template.render(context, request))
    
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

def b_free_delete(request, no):
    post = Board.objects.get(no=no)
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
    posts = Board.objects.filter(type='익명게시판').order_by('-no')
    
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