from django.db import models

# Create your models here.
employeerole = (
    ('admin','admin'),
    ('employee','employee'),
)


class Account(models.Model):
    username = models.CharField(max_length=255,default = "")
    email = models.EmailField(max_length=255,default = "")
    password = models.TextField(max_length=255,default = "")
    role = models.CharField(choices=employeerole,max_length=20,default="employee")
    
   
    def __str__(self):
        return self.username



class Questions(models.Model):

    question = models.TextField(default="")
    Accouuntid = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    
class Answer(models.Model):
    answer = models.TextField(default="")
    Qid = models.ForeignKey(Questions,on_delete=models.CASCADE,blank=True,null=True)
    Accouuntid = models.ForeignKey(Account,on_delete=models.CASCADE,blank=True,null=True)
    

    