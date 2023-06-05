from django import forms
from .models import Client,UserAdmin,Haematology,BloodChemistry

from django.forms import formset_factory

class DateInput(forms.DateInput):
    input_type = 'date'

class AdminForm(forms.ModelForm):

    class Meta:
        model = UserAdmin
        #fields='__all__'
        fields =('fname','lname','username','birthdate','gender','is_admin','is_superuser','is_staff','password1','password2','is_technichal','is_advisor')

        widgets={
                'fname':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'lname':forms.TextInput(attrs={'class':'form-control','style':'max-width: 20em',"id":"","placeholder":""}),
                #'email':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":"email"}),
                'username':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'birthdate':DateInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":"29/09/1996"}),
                'password1':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'password2':forms.TextInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'gender': forms.Select(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'is_admin': forms.CheckboxInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":""}),
                'is_superuser': forms.CheckboxInput(attrs={'class':'form-control ','style':' max-width: 20em',"id":"","placeholder":""}),
                'is_staff': forms.CheckboxInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'is_advisor': forms.CheckboxInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""}),
                'is_technichal': forms.CheckboxInput(attrs={'class':'form-control ','style':'max-width: 20em',"id":"","placeholder":""})
          }     
        
     
class AddClient(forms.ModelForm):
    class Meta:
            model = Client
            #fields='__all__'
            fields = ('clientname','phonenumber','animaltype','sampletype','age','notes')
            
            widgets={
                'clientname':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'phonenumber':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'animaltype':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'sampletype':forms.Select(attrs={'class':'form-control','style':'width:70%'}),
                'age':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'notes':forms.TextInput(attrs={'class':'form-control','style':'width:70%'})
            }
              
class SearchUserForm(forms.Form):
     clientnumber=forms.IntegerField()
     fields=('clientnumber')
     widgets={
        'clientnumber':forms.TextInput(attrs={'class':'form-control'})
            
     }



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class HaematologyForm(forms.ModelForm):
     class Meta:
          model=Haematology
          fields =('WBC','LYMPH','MONO','EOSIN','NEUT','RBC','HCT','MCV','MCH','HGB','MCHC','PLT')

          widgets={
                'WBC':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'LYMPH':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'MONO':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'EOSIN':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'NEUT':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'RBC':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'HCT':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'MCV':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'MCH':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'MCHC':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'HGB':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'PLT':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
            }
          
          #fields='__all__'

class BloodChemistryForm(forms.ModelForm):
     class Meta:
          model=BloodChemistry
          fields =('TotalProtien','Urea','Gluco','Calcium','Ck','LDH','AST_GOT','ALT_GPT','Albumin','Phosphorous','Creatinine','IRON')

          widgets={
                'TotalProtien':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'Urea':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'Gluco':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'Calcium':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'Ck':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'LDH':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'AST_GOT':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'ALT_GPT':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'Albumin':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'Phosphorous':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'Creatinine':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
                'IRON':forms.TextInput(attrs={'class':'form-control','style':'width:70%'}),
            }


"""
class DynamicFieldForm(forms.ModelForm):
     class Meta:
          model=DynamicField
          fields='__all__'



DynamicFieldFormSet=formset_factory(DynamicFieldForm,extra=1)


class FormCreationForm(forms.ModelForm):
     class Meta:
          model=DynamicForm
          #fields=['title']
          fields='__all__'
"""