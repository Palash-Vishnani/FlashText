from django.db import models

# Create your models here.
class Userstatistic(models.Model):
    test_id=models.AutoField(primary_key=True)
    login_username=models.CharField(max_length=25,default="")
    test_wpm=models.IntegerField(default=0)
    test_keystrokes=models.IntegerField(default=0)
    test_accuracy=models.FloatField(default=0)
    correct_count=models.IntegerField(default=0)
    wrong_count=models.IntegerField(default=0)

    def __str__(self):
        return str(self.test_wpm) + " " + "wpm" + " by " + self.login_username

class Contact(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    number=models.IntegerField()
    feedback=models.TextField()

    def __str__(self):
        return "message by " + self.name