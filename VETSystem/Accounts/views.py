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
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph,Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image
from arabic_reshaper import reshape

from django.http import HttpResponse


from django import forms
from .models import UserAdmin,Client,Report
from .forms import AdminForm,AddClient,SearchUserForm,LoginForm,HaematologyForm,BloodChemistryForm







@login_required(login_url='/ar/login/')
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




# Create your views here.

@login_required(login_url='/ar/login/')
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


@login_required(login_url='/ar/login/')
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


@login_required(login_url='/ar/login/')
def home_page(request):
    #lang = request.GET.get('lang', 'en')  # Default to English if the language is not specified
    #activate(lang)
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name='home.html' if language_code=='en' else 'home-ar.html'
    return render(request,template_name)


@login_required(login_url='/ar/login/')
def search_user(request):
    if request.method == 'POST':
        form=SearchUserForm(request.POST)
        print(request.POST['phonenumber'])
        print(type(request.POST['phonenumber']))
        phonenumber=(request.POST['phonenumber'])
        print(type(phonenumber))
        print("user")
        users=Client.objects.filter(phonenumber=phonenumber)
        user=Client.objects.get(phonenumber=phonenumber)
        
        if user!=None: 
            context={'form':form,'users':users,'user':user}
            return render(request,'history.html',context)
        else:
            return HttpResponse("No user found")
    
    form=SearchUserForm()
    return render(request,'historyform.html',{'form':form})



from .forms import IntestinalparasitesForm,BloodParasaiteForm


@login_required(login_url='/ar/login/')
def Blood_Parasite(request,pk):
    #language_code = request.path.split('/')[1]  # Extract the first part of the path
    """Process images uploaded by users"""
    form = BloodParasaiteForm()
    if request.method == 'POST':
        form = BloodParasaiteForm(request.POST)
        if form.is_valid():
            BloodParasaite=form.save(commit=False)  
            client=Client.objects.get(clientnumber=pk) 
            BloodParasaite.admin=request.user
            BloodParasaite.client=client
            BloodParasaite.save()
            
            THELERIA=request.POST['THELERIA']
            BABESIA=request.POST['BABESIA']
            ANAPLASMA=request.POST['ANAPLASMA']
            TRYPANOSOMA=request.POST['TRYPANOSOMA']
        
            
            """
            Create Table here
            """
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="EmployeeReport.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 

           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))
      
            IntestinalparasitesTable=[
                [get_display(reshape('Value القيمه')),get_display(reshape('Type نوع التحليل'))],
                [THELERIA,'THELERIA '],
                [BABESIA,'BABESIA '],
                [ANAPLASMA,'ANAPLASMA'],
                [TRYPANOSOMA,'TRYPANOSOMA'],
                ]

            # Define table style
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

         
            BloodParasaiteTable = Table(IntestinalparasitesTable)
            # Increase table size by specifying the width and height
           

            # Create table object and apply style
            bloodParasaiteTable = Table(BloodParasaiteTable, colWidths=[200, 200])  # Specify column widths here
            bloodParasaiteTable.setStyle(table_style)

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 

            # Add a spacer with horizontal space of 50 points
            spacer = Spacer(50, 50)
           
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            #logo_path = settings.MEDIA_URL + 'img/logo.jpg'  # Replace with the actual path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image
            # Set the desired width and height of the logo (optional)
  

            # Set the logo's position to the left side of the page
       
            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)        
            arabic_text_display = get_display(reshaper.reshape(f' Name: {client.clientname}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            arabic_text_display = get_display(reshaper.reshape(f' Client Number: {client.clientnumber}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Type: {client.animaltype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Sample Type: {client.sampletype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Age: {client.age}'))
            story.append(Paragraph(arabic_text_display,custom_style))


            arabic_text_display = get_display(reshaper.reshape(f' Notes: {client.notes}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            story.append(spacer)
            story.append(bloodParasaiteTable)
            story.append(spacer)
            story.append(spacer)
            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            # Build the PDF document
            doc.build(story)



            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response
     

        print(form.errors.as_data())
        return render(request,'blood_parasite.html' , {'form': form})
    return render(request,'blood_parasite.html' , {'form': form}) 








@login_required(login_url='/ar/login/')
def Intestinalparasites(request,pk):
    #language_code = request.path.split('/')[1]  # Extract the first part of the path
    """Process images uploaded by users"""
    form = IntestinalparasitesForm()
    if request.method == 'POST':
        form = IntestinalparasitesForm(request.POST)
        if form.is_valid():
            Intestinalparasites=form.save(commit=False)  
            client=Client.objects.get(clientnumber=pk) 
            Intestinalparasites.admin=request.user
            Intestinalparasites.client=client
            Intestinalparasites.save()
            
            COCCIDIA=request.POST['COCCIDIA']
            NEMATODE=request.POST['NEMATODE']
            CESTODE=request.POST['CESTODE']
        
            
            """
            Create Table here
            """
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="EmployeeReport.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 

           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))
      
            IntestinalparasitesTable=[
                [get_display(reshape('Value القيمه')),get_display(reshape('Type نوع التحليل'))],
                [COCCIDIA,'COCCIDIA '],
                [NEMATODE,'NEMATODE '],
                [CESTODE,'CESTODE'],
       
                ]

            # Define table style
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

         
            intestinalparasitesTable = Table(IntestinalparasitesTable)
            # Increase table size by specifying the width and height
           

            # Create table object and apply style
            intestinalparasitesTable = Table(IntestinalparasitesTable, colWidths=[200, 200])  # Specify column widths here
            intestinalparasitesTable.setStyle(table_style)

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 

            # Add a spacer with horizontal space of 50 points
            spacer = Spacer(50, 50)
           
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            #logo_path = settings.MEDIA_URL + 'img/logo.jpg'  # Replace with the actual path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image
            # Set the desired width and height of the logo (optional)
  

            # Set the logo's position to the left side of the page
       
            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)        
            arabic_text_display = get_display(reshaper.reshape(f' Name: {client.clientname}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            arabic_text_display = get_display(reshaper.reshape(f' Client Number: {client.clientnumber}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Type: {client.animaltype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Sample Type: {client.sampletype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Age: {client.age}'))
            story.append(Paragraph(arabic_text_display,custom_style))


            arabic_text_display = get_display(reshaper.reshape(f' Notes: {client.notes}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            story.append(spacer)
            story.append(intestinalparasitesTable)
            story.append(spacer)
            story.append(spacer)
            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            # Build the PDF document
            doc.build(story)



            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response
     

        print(form.errors.as_data())
        return render(request,'intestinal_parasites.html' , {'form': form})
    return render(request,'intestinal_parasites.html' , {'form': form}) 








@login_required(login_url='/ar/login/')
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
            
            WBC=request.POST['WBC']
            LYMPH=request.POST['LYMPH']
            MONO=request.POST['MONO']
            HCT=request.POST['HCT']
            MCV=request.POST['MCV']
            MCH=request.POST['MCH']
            MCHC=request.POST['MCHC']
            PLT=request.POST['PLT']
            HGB=request.POST['HGB']
            EOSIN=request.POST['EOSIN']
            NEUT=request.POST['NEUT']
            RBC=request.POST['RBC']
            
            """
            Create Table here
            """
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="EmployeeReport.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 

           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))
      
            HaematologyTable=[
                [get_display(reshape('Value القيمه')),get_display(reshape('Type نوع التحليل'))],
                [WBC,'WBC '],
                [LYMPH,'LYMPH '],
                [MONO,'MONO'],
                [HCT,'HCT'],
                [MCV,'MCV'],
                [MCH,'MCH'],
                [MCHC,'MCHC'],
                [PLT,'PLT'],
                [HGB,'HGB'],
                [EOSIN,'EOSIN'],
                [NEUT,'NEUT'],
                [RBC,'RBC']
                ]

            # Define table style
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

         
            haematologytable = Table(HaematologyTable)
            # Increase table size by specifying the width and height
           

            # Create table object and apply style
            haematologytable = Table(HaematologyTable, colWidths=[200, 200])  # Specify column widths here
            haematologytable.setStyle(table_style)

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 

            # Add a spacer with horizontal space of 50 points
            spacer = Spacer(50, 50)
           
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            #logo_path = settings.MEDIA_URL + 'img/logo.jpg'  # Replace with the actual path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image
            # Set the desired width and height of the logo (optional)
  

            # Set the logo's position to the left side of the page
       
            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)        
            arabic_text_display = get_display(reshaper.reshape(f' Name: {client.clientname}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            arabic_text_display = get_display(reshaper.reshape(f' Client Number: {client.clientnumber}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Type: {client.animaltype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Sample Type: {client.sampletype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Age: {client.age}'))
            story.append(Paragraph(arabic_text_display,custom_style))


            arabic_text_display = get_display(reshaper.reshape(f' Notes: {client.notes}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            story.append(spacer)
            story.append(haematologytable)
            story.append(spacer)
            story.append(spacer)
            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            # Build the PDF document
            doc.build(story)



            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response
     

        print(form.errors.as_data())
        return render(request,template_name , {'form': form})
    return render(request,template_name , {'form': form})    
  

@login_required(login_url='/ar/login/')
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

            TotalProtien=request.POST['TotalProtien']
            Urea=request.POST['Urea']
            Gluco=request.POST['Gluco']
            Calcium=request.POST['Calcium']
            Ck=request.POST['Ck']
            LDH=request.POST['LDH']
            AST_GOT=request.POST['AST_GOT']
            ALT_GPT=request.POST['ALT_GPT']
            Albumin=request.POST['Albumin']
            Phosphorous=request.POST['Phosphorous']
            Creatinine=request.POST['Creatinine']
            IRON=request.POST['IRON']
            
            """
            Create Table here
            """
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="EmployeeReport.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 

           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))
      
            BloodChemistryTable=[
                [get_display(reshape('Value القيمه')),get_display(reshape('Type النوع '))],
                [TotalProtien,'TotalProtien '],
                [Urea,'Urea '],
                [Gluco,'Gluco'],
                [Calcium,'Calcium'],
                [Ck,'Ck'],
                [LDH,'LDH'],
                [AST_GOT,'AST_GOT'],
                [ALT_GPT,'ALT_GPT'],
                [Albumin,'Albumin'],
                [Phosphorous,'Phosphorous'],
                [Creatinine,'Creatinine'],
                [IRON,'IRON']
                ]

            # Define table style
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])

            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

         
            bloodchemistrytable = Table(BloodChemistryTable)
            # Increase table size by specifying the width and height
           

            # Create table object and apply style
            bloodchemistrytable = Table(BloodChemistryTable, colWidths=[200, 200])  # Specify column widths here
            bloodchemistrytable.setStyle(table_style)

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 

            # Add a spacer with horizontal space of 50 points
            spacer = Spacer(50, 50)
           
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            #logo_path = settings.MEDIA_URL + 'img/logo.jpg'  # Replace with the actual path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image
            # Set the desired width and height of the logo (optional)
  

            # Set the logo's position to the left side of the page
       
            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)        
            arabic_text_display = get_display(reshaper.reshape(f' Name: {client.clientname}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            arabic_text_display = get_display(reshaper.reshape(f' Client Number: {client.clientnumber}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Type: {client.animaltype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Sample Type: {client.sampletype}'))
            story.append(Paragraph(arabic_text_display,custom_style))

            arabic_text_display = get_display(reshaper.reshape(f' Animal Age: {client.age}'))
            story.append(Paragraph(arabic_text_display,custom_style))


            arabic_text_display = get_display(reshaper.reshape(f' Notes: {client.notes}'))
            story.append(Paragraph(arabic_text_display,custom_style))
            story.append(spacer)
            story.append(bloodchemistrytable)
            story.append(spacer)
            story.append(spacer)
            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            # Build the PDF document
            doc.build(story)



            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response
     


            # Get the current instance object to display in the template
            img_obj = form.instance
            #return redirect(f'/{language_code}/form_created/')
            #return render(request, 'add_user.html', {'form': form,'img_obj': img_obj})
       
        print(form.errors.as_data())
        return render(request,template_name , {'form': form})
    return render(request,template_name , {'form': form})    
  



@login_required(login_url='/ar/login/')
def create_report(request,pk):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="EmplyeeReport.pdf"'
    buffer = BytesIO()
    # Set the desired margin size (in this example, 1 inch)
    margin_size = 0.5 * inch
    # Create the PDF object
    doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
    


           

    # Load custom font file for Arabic text
    font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
    print(font_path)
    pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))

   
   
    # Create a custom ParagraphStyle
    custom_style = ParagraphStyle(
        name='CustomStyle',
        fontName='22016-adobearabic',  # Specify your custom font name
        fontSize=14,  # Specify the font size
        textColor=colors.black,  # Specify the font color
        spaceBefore=12,  # Specify the space before the paragraph
        spaceAfter=6,  # Specify the space after the paragraph
    )
    # Define a style for center-aligned paragraph
    center_style = ParagraphStyle(
        name='CustomStyle',
        fontName='22016-adobearabic',  # Specify your custom font name
        fontSize=14,  # Specify the font size
        textColor=colors.blue,  # Specify the font color
        spaceBefore=12,  # Specify the space before the paragraph
        spaceAfter=6,  # Specify the space after the paragraph
        alignment=1
    )

         


    # Add simple strings above the table
    client=Client.objects.get(clientnumber=pk) 

    # Add a spacer with horizontal space of 50 points
    spacer = Spacer(50, 50)
    
    # Build the story containing the table
    story = []    
    # Define the path to your logo image file
    #logo_path = settings.MEDIA_URL + 'img/logo.jpg'  # Replace with the actual path to your logo image file
    logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
    # Create an Image object with the logo image



    # Set the logo's position to the left side of the page

    logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
    logo_image.hAlign = 'RIGHT'
    # Add the logo image to the story before the table
    story.append(logo_image)        
    arabic_text_display = get_display(reshaper.reshape(f' Name: {client.clientname}'))
    story.append(Paragraph(arabic_text_display,custom_style))
    arabic_text_display = get_display(reshaper.reshape(f' Client Number: {client.clientnumber}'))
    story.append(Paragraph(arabic_text_display,custom_style))

    arabic_text_display = get_display(reshaper.reshape(f' Animal Type: {client.animaltype}'))
    story.append(Paragraph(arabic_text_display,custom_style))

    arabic_text_display = get_display(reshaper.reshape(f' Animal Sample Type: {client.sampletype}'))
    story.append(Paragraph(arabic_text_display,custom_style))

    arabic_text_display = get_display(reshaper.reshape(f' Animal Age: {client.age}'))
    story.append(Paragraph(arabic_text_display,custom_style))


    arabic_text_display = get_display(reshaper.reshape(f' Notes: {client.notes}'))
    story.append(Paragraph(arabic_text_display,custom_style))
    story.append(spacer)
    story.append(spacer)
    story.append(spacer)
    arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
    arabic_text_display = get_display(arabic_text_display)
    story.append(Paragraph(arabic_text_display,center_style))
    # Build the PDF document
    doc.build(story)
   



    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response