from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from .models import Member, Board

def index(request):
    template = loader.get_template('index.html')
    #return HttpResponse(template.render()) #나중에 로그인 session 변수값을 가져오지 못함
    return HttpResponse(template.render({}, request))

def theme(request):
    template = loader.get_template('theme.html')
    #return HttpResponse(template.render()) #나중에 로그인 session 변수값을 가져오지 못함
    return HttpResponse(template.render({}, request)) 

def cafe(request):
    template = loader.get_template('cafe.html')
    #return HttpResponse(template.render()) #나중에 로그인 session 변수값을 가져오지 못함
    return HttpResponse(template.render({}, request))

#################### 로그인용 메소드 ############################
from django.shortcuts import redirect, render #방법2

def login(request):
    #template = loader.get_template('login.html') #방법1
    #return HttpResponse(template.render({}, request)) #방법1
    return render(request,'login.html') #방법2 

def login_ok(request):
    #email = request.POST['email'] #방법1
    #pw = request.POST['pw'] #방법1
    email = request.POST.get('email', None) #방법2
    pw = request.POST.get('pw', None) #방법2
    print("email", email, "pw", pw)
    
    try:
        member = Member.objects.get(email=email)
    except Member.DoesNotExist:
        member = None
    print("member", member)
    
    result = 0
    if member != None:
        print("해당 email 회원 존재함")
        if member.pw == pw:
            print("비밀번호까지 일치") 
            result = 2
            
            print("member.email", member.email) #방법1
            request.session['login_ok_user'] = member.email #방법1
            #session_id = request.session.session_key #방법2
            #print("session_id", session_id) #방법2
            #request.session['login_ok_user'] = session_id #방법2
        else:
            print("비밀번호 틀림")
            result = 1
    else:
        print("해당 email 회원 존재하지 않음") 
        result = 0   
    
    template = loader.get_template("login_ok.html") #모든 login_ok.html은 utf-8 형식이어야 한글이 깨지지 않음
    context = {
        'result': result, 
    }
    return HttpResponse(template.render(context, request)) #렌더는 (context, request)를 함께 넘기는 방법

def signup(request):
    #template = loader.get_template('login.html') #방법1
    #return HttpResponse(template.render({}, request)) #방법1
    return render(request,'signup.html') #방법2 
'''
def signup_ok(request):
    #email = request.POST['email'] #방법1
    #pw = request.POST['pw'] #방법1
    email = request.POST.get('email', None) #방법2
    pw = request.POST.get('pw', None) #방법2
    print("email", email, "pw", pw)
    
    try:
        member = Member.objects.get(email=email)
    except Member.DoesNotExist:
        member = None
    print("member", member)
    
    result = 0
    if member != None:
        print("해당 email 회원 존재함")
        if member.pw == pw:
            print("비밀번호까지 일치") 
            result = 2
            
            print("member.email", member.email) #방법1
            request.session['login_ok_user'] = member.email #방법1
            #session_id = request.session.session_key #방법2
            #print("session_id", session_id) #방법2
            #request.session['login_ok_user'] = session_id #방법2
        else:
            print("비밀번호 틀림")
            result = 1
    else:
        print("해당 email 회원 존재하지 않음") 
        result = 0   
    
    template = loader.get_template("login_ok.html") #모든 login_ok.html은 utf-8 형식이어야 한글이 깨지지 않음
    context = {
        'result': result, 
    }
    return HttpResponse(template.render(context, request)) #렌더는 (context, request)를 함께 넘기는 방법
'''


def logout(request):
    if request.session.get('login_ok_user'):
        #del request.session['login_ok_user']
        #request.session.clear() # 서버측의 해당 user의 session방을 초기화
        request.session.flush() # 서버측의 해당 user의 session방을 삭제(더욱 강력)
    return redirect("../") #세션 delete 후 한단계 상위폴더(인덱스.html)로 이동

def mypage(request):
    #template = loader.get_template('login.html') #방법1
    #return HttpResponse(template.render({}, request)) #방법1
    return render(request,'mypage.html') #방법2 


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

from django.urls import reverse
from django.utils import timezone

def b_announce_write_ok(request):
    x = request.POST['writer'] # board_write.html의 태그에서 name=writer 인 값을 불러와라 
    y = request.POST['email']
    z = request.POST['subject']
    a = request.POST['content']
    nowDatetime = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    boardwrite = Board(name=x, email=y, subject=z, content=a, rdate=nowDatetime)
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
    b_free_lists = Board.objects.all().values()
    context = {
       'b_free_lists' : b_free_lists,
    }
    return HttpResponse(template.render(context, request))

def b_anony(request):
    template = loader.get_template('b_anony.html')
    b_anony_lists = Board.objects.all().values()
    context = {
       'b_anony_lists' : b_anony_lists,
    }
    return HttpResponse(template.render(context, request))