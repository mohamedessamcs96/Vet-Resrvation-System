from django import forms
from .models import Client,UserAdmin


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