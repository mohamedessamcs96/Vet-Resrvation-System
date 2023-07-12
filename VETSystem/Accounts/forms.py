from django import forms
from .models import Client,UserAdmin,Haematology,BloodChemistry,AnalysisPrices,Intestinalparasites,BloodParasaite
from django.contrib.auth.forms import UserCreationForm

from django.forms import formset_factory

class DateInput(forms.DateInput):
    input_type = 'date'

class AdminForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'style': 'max-width: 20em'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'style': 'max-width: 20em'})
    class Meta:
        model = UserAdmin
        #fields='__all__'
        # password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'width: 100%'}))
        # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','style': 'width: 100%'}))        
        fields =('fname','lname','username','email','birthdate','gender','is_admin','is_superuser','is_staff','password1','password2','is_technichal','is_advisor')

        widgets={
                'fname':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'lname':forms.TextInput(attrs={'class':'form-control','style':'max-width: 20em',"id":"","placeholder":""}),
                'email':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'username':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"placeholder":""}),
                'birthdate':DateInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":"29/09/1996"}),
                #'password1':forms.PasswordInput(attrs={'class':'form-control ','style':'max-width: 20em',"placeholder":""}),
                #'password2':forms.PasswordInput(attrs={'class':'form-control ','style':'max-width: 20em',"placeholder":""}),
                'gender': forms.Select(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'is_admin': forms.CheckboxInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":""}),
                'is_superuser': forms.CheckboxInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":""}),
                'is_staff': forms.CheckboxInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'is_advisor': forms.CheckboxInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'is_technichal': forms.CheckboxInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""})
          }  
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['class'] = 'form-control'   
        
     
class AddClient(forms.ModelForm):
    class Meta:
            model = Client
            #fields='__all__'
            fields = ('clientname','phonenumber','animaltype','sampletype','age','notes')
            
            widgets={
                'clientname':forms.TextInput(attrs={'class':'form-control'}),
                'phonenumber':forms.TextInput(attrs={'class':'form-control'}),
                'animaltype':forms.TextInput(attrs={'class':'form-control'}),
                'sampletype':forms.Select(attrs={'class':'form-control'}),
                'age':forms.TextInput(attrs={'class':'form-control'}),
                'notes':forms.TextInput(attrs={'class':'form-control'})
            }
              
class SearchUserForm(forms.Form):
     #phonenumber=forms.CharField()
     #fields=('phonenumber')
    phonenumber=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
            
  



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','name':'password'}))



class AnalysisPricesForm(forms.Form):
    Haematology = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    BIOChemistry = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    Intestinalparasites= forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    BloodParasite= forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    All= forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class IntestinalparasitesForm(forms.ModelForm):
    class Meta:
            model = Intestinalparasites
            fields = ('COCCIDIA','NEMATODE','CESTODE')
            widgets={
                'COCCIDIA':forms.Select(attrs={'class':'form-control','style':''}),
                'NEMATODE':forms.Select(attrs={'class':'form-control','style':''}),
                'CESTODE':forms.Select(attrs={'class':'form-control','style':''}),
            }

class BloodParasaiteForm(forms.ModelForm):
    class Meta:
            model = BloodParasaite
            fields = ('THELERIA','BABESIA','ANAPLASMA','TRYPANOSOMA')
            widgets={
                'THELERIA':forms.Select(attrs={'class':'form-control','style':''}),
                'BABESIA':forms.Select(attrs={'class':'form-control','style':''}),
                'ANAPLASMA':forms.Select(attrs={'class':'form-control','style':''}),
                'TRYPANOSOMA':forms.Select(attrs={'class':'form-control','style':''}),
            }




class HaematologyForm(forms.ModelForm):
     class Meta:
          model=Haematology
          fields =('WBC','LYMPH','MONO','EOSIN','NEUT','RBC','HCT','MCV','MCH','HGB','MCHC','PLT','BAS')

          widgets={
                'WBC':forms.TextInput(attrs={'class':'form-control',}),
                'LYMPH':forms.TextInput(attrs={'class':'form-control'}),
                'MONO':forms.TextInput(attrs={'class':'form-control'}),
                'EOSIN':forms.TextInput(attrs={'class':'form-control'}),
                'NEUT':forms.TextInput(attrs={'class':'form-control'}),
                'RBC':forms.TextInput(attrs={'class':'form-control'}),
                'HCT':forms.TextInput(attrs={'class':'form-control'}),
                'MCV':forms.TextInput(attrs={'class':'form-control'}),
                'MCH':forms.TextInput(attrs={'class':'form-control'}),
                'MCHC':forms.TextInput(attrs={'class':'form-control'}),
                'HGB':forms.TextInput(attrs={'class':'form-control'}),
                'PLT':forms.TextInput(attrs={'class':'form-control'}),
                'BAS':forms.TextInput(attrs={'class':'form-control'}),
            }
          
          #fields='__all__'

class BloodChemistryForm(forms.ModelForm):
     class Meta:
          model=BloodChemistry
          fields =('TotalProtien','Urea','Gluco','Calcium','Ck','LDH','AST_GOT','ALT_GPT','GGT','Phosphorous','Creatinine','IRON','Copper','APL')

          widgets={
                'TotalProtien':forms.TextInput(attrs={'class':'form-control','style':''}),
                'Urea':forms.TextInput(attrs={'class':'form-control','style':''}),
                'Gluco':forms.TextInput(attrs={'class':'form-control','style':''}),
                'Calcium':forms.TextInput(attrs={'class':'form-control','style':''}),
                'Ck':forms.TextInput(attrs={'class':'form-control','style':''}),
                'LDH':forms.TextInput(attrs={'class':'form-control','style':''}),
                'AST_GOT':forms.TextInput(attrs={'class':'form-control','style':''}),
                'ALT_GPT':forms.TextInput(attrs={'class':'form-control','style':''}),
                'GGT':forms.TextInput(attrs={'class':'form-control','style':''}),
                'Phosphorous':forms.TextInput(attrs={'class':'form-control','style':''}),
                'Creatinine':forms.TextInput(attrs={'class':'form-control','style':''}),
                'IRON':forms.TextInput(attrs={'class':'form-control','style':''}),
                'Copper':forms.TextInput(attrs={'class':'form-control','style':''}),
                'APL':forms.TextInput(attrs={'class':'form-control','style':''}),
            }

