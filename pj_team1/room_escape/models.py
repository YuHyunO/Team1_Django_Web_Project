from django.db import models

class Member(models.Model):
    email = models.CharField(primary_key=True, max_length=255)
    pw = models.TextField()
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)    
    phone = models.CharField(max_length=50)
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    
class Board(models.Model):
    email = models.ForeignKey(Member, related_name='board_email', on_delete=models.CASCADE, db_column='email')
    name = models.CharField(max_length=255)    
    type = models.CharField(max_length=20)
    title = models.TextField(max_length=1000)
    content = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
  
class Room(models.Model):
    room = models.TextField(primary_key=True)
    loc = models.TextField()
    url = models.CharField(max_length=255)
    tel = models.CharField(max_length=50)
    theme_number = models.IntegerField(default=0)

class CafeReview(models.Model):
    no = models.AutoField(primary_key=True)
    email = models.ForeignKey(Member, related_name='CafeReview_email', on_delete=models.CASCADE, db_column='email')
    room = models.ForeignKey(Room, related_name='CafeReview_room', on_delete=models.CASCADE, db_column='room')
    review = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()
    
class Theme(models.Model):
    theme = models.TextField(primary_key=True)
    room = models.ForeignKey(Room, related_name='Theme_room', on_delete=models.CASCADE, db_column='room')
    img_path = models.TextField()
    genre = models.CharField(max_length=255)
    people = models.CharField(max_length=10, default='-')
    info = models.TextField(default='-')
    difficulty = models.CharField(max_length=10, default='0')
    horror = models.CharField(max_length=10, default='0')
    activity = models.CharField(max_length=10, default='0')
    star = models.CharField(max_length=10, default='0')
    recommend = models.IntegerField(default=0)
            
class ThemeReview(models.Model):
    no = models.AutoField(primary_key=True)
    email = models.ForeignKey(Member, related_name='ThemeReview_email', on_delete=models.CASCADE, db_column='email')
    theme = models.ForeignKey(Theme, related_name='ThemeReview_theme', on_delete=models.CASCADE, db_column='theme')
    review = models.TextField()
    rdate = models.DateTimeField()
    udate = models.DateTimeField()