from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
# Create your models here.

GENDER_CHOICES=(
        ('m','male'),
        ('f','female')
    )


ANIMAL_SAMPLES=(
    ('h','Haematology'),
    ('b','BIOChemistry'),
    ('i','Intestinalparasites'),
    ('p','BloodParasaite'),
    ('a','All')
)

class AnalysisPrices(models.Model):
    Haematology=models.IntegerField()
    BIOChemistry=models.IntegerField()
    Intestinalparasites=models.IntegerField()
    BloodParasaite=models.IntegerField()
    All=models.IntegerField()



# Create your models here.

class UserAdmin(AbstractUser):
    fname=models.CharField(max_length=18,default='')
    lname=models.CharField(max_length=18,default='')
    email=models.EmailField(unique=True,null=False)
    gender=models.CharField(max_length=1,choices=GENDER_CHOICES)
    birthdate=models.DateField(null=True)
    is_staff=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_technichal=models.BooleanField(default=False)
    is_advisor=models.BooleanField(default=False)
    password1=models.CharField(max_length=20)
    password2=models.CharField(max_length=20)
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.fname + ' '+self.lname
    

class Client(models.Model):
    admin=models.ForeignKey(UserAdmin,on_delete=models.CASCADE,null=True)
    clientnumber=models.AutoField(unique=True,primary_key=True)
    clientname = models.CharField(max_length=200)
    phonenumber  = models.CharField(max_length=200)
    animaltype  = models.CharField(max_length=10)
    sampletype=models.CharField(max_length=1,choices=ANIMAL_SAMPLES)
    age=models.IntegerField(null=True)
    #sampletype = models.ImageField(upload_to='images')
    notes=models.CharField(max_length=150)
    created=models.DateTimeField(auto_now_add=True)
 

    def __str__(self):
        return str(self.clientnumber)



class Report(models.Model):
    title=models.CharField(max_length=20)
    notes=models.CharField(max_length=100)
    image = models.ImageField(upload_to='images',null=True)
    created=models.DateTimeField(auto_now_add=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.title
    



class Haematology(models.Model):
    admin=models.ForeignKey(UserAdmin,on_delete=models.CASCADE,null=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    created=models.DateTimeField(auto_now_add=True)
    WBC=models.FloatField()
    LYMPH=models.FloatField()
    MONO=models.FloatField()
    EOSIN=models.FloatField()
    NEUT=models.FloatField()
    RBC=models.FloatField()
    HGB=models.FloatField()
    HCT= models.FloatField()
    MCV=models.FloatField()
    MCH=models.FloatField()
    MCHC=models.FloatField()
    PLT=models.FloatField()


class BloodChemistry(models.Model):
    admin=models.ForeignKey(UserAdmin,on_delete=models.CASCADE,null=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    created=models.DateTimeField(auto_now_add=True)
    TotalProtien=models.FloatField()
    Urea=models.FloatField()
    Gluco=models.FloatField()
    Calcium=models.FloatField()
    Ck=models.FloatField()
    LDH=models.FloatField()
    AST_GOT=models.FloatField()
    ALT_GPT= models.FloatField()
    Albumin=models.FloatField()
    Phosphorous=models.FloatField()
    Creatinine=models.FloatField()
    IRON=models.FloatField()


CHOICES=(
    ('F','Found'),
    ('N','Not Found')
)
class Intestinalparasites(models.Model):
    admin=models.ForeignKey(UserAdmin,on_delete=models.CASCADE,null=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    created=models.DateTimeField(auto_now_add=True)
    COCCIDIA=models.CharField(max_length=1,choices=CHOICES)
    NEMATODE=models.CharField(max_length=1,choices=CHOICES)
    CESTODE=models.CharField(max_length=1,choices=CHOICES)



BLOOD_CHOICES=(
    ('P','Positive'),
    ('N','Negative')
)
class BloodParasaite(models.Model):
    admin=models.ForeignKey(UserAdmin,on_delete=models.CASCADE,null=True)
    client=models.ForeignKey(Client,on_delete=models.CASCADE,null=True)
    created=models.DateTimeField(auto_now_add=True)
    THELERIA=models.CharField(max_length=1,choices=BLOOD_CHOICES)
    BABESIA=models.CharField(max_length=1,choices=BLOOD_CHOICES)
    ANAPLASMA=models.CharField(max_length=1,choices=BLOOD_CHOICES)  
    TRYPANOSOMA=models.CharField(max_length=1,choices=BLOOD_CHOICES)  
     


