from django.db import models

class Member(models.Model):
    email = models.EmailField(max_length=50, primary_key=True) #시스템 자동생성 되는 id컬럼(pk)이 생성되지 않음
    pw = models.TextField(max_length=30)
    name = models.CharField(max_length=30) #이름 혹은 별명
    phone = models.TextField(max_length=50)
    rdate = models.DateTimeField() #회원가입일(최초)
    udate = models.DateTimeField() #회원정보 수정일
    
class Board(models.Model): #primary key 는 id 컬럼
    email = models.EmailField(max_length=50) # CharField 보다 더 많이 적을 수 있음
    name = models.CharField(max_length=30) #이름 혹은 별명
    title = models.TextField(max_length=100)
    content = models.TextField()
    rdate = models.DateTimeField() #게시글 등록일
    udate = models.DateTimeField() #게시글 수정일