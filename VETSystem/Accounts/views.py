from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.http import HttpResponse
import datetime 
from django.contrib.auth.decorators import login_required

# Import these methods
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from rtl import reshaper
from bidi.algorithm import get_display


from django.http import HttpResponse
#from django.utils.translation import gettext as _


from django import forms
from .models import UserAdmin,Client,Report
from .forms import AdminForm,AddClient,SearchUserForm,LoginForm,HaematologyForm,BloodChemistryForm






@login_required(login_url='/login') 
def form_created(request):
    return render(request,'form_created.html')

#Create an error message function
def get_error_message(request):
    password1=request.POST['password1']
    password2=request.POST['password2']
    email=request.POST['email']
    if password1!=password2:
        return "The Passwords didn't match"
    if UserAdmin.objects.filter(email=email).exists():
        return "Email already exists"


# def change_language(request,language_code):
#     request.session['django-language']=language_code
#     print()
#     request.session.save()
#     return redirect(request.META.get('HTTP_REFERER','/'))

# from django.utils.translation import activate

# def switch_language(request, language_code):
#     activate('ar')


# Create your views here.
def register_request(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    #template_name='register.html' if language_code=='en' else 'register-ar.html'
    template_name='register.html'
    if request.user.is_superuser or request.user.is_staff:
        if request.method=="POST":
            form=AdminForm(request.POST)
            if form.is_valid():
                user=form.save()
                login(request,user)
                print("register successful")
                messages.success(request,"Register successful")
                return redirect(f'/{language_code}/form_created/')
            print("unsucessful")
            messages.error(request,get_error_message(request))
            return render(request=request,template_name=template_name,context={'register_form':form})
        else:
            form=AdminForm()
            return render(request=request,template_name=template_name,context={'register_form':form})
    else:
        return render(request=request,template_name='notallowed.html')
 
def logout_request(request):
    logout(request)
    messages.info(request,"You have sucessfully logged out")
    return redirect("login")

# Create your views here.
def login_request(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                print('loggged')
                messages.info(request,f"You are logged as {username}")
                return redirect('homepage')
            else:
                print("Invalid username and password!")
                messages.error(request,"invalid username and password")
        else:
            print("not valid form")
            messages.error(request,"not valid form")

    form=LoginForm()
    return render(request=request,template_name='login.html',context={'login_form':form})
    now = datetime.datetime.now()
    return HttpResponse("html")
def logout_request(request):
    logout(request)
    messages.info(request,"You have sucessfully logged out")
    return redirect("login")


@login_required(login_url='/login/')
def add_client(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name='add_user.html' if language_code=='en' else 'add_user-ar.html'
    """Process images uploaded by users"""
    if request.method == 'POST':
        form = AddClient(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Get the current instance object to display in the template
            img_obj = form.instance
            print(request.POST)
            #img = request.FILES['image']
            
            return redirect(f'/{language_code}/form_created/')
            #return render(request, 'add_user.html', {'form': form,'img_obj': img_obj})
        return render(request,template_name , {'form': form})
        
    else:
        form = AddClient()
        return render(request, template_name, {'form': form})


from django.utils.translation import activate

@login_required(login_url='/login') 
def home_page(request):
    #lang = request.GET.get('lang', 'en')  # Default to English if the language is not specified
    #activate(lang)
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name='home.html' if language_code=='en' else 'home-ar.html'
    return render(request,template_name)


@login_required(login_url='/login/')
def search_user(request):
    if request.method == 'POST':
        form=SearchUserForm(request.POST)
        print(request.POST['clientnumber'])
        print(type(request.POST['clientnumber']))
        clientnumber=(request.POST['clientnumber'])
        print(type(clientnumber))
        print("user")
        users=Client.objects.filter(clientnumber=clientnumber)
        user=Client.objects.get(clientnumber=clientnumber)
        
        if user!=None: 
            context={'form':form,'users':users,'user':user}
            return render(request,'history.html',context)
        else:
            return HttpResponse("No user found")
    
    form=SearchUserForm()
    return render(request,'historyform.html',{'form':form})


"""
def create_form(request):
    if request.method=='POST':
        form=FormCreationForm(request.POST)
        dynamic_formset=DynamicFieldFormSet(request.POST)
        if form.is_valid() and dynamic_formset.is_valid():
            form_instance=form.save()
            for dynamic_form in dynamic_formset:
                dynamic_field=dynamic_form.save(commit=False)
                dynamic_field.form=form_instance
                dynamic_field.save()

            return redirect('form_created')

    else:
        form=FormCreationForm()
        dynamic_formset=DynamicFieldFormSet()

    return render(request,'create_form.html',{'form':form,'dynamic_formset':dynamic_formset})

"""



@login_required(login_url='/login/')
def Haematology(request,pk):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name='hame_tology.html' if language_code=='en' else 'hame_tology.html'
    """Process images uploaded by users"""
    form = HaematologyForm()
    if request.method == 'POST':
        form = HaematologyForm(request.POST)
        if form.is_valid():
            Haematology=form.save(commit=False)  
            client=Client.objects.get(clientnumber=pk) 
            Haematology.admin=request.user
            Haematology.client=client
            Haematology.save()
            
            # Get the current instance object to display in the template
            img_obj = form.instance
            return redirect(f'/{language_code}/form_created/')
            #return render(request, 'add_user.html', {'form': form,'img_obj': img_obj})
       
        print(form.errors.as_data())
        return render(request,template_name , {'form': form})
    return render(request,template_name , {'form': form})    
  
@login_required(login_url='/login/')
def BloodChemistry(request,pk):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name='bio_chemestry.html' if language_code=='en' else 'bio_chemestry.html'
    """Process images uploaded by users"""
    form = BloodChemistryForm()
    if request.method == 'POST':
        form = BloodChemistryForm(request.POST)
        if form.is_valid():
            BloodChemistry=form.save(commit=False)   
            client=Client.objects.get(clientnumber=pk)
            BloodChemistry.admin=request.user
            BloodChemistry.client=client
            BloodChemistry.save()
            
            # Get the current instance object to display in the template
            img_obj = form.instance
            return redirect(f'/{language_code}/form_created/')
            #return render(request, 'add_user.html', {'form': form,'img_obj': img_obj})
       
        print(form.errors.as_data())
        return render(request,template_name , {'form': form})
    return render(request,template_name , {'form': form})    
  




def create_report_ar(request,pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EmplyeeReport.pdf"'

    usertable=Client.objects.get(clientnumber=pk)
    

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('22016-adobearabic', '/Users/mac/Desktop/VETReservaton/VETSystem/static/webfonts/22016-adobearabic.ttf'))
    from rtl import reshaper
    
    #pdfmetrics.registerFontFamily('ArabicFamily', normal='ArabicFont', bold='ArabicFont', italic='ArabicFont', boldItalic='ArabicFont')
    from bidi.algorithm import get_display


    # Set outline parameters
    outline_x = 50
    outline_y = 50
    outline_width = 700
    outline_height = 700
    outline_thickness = 2

    # Draw outline rectangle
    p.setStrokeColorRGB(0, 0, 0)  # Set outline color (black in this example)
    p.setLineWidth(outline_thickness)  # Set outline thickness
    p.rect(outline_x, outline_y, outline_width, outline_height)

    p.setPageSize((800, 800)) 
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #reshaped_text=reshaper.reshape("العميل")
    
    arabic_text_display=reshaper.reshape(f'العميل {usertable.clientname}')
    arabic_text_display = get_display(arabic_text_display)
    #reshaped_text=arabic_reshaper.reshape(arabic_text_display)
    p.setFont('22016-adobearabic',35)
    
    p.drawString(370,700, f'   {arabic_text_display}  ')
    
    arabic_text_display=reshaper.reshape(f"رقم:{usertable.clientnumber}")
    arabic_text_display = get_display(arabic_text_display)
    p.setFont('22016-adobearabic',15)
    p.drawString(650,650, f" {arabic_text_display}")

    arabic_text_display=reshaper.reshape(f"نوع الحيوان:{usertable.animaltype}")
    arabic_text_display = get_display(arabic_text_display)
    p.drawString(650,550, f"{arabic_text_display}")
    
    arabic_text_display=reshaper.reshape(f'نوع العينه:{usertable.sampletype}')
    arabic_text_display = get_display(arabic_text_display)
    p.drawString(650,450, f" {arabic_text_display}")

    arabic_text_display=reshaper.reshape(f'عمرر الحيوان: {usertable.age}')
    arabic_text_display = get_display(arabic_text_display)
    p.drawString(650,350, f"  {arabic_text_display}")

    arabic_text_display=reshaper.reshape(f'ملحوظه: {usertable.notes}')
    arabic_text_display = get_display(arabic_text_display)
    p.drawString(620,250, f"  {arabic_text_display}")
    
    arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
    arabic_text_display = get_display(arabic_text_display)
    #reshaped_text=arabic_reshaper.reshape(arabic_text_display)
    p.setFont('22016-adobearabic',20)
    
    p.drawString(310,100, f' {arabic_text_display}  ')
    

    # save the pdf file
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return redirect('/form_created')




def create_report(request,pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EmplyeeReport.pdf"'

    usertable=Client.objects.get(clientnumber=pk)
    

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    
    #pdfmetrics.registerFontFamily('ArabicFamily', normal='ArabicFont', bold='ArabicFont', italic='ArabicFont', boldItalic='ArabicFont')
    from bidi.algorithm import get_display


    # Set outline parameters
    outline_x = 50
    outline_y = 50
    outline_width = 700
    outline_height = 700
    outline_thickness = 2

    # Draw outline rectangle
    p.setStrokeColorRGB(0, 0, 0)  # Set outline color (black in this example)
    p.setLineWidth(outline_thickness)  # Set outline thickness
    p.rect(outline_x, outline_y, outline_width, outline_height)

    p.setPageSize((800, 800)) 
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    #reshaped_text=reshaper.reshape("العميل")
    
 
    p.setFont('Helvetica',35)
    p.drawString(270,700, f' Client name {usertable.clientname}  ')
    
    p.setFont('Helvetica',20)
    p.drawString(70,650, f" Number:{usertable.clientnumber}")

  
    p.drawString(70,550, f"Animal Type {usertable.animaltype}")
    

    p.drawString(70,450, f" Sample Type {usertable.sampletype}")


    p.drawString(70,350, f'Animal Age: {usertable.age}')

    p.drawString(70,250, (f'Notes: {usertable.notes}'))


    pdfmetrics.registerFont(TTFont('22016-adobearabic', '/Users/mac/Desktop/VETReservaton/VETSystem/static/webfonts/22016-adobearabic.ttf'))
    arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
    arabic_text_display = get_display(arabic_text_display)
    #reshaped_text=arabic_reshaper.reshape(arabic_text_display)
    
    p.setFont('22016-adobearabic',20)
    
    p.drawString(310,100, f' {arabic_text_display}  ')
    

    # save the pdf file
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response 



