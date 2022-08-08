from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from .models import Board, Member
from django.utils import timezone
from django.core.paginator import Paginator
import re
from django.urls import reverse


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

def search(request):
    template = loader.get_template('search.html')
    return HttpResponse(template.render({}, request))


def login(request):
    if request.method == 'POST':
        template = loader.get_template('login.html')
        email = request.POST['email']
        pwd = request.POST['pwd']
        email = email.strip()
        pwd = pwd.strip()
        
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
    
def signup(request): ##

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
        
        print('-----------------------------------------------') 
        print(phone)   
        
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
        
        else: # 회원가입 성공 시
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
def b_announce(request):
    template = loader.get_template('b_announce.html')
    b_announce_lists = Board.objects.all().values()
    context = {
       'b_announce_lists' : b_announce_lists,
    }
    return HttpResponse(template.render(context, request))

def b_announce_read(request, id):
    template = loader.get_template('b_announce_read.html') #board_content.html에서 id를 불러올 때, boardcontent.id 형태로 불러와야 함
    boardcontent = Board.objects.get(id=id)
    context = {
       'boardcontent' : boardcontent,
    }
    return HttpResponse(template.render(context, request))

def b_announce_write(request):
    template = loader.get_template('b_announce_write.html')
    return HttpResponse(template.render({}, request))



def b_announce_write_ok(request):
    x = request.POST['writer'] # board_write.html의 태그에서 name=writer 인 값을 불러와라 
    y = request.POST['email']
    z = request.POST['subject']
    a = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boardwrite = Board(name=x, email=Member.objects.get(pk=y), title=z, content=a, type='1', rdate=nowDatetime, udate=nowDatetime)
    boardwrite.save()
    return HttpResponseRedirect(reverse('b_announce')) #태그 name일까, url 주소부분을 쓰는걸까

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

def b_announce_update_ok(request, id): # boardupdateok와 board_update.html 과 전혀 연관없음 주의 
    x = request.POST['email'] # board_update.html 태그의 input name='email'인 값을 x로 받음 
    y = request.POST['subject'] # board_update.html 태그의 input name='subject'인 값을 y로 받음 
    z = request.POST['content']
    boardupdateok = Board.objects.get(id=id) # board_update.html 과 변수 boardupdateok는 전혀 직접적 연관 없음 주의 
    boardupdateok.email = x
    boardupdateok.subject = y
    boardupdateok.content = z
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S') #옵션
    boardupdateok.rdate = nowDatetime #옵션
    boardupdateok.save()
    return HttpResponseRedirect(reverse("b_announce"))
    
    
def b_free(request):
    
    template = loader.get_template('b_free.html')
    board = Board.objects.all().values()
    page = request.GET.get('page', '1')
    paginator = Paginator(board, 5)
    b_free_lists = paginator.page(page)
    
    try: 
        email = request.session['member_id']
        print(email)
            
        context = {
        'b_free_lists' : b_free_lists,
        'email' : email,
        }
        return HttpResponse(template.render(context, request))
    except:
        return render(request, 'b_free.html')
        

def b_free_read(request, id):
    template = loader.get_template('b_free_read.html')
    boardcontent = Board.objects.get(id=id)
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
    
def b_free_write_ok(request):
    try:
        x = request.POST['writer']  
        y = request.POST['email']
        z = request.POST['subject']
        a = request.POST['content']
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        boardwrite = Board(name=x, email=Member.objects.get(pk=y), title=z, content=a, rdate=nowDatetime, udate=nowDatetime)
        boardwrite.save()
        return HttpResponseRedirect(reverse('b_free'))
    except:
        return HttpResponseRedirect(reverse('b_free_write'))    

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
    board = Board.objects.all().values()
    page = request.GET.get('page', '1')
    paginator = Paginator(board, 5)
    b_anony_lists = paginator.page(page)
    
    try: 
        email = request.session['member_id']
        print(email)
            
        context = {
        'b_anony_lists' : b_anony_lists,
        'email' : email,
        }
        return HttpResponse(template.render(context, request))
    except:
        return render(request, 'b_anony.html')
    

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
    try:
        x = request.POST['writer']  
        y = request.POST['email']
        z = request.POST['subject']
        a = request.POST['content']
        nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        boardwrite = Board(name=x, email=Member.objects.get(pk=y), title=z, content=a, rdate=nowDatetime, udate=nowDatetime)
        boardwrite.save()
        return HttpResponseRedirect(reverse('b_anony'))
    except:
        return HttpResponseRedirect(reverse('b_anony_write'))

    
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