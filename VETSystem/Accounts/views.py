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
from reportlab.graphics.shapes import Drawing, Line

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image
from arabic_reshaper import reshape

from django.http import HttpResponse


from django import forms
from .models import UserAdmin,Client,Report
from .forms import AdminForm,AddClient,AnalysisPricesForm,SearchUserForm,LoginForm,HaematologyForm,BloodChemistryForm,IntestinalparasitesForm,BloodParasaiteForm







@login_required(login_url='/ar/login/')
def admin_panel(request):
    return render(request,'admin_panel.html')

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

    if request.user.is_superuser or request.user.is_admin:
        if request.method=="POST":
            form=AdminForm(request.POST)
            if form.is_valid():
                user=form.save()
                print(user)
                print(request.POST)

       

                print("register successful")
                messages.success(request,"Register successful")
                # Add the logo image to the story before the table
                username=request.POST['username']        
                usernametext = username
                password=request.POST['password1']        
                passwordtext = password
                
                """
                Create Table here
                """

                # Add simple strings above the table
                #client=Client.objects.get(clientnumber=pk) 
                # Create the HttpResponse object with the appropriate PDF headers.
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="User Login Data.pdf"'

                # Create a PDF document object
            
                buffer = BytesIO()
                # Set the desired margin size (in this example, 1 inch)
                margin_size = 0.5 * inch
                # Create the PDF object
                doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                            topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
                
    
                # Create a custom ParagraphStyle
                custom_style = ParagraphStyle(
                    name='CustomStyle',
                    fontName='22016-adobearabic',  # Specify your custom font name
                    fontSize=14,  # Specify the font size
                    textColor=colors.black,  # Specify the font color
                    alignment=2,
            
                )
                # Define a style for center-aligned paragraph
                center_style = ParagraphStyle(
                    name='CustomStyle',
                    fontName='22016-adobearabic',  # Specify your custom font name
                    fontSize=16,  # Specify the font size
                    textColor=colors.blue,  # Specify the font color
                    spaceBefore=12,  # Specify the space before the paragraph
                    spaceAfter=6,  # Specify the space after the paragraph
                    alignment=1
                )

                # Define a style for center-aligned paragraph
            # Define a style for center-aligned paragraph
                head_style = ParagraphStyle(
                    name='head_style',
                    fontName='22016-adobearabic',  # Specify your custom font name
                    fontSize=20,  # Specify the font size
                    textColor=colors.black,  # Specify the font color
                    spaceBefore=12,  # Specify the space before the paragraph
                    spaceAfter=6,  # Specify the space after the paragraph
                    alignment=1
                )  
            

                # Load custom font file for Arabic text
                font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
                print(font_path)
                pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))










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

            


    



                # Add a spacer with horizontal space of 50 points
                spacer = Spacer(50, 50)
                
                # Build the story containing the table
                story = []    
                # Define the path to your logo image file
                logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
                # Create an Image object with the logo image



                # Set the logo's position to the left side of the page

                logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
                logo_image.hAlign = 'RIGHT'
                # Add the logo image to the story before the table
                story.append(logo_image)     

                arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
                arabic_text_display = get_display(arabic_text_display)
                story.append(Paragraph(arabic_text_display,head_style))
                

                story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
                story.append(spacer)
                arabic_text_display=reshaper.reshape('  بيانات العميل ')
                arabic_text_display = get_display(arabic_text_display)
                story.append(Paragraph(arabic_text_display,head_style))
                story.append(spacer)

                now=datetime.datetime.now()
                arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))


                # Create a table with three rows and two cells
                info_table_data = [
                    [Paragraph('Username', custom_style), Paragraph(usernametext, custom_style)],
                    [Paragraph('Password', custom_style), Paragraph(passwordtext, custom_style)],

                ]
                info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
                info_table_data_style= TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                            ('FONTSIZE', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding for all cells
                            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding for all cells
                        ])
                info_table_data.setStyle(info_table_data_style)
                # Set the row heights

                # Add the table to the story
                story.append(info_table_data)
                # Add the table to the story
    
                story.append(spacer)
                story.append(spacer)  
                story.append(spacer)  
                story.append(spacer)  
                


                line_table_data = [['']]  # Empty cell content
                line_table_style = TableStyle([
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
                    ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
                ])
                line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
                line_table.setStyle(line_table_style)  # Apply the table style
                story.append(line_table)
        
                logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
                # Create an Image object with the logo image
                # Set the logo's position to the left side of the page
                
                story.append(spacer)  

                logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
                # Add the logo image to the story before the table
                story.append(logo_image)  




                arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
                arabic_text_display = get_display(arabic_text_display)
                story.append(Paragraph(arabic_text_display,center_style))
                story.append(Paragraph('0503721656 / 0537308922',center_style))
                # Build the PDF document
                doc.build(story)


                print("REport didn't work")
                # Get the value of the BytesIO buffer and write it to the response
                pdf = buffer.getvalue()
                buffer.close()
                response.write(pdf)
                
                return response




            #return redirect(f'/{language_code}/form_created/')
            print("unsucessful")
            messages.error(request,get_error_message(request))
            return render(request=request,template_name='register.html',context={'register_form':form})
        else:
            form=AdminForm()
            return render(request=request,template_name='register.html',context={'register_form':form})
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
        print(request.POST)
        print(form.is_bound)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username, password=password)

            #username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            print(username)
            print(password)
            #user=authenticate(username=username,password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}")
                return redirect('homepage')
            else:
                messages.error(request, "Invalid username and password!")
        else:
            messages.error(request, "Invalid form")

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
            phonenumber=request.POST['phonenumber']
            
           
            client=Client.objects.get(phonenumber=phonenumber)

            return redirect('getchecked', pk=client.clientnumber)
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

def about(request):
    return render(request,'about.html')

def contactus(request):
    return render(request,'contact.html')

from .models import AnalysisPrices

@login_required(login_url='/ar/login/')
def add_price(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
        # Retrieve the AnalysisPrices object
    analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
    
    
    # Create an instance of the form with initial values
    form = AnalysisPricesForm(initial={
        'Haematology': analysis_prices.Haematology,
        'BIOChemistry': analysis_prices.BIOChemistry,
        'Intestinalparasites': analysis_prices.Intestinalparasites,
        'BloodParasite': analysis_prices.BloodParasaite,
        'All': analysis_prices.All
    })
    if request.method == 'POST':
        # Update the values of AnalysisPrices object
        analysis_prices.Haematology = request.POST['Haematology']
        analysis_prices.BIOChemistry = request.POST['BIOChemistry']
        analysis_prices.Intestinalparasites = request.POST['Intestinalparasites']
        analysis_prices.BloodParasite = request.POST['BloodParasite']
        analysis_prices.All = request.POST['All']
        analysis_prices.save()
        #return redirect(f'/{language_code}/')
    
    
    #form=AnalysisPricesForm()
    return render(request,'add_price.html',{'form':form})


@login_required(login_url='/ar/login/')
def search_user(request):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    if request.method == 'POST':
        form=SearchUserForm(request.POST)
        print(request.POST['phonenumber'])
        print(type(request.POST['phonenumber']))
        phonenumber=(request.POST['phonenumber'])
        print(type(phonenumber))
        print("user")
        try:
            #clients=Client.objects.filter(phonenumber=phonenumber)
            client=Client.objects.get(phonenumber=phonenumber)
        except Exception as e:
            client=None
            #messages.error(request,"User Not found")


        if client!=None:
            return redirect('getchecked', pk=client.clientnumber)

        else:
            messages.error(request,"User Not found")
            return render(request,'historyform.html',{'form':form})
    
    form=SearchUserForm()
    return render(request,'historyform.html',{'form':form})

@login_required(login_url='/ar/login/')
def get_checked(request,pk):
    clients=Client.objects.filter(clientnumber=pk)
    client=Client.objects.get(clientnumber=pk)
    context={'clients':clients,'client':client}
    return render(request,'history.html',context)





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


            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Blood parasites Report-{client.clientname}.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 
            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                alignment=2,
         

            )
            # Create a custom ParagraphStyle
            custom_style2 = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
    
                alignment=1,


            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=16,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

            # Define a style for center-aligned paragraph
           # Define a style for center-aligned paragraph
            head_style = ParagraphStyle(
                name='head_style',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=20,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )  
           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))


            Blood_ParasiteTable=[
                [Paragraph('Test', custom_style2), Paragraph('Result', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('التَيْلَريَّات THELERIA')), custom_style2),Paragraph(THELERIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' البابسيات BABESIA')), custom_style2),Paragraph(BABESIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape('  داءُ الإيرليخِيَّات  ANAPLASMA')), custom_style2),Paragraph(ANAPLASMA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape('  الطلائعيات الطفيلية   TRYPANOSOMA')), custom_style2),Paragraph(TRYPANOSOMA, custom_style2)],

                ]  




            # Define table style
            # Set custom column widths
            column_widths = [2 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            Blood_ParasiteTable = Table(Blood_ParasiteTable,colWidths=column_widths)
            Blood_ParasiteTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 16),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Bottom padding for all cells
                    ])
            Blood_ParasiteTable.setStyle(Blood_ParasiteTable_style)
            # Set the row heights


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
            spacer = Spacer(10, 10)
            
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image



            # Set the logo's position to the left side of the page

            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)     

            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            

            story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
            story.append(spacer)
            arabic_text_display=reshaper.reshape('  بيانات العميل ')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            story.append(spacer)

            arabic_text_display=reshaper.reshape(f"الآسم:{client.clientname}")
            arabic_text_display1 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"رقم العميل:{client.clientnumber}")
            arabic_text_display2 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"نوع الحيوات :{client.animaltype}")
            arabic_text_display3 = get_display(arabic_text_display)

        
       
            arabic_text_display4 = get_display(reshaper.reshape(f' نوع العينه: BloodParasite'))
            now=datetime.datetime.now()
            arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))
            analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
            field=str('BloodParasaite')
            print(field)
            price = getattr(analysis_prices, field)

            arabic_text_display6 = get_display(reshaper.reshape(f' السعر: {price} ريال'))
            arabic_text_display7 = get_display(reshaper.reshape(f' عمر الحيوان: {client.age} سنه'))


            arabic_text_display8 = get_display(reshaper.reshape(f' ملحوظه: {client.notes}'))

            # Create a table with three rows and two cells
            info_table_data = [
                [Paragraph(arabic_text_display2, custom_style), Paragraph(arabic_text_display1, custom_style)],
                [Paragraph(arabic_text_display3, custom_style), Paragraph(arabic_text_display4, custom_style)],
                [Paragraph(arabic_text_display6, custom_style), Paragraph(arabic_text_display5, custom_style)],
                [Paragraph(arabic_text_display7, custom_style), Paragraph(arabic_text_display8, custom_style)]

            ]
            info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
            info_table_data_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding for all cells
                    ])
            info_table_data.setStyle(info_table_data_style)
            # Set the row heights

            # Add the table to the story
            story.append(info_table_data)
            # Add the table to the story
            story.append(spacer)  
            story.append(spacer)   

            story.append(spacer) 
            story.append(Paragraph(get_display(reshaper.reshape('Blood Parasites امراض الدم')),head_style))
            story.append(spacer)
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer) 
            story.append(Blood_ParasiteTable) 
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer)             


            line_table_data = [['']]  # Empty cell content
            line_table_style = TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
            ])
            line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
            line_table.setStyle(line_table_style)  # Apply the table style
            story.append(line_table)
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer) 
            logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
            # Create an Image object with the logo image
            # Set the logo's position to the left side of the page
            
            story.append(spacer)  

            logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
            # Add the logo image to the story before the table
            story.append(logo_image)  




            arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            story.append(Paragraph('0503721656 / 0537308922',center_style))
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
            """
            Create Table here
            """

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Intestinal parasites Report-{client.clientname}.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 
            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                alignment=2,
         

            )
            # Create a custom ParagraphStyle
            custom_style2 = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
    
                alignment=1,


            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=16,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

            # Define a style for center-aligned paragraph
           # Define a style for center-aligned paragraph
            head_style = ParagraphStyle(
                name='head_style',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=20,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )  
           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))


            IntestinalparasitesTable=[
                [Paragraph('Test', custom_style2), Paragraph('Result', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الأكريات COCCIDIA')), custom_style2),Paragraph(COCCIDIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' الدِّيدانُ المَمْسودَة NEMATODE')), custom_style2),Paragraph(NEMATODE, custom_style2)],
                [Paragraph(get_display(reshaper.reshape('  الديدان الشريطية  CESTODE')), custom_style2),Paragraph(CESTODE, custom_style2)],
      
                ]  




            # Define table style
            # Set custom column widths
            column_widths = [2 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            IntestinalparasitesTable = Table(IntestinalparasitesTable,colWidths=column_widths)
            IntestinalparasitesTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 16),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Bottom padding for all cells
                    ])
            IntestinalparasitesTable.setStyle(IntestinalparasitesTable_style)
            # Set the row heights


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
            spacer = Spacer(10, 10)
            
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image



            # Set the logo's position to the left side of the page

            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)     

            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            

            story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
            story.append(spacer)
            arabic_text_display=reshaper.reshape('  بيانات العميل ')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            story.append(spacer)

            arabic_text_display=reshaper.reshape(f"الآسم:{client.clientname}")
            arabic_text_display1 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"رقم العميل:{client.clientnumber}")
            arabic_text_display2 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"نوع الحيوات :{client.animaltype}")
            arabic_text_display3 = get_display(arabic_text_display)


            
            arabic_text_display4 = get_display(reshaper.reshape(f' نوع العينه: Intestinalparasites'))
            now=datetime.datetime.now()
            arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))
            analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
            field=str('Intestinalparasites')
            price = getattr(analysis_prices, field)

            arabic_text_display6 = get_display(reshaper.reshape(f' السعر: {price} ريال'))
            arabic_text_display7 = get_display(reshaper.reshape(f' عمر الحيوان: {client.age} سنه'))


            arabic_text_display8 = get_display(reshaper.reshape(f' ملحوظه: {client.notes}'))

            # Create a table with three rows and two cells
            info_table_data = [
                [Paragraph(arabic_text_display2, custom_style), Paragraph(arabic_text_display1, custom_style)],
                [Paragraph(arabic_text_display3, custom_style), Paragraph(arabic_text_display4, custom_style)],
                [Paragraph(arabic_text_display6, custom_style), Paragraph(arabic_text_display5, custom_style)],
                [Paragraph(arabic_text_display7, custom_style), Paragraph(arabic_text_display8, custom_style)]

            ]
            info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
            info_table_data_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding for all cells
                    ])
            info_table_data.setStyle(info_table_data_style)
            # Set the row heights

            # Add the table to the story
            story.append(info_table_data)
            # Add the table to the story
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer) 
            story.append(Paragraph(get_display(reshaper.reshape('Intestinal Parasites امراض الدم')),head_style))
            story.append(spacer)
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer) 
            story.append(IntestinalparasitesTable) 
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer)             


            line_table_data = [['']]  # Empty cell content
            line_table_style = TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
            ])
            line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
            line_table.setStyle(line_table_style)  # Apply the table style
            story.append(line_table)
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer) 
            logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
            # Create an Image object with the logo image
            # Set the logo's position to the left side of the page
            
            story.append(spacer)  

            logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
            # Add the logo image to the story before the table
            story.append(logo_image)  




            arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            story.append(Paragraph('0503721656 / 0537308922',center_style))
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
            BAS=request.POST['BAS']
            
            """
            Create Table here
            """
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Hametology Report-{client.clientname}.pdf"'
            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 
            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                alignment=2,
         

            )
            # Create a custom ParagraphStyle
            custom_style2 = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
    
                alignment=1,


            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=16,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

            # Define a style for center-aligned paragraph
           # Define a style for center-aligned paragraph
            head_style = ParagraphStyle(
                name='head_style',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=20,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )  
           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))





            HaematologyTable=[
                [Paragraph('Test', custom_style2), Paragraph('Result', custom_style2),Paragraph('Normal', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('المناعه  	WBC')), custom_style2),Paragraph(WBC, custom_style2),Paragraph('8-16', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا اللمفاوية            	Lymph')), custom_style2),Paragraph(LYMPH, custom_style2),Paragraph('13 – 45', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('خلايا وحيدات النواة  		Mono')), custom_style2),Paragraph(MONO, custom_style2),Paragraph('2.0 – 8.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا المتعادلة	Neut')), custom_style2),Paragraph(NEUT, custom_style2),Paragraph('30 – 70', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا الحمضية    	Eosin')), custom_style2),Paragraph(EOSIN, custom_style2),Paragraph('0.0 – 6.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا القاعدية    	Bas')), custom_style2),Paragraph(BAS, custom_style2),Paragraph('0.0 – 1.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('كريات الدم الحمراء   	RBC')), custom_style2),Paragraph(RBC, custom_style2),Paragraph('7 – 11', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('هيمو جلوين  	Hgb')), custom_style2),Paragraph(HGB, custom_style2),Paragraph('11 – 16', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('حجم الدم  	Hct')), custom_style2),Paragraph(HCT, custom_style2),Paragraph('25 – 33', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('معدل حجم كريات الدم  	Mcv ')), custom_style2),Paragraph(MCV, custom_style2),Paragraph('26 – 35', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('هيمو جلوبين الكرية الوسط  	Mch')), custom_style2),Paragraph(MCH, custom_style2),Paragraph('12 – 17', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('متوسط تركيز هيمو جلوبين  Mchc')), custom_style2),Paragraph(MCHC, custom_style2),Paragraph('40 – 50', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الصفائح الدموية  	PLT')), custom_style2),Paragraph(PLT, custom_style2),Paragraph('150 - 500', custom_style2)],

      
                ]

            # Define table style
            # Set custom column widths
            column_widths = [2 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            HaematologyTable = Table(HaematologyTable,colWidths=column_widths)
            HaematologyTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 16),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Bottom padding for all cells
                    ])
            HaematologyTable.setStyle(HaematologyTable_style)
            # Set the row heights


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

 


            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 

            # Add a spacer with horizontal space of 50 points
            spacer = Spacer(10, 10)
            
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image



            # Set the logo's position to the left side of the page

            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)     

            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            

            story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
            story.append(spacer)
            arabic_text_display=reshaper.reshape('  بيانات العميل ')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            story.append(spacer)

            arabic_text_display=reshaper.reshape(f"الآسم:{client.clientname}")
            arabic_text_display1 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"رقم العميل:{client.clientnumber}")
            arabic_text_display2 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"نوع الحيوات :{client.animaltype}")
            arabic_text_display3 = get_display(arabic_text_display)

           
            
            arabic_text_display4 = get_display(reshaper.reshape(f' نوع العينه: Haematology '))
            now=datetime.datetime.now()
            arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))
            analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
            field=str('Haematology')
            price = getattr(analysis_prices, field)

            arabic_text_display6 = get_display(reshaper.reshape(f' السعر: {price} ريال'))
            arabic_text_display7 = get_display(reshaper.reshape(f' عمر الحيوان: {client.age} سنه'))


            arabic_text_display8 = get_display(reshaper.reshape(f' ملحوظه: {client.notes}'))

            # Create a table with three rows and two cells
            info_table_data = [
                [Paragraph(arabic_text_display2, custom_style), Paragraph(arabic_text_display1, custom_style)],
                [Paragraph(arabic_text_display3, custom_style), Paragraph(arabic_text_display4, custom_style)],
                [Paragraph(arabic_text_display6, custom_style), Paragraph(arabic_text_display5, custom_style)],
                [Paragraph(arabic_text_display7, custom_style), Paragraph(arabic_text_display8, custom_style)]

            ]
            info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
            info_table_data_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding for all cells
                    ])
            info_table_data.setStyle(info_table_data_style)
            # Set the row heights

            # Add the table to the story
            story.append(info_table_data)
            # Add the table to the story
            story.append(Paragraph('Hametology',head_style))
            story.append(spacer)

            story.append(HaematologyTable)            

            line_table_data = [['']]  # Empty cell content
            line_table_style = TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
            ])
            line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
            line_table.setStyle(line_table_style)  # Apply the table style
            story.append(line_table)

            logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
            # Create an Image object with the logo image
            # Set the logo's position to the left side of the page
            
            story.append(spacer)  

            logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
            # Add the logo image to the story before the table
            story.append(logo_image)  




            arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            story.append(Paragraph('0503721656 / 0537308922',center_style))
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
            GGT=request.POST['GGT']
            ALP=request.POST['APL']
            Copper=request.POST['Copper']
            Phosphorous=request.POST['Phosphorous']
            Creatinine=request.POST['Creatinine']
            IRON=request.POST['IRON']

          
            """
            Create Table here
            """

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="BloodChemistry-{client.clientname}.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 
            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                alignment=2,
         

            )
            # Create a custom ParagraphStyle
            custom_style2 = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
    
                alignment=1,


            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=16,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

            # Define a style for center-aligned paragraph
           # Define a style for center-aligned paragraph
            head_style = ParagraphStyle(
                name='head_style',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=20,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )  
           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))


            BloodChemistryTable=[
                [Paragraph('Test', custom_style2), Paragraph('Result', custom_style2),Paragraph('Normal', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('يوريا UREA')), custom_style2),Paragraph(Urea, custom_style2),Paragraph('28 - 8', custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' الكلى Creatinine')), custom_style2),Paragraph(Creatinine, custom_style2),Paragraph('2.4 – 0.5', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الكبد1 Ast')), custom_style2),Paragraph(AST_GOT, custom_style2),Paragraph('135 – 31', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الكبد2 ALT')), custom_style2),Paragraph(ALT_GPT, custom_style2),Paragraph('25 – 3', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الكبد3 GGT ')), custom_style2),Paragraph(GGT, custom_style2),Paragraph('55 – 4.5', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('بروتين Protein')), custom_style2),Paragraph(TotalProtien, custom_style2),Paragraph('7.5 – 5.2', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الفوسفاتاز ALP')), custom_style2),Paragraph(ALP, custom_style2),Paragraph('98-279', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('قلب CK')), custom_style2),Paragraph(Ck, custom_style2),Paragraph('16 – 206', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('العضلات LDH')), custom_style2),Paragraph(LDH, custom_style2),Paragraph('185 - 550', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('كالسيوم CA')), custom_style2),Paragraph(Calcium, custom_style2),Paragraph('8.0 – 13.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('فسفور Phos')), custom_style2),Paragraph(Phosphorous, custom_style2),Paragraph(' 3.0 - 8.5', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('النحاس Copper')), custom_style2),Paragraph(Copper, custom_style2),Paragraph('40 – 50', custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' حديد  	IRON')), custom_style2),Paragraph(IRON, custom_style2),Paragraph('150 - 500', custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' جلوكوز  	Glucose')), custom_style2),Paragraph(Gluco, custom_style2),Paragraph('150 - 500', custom_style2)],

      
                ]  




            # Define table style
            # Set custom column widths
            column_widths = [2 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            BloodChemistryTable = Table(BloodChemistryTable,colWidths=column_widths)
            BloodChemistryTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 16),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 4),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Bottom padding for all cells
                    ])
            BloodChemistryTable.setStyle(BloodChemistryTable_style)
            # Set the row heights


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
            spacer = Spacer(10, 10)
            
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image



            # Set the logo's position to the left side of the page

            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)     

            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            

            story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
            story.append(spacer)
            arabic_text_display=reshaper.reshape('  بيانات العميل ')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            story.append(spacer)

            arabic_text_display=reshaper.reshape(f"الآسم:{client.clientname}")
            arabic_text_display1 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"رقم العميل:{client.clientnumber}")
            arabic_text_display2 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"نوع الحيوات :{client.animaltype}")
            arabic_text_display3 = get_display(arabic_text_display)

            
            arabic_text_display4 = get_display(reshaper.reshape(f' نوع العينه: BIOChemistry'))
            now=datetime.datetime.now()
            arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))
            analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
            field=str('BIOChemistry')
            price = getattr(analysis_prices, field)

            arabic_text_display6 = get_display(reshaper.reshape(f' السعر: {price} ريال'))
            arabic_text_display7 = get_display(reshaper.reshape(f' عمر الحيوان: {client.age} سنه'))


            arabic_text_display8 = get_display(reshaper.reshape(f' ملحوظه: {client.notes}'))

            # Create a table with three rows and two cells
            info_table_data = [
                [Paragraph(arabic_text_display2, custom_style), Paragraph(arabic_text_display1, custom_style)],
                [Paragraph(arabic_text_display3, custom_style), Paragraph(arabic_text_display4, custom_style)],
                [Paragraph(arabic_text_display6, custom_style), Paragraph(arabic_text_display5, custom_style)],
                [Paragraph(arabic_text_display7, custom_style), Paragraph(arabic_text_display8, custom_style)]

            ]
            info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
            info_table_data_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding for all cells
                    ])
            info_table_data.setStyle(info_table_data_style)
            # Set the row heights

            # Add the table to the story
            story.append(info_table_data)
            # Add the table to the story
            story.append(Paragraph('Blood Chemistry',head_style))
            story.append(spacer)

            story.append(BloodChemistryTable)            

            line_table_data = [['']]  # Empty cell content
            line_table_style = TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
            ])
            line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
            line_table.setStyle(line_table_style)  # Apply the table style
            story.append(line_table)

            logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
            # Create an Image object with the logo image
            # Set the logo's position to the left side of the page
            
            story.append(spacer)  

            logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
            # Add the logo image to the story before the table
            story.append(logo_image)  




            arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            story.append(Paragraph('0503721656 / 0537308922',center_style))
            # Build the PDF document
            doc.build(story)



            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response
     


            # Get the current instance object to display in the template
            img_obj = form.instance
            #return render(request, 'add_user.html', {'form': form,'img_obj': img_obj})
       
        print(form.errors.as_data())
        return render(request,template_name , {'form': form})
    return render(request,template_name , {'form': form})    
  

@login_required(login_url='/ar/login/')
def create_report(request,pk):
    # Create the HttpResponse object with the appropriate PDF headers.
            """
            Create Table here
            """

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 
            # Create the HttpResponse object with the appropriate PDF headers.
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Clinet Info Report-{client.clientname}.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 
            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                alignment=2,
         

            )
            # Create a custom ParagraphStyle
            custom_style2 = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=14,  # Specify the font size
                textColor=colors.black,  # Specify the font color
    
                alignment=1,


            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=16,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

            # Define a style for center-aligned paragraph
           # Define a style for center-aligned paragraph
            head_style = ParagraphStyle(
                name='head_style',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=20,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )  
           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))










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
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image



            # Set the logo's position to the left side of the page

            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)     

            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            

            story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
            story.append(spacer)
            arabic_text_display=reshaper.reshape('  بيانات العميل ')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            story.append(spacer)

            arabic_text_display=reshaper.reshape(f"الآسم:{client.clientname}")
            arabic_text_display1 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"رقم العميل:{client.clientnumber}")
            arabic_text_display2 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"نوع الحيوات :{client.animaltype}")
            arabic_text_display3 = get_display(arabic_text_display)

            clientrow = Client.objects.get(pk=1)
            field_label = clientrow.get_field_label(client.sampletype)
            
            arabic_text_display4 = get_display(reshaper.reshape(f' نوع العينه: {field_label}'))
            now=datetime.datetime.now()
            arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))
            analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
            field=str(field_label)
            price = getattr(analysis_prices, field)

            arabic_text_display6 = get_display(reshaper.reshape(f' السعر: {price} ريال'))
            arabic_text_display7 = get_display(reshaper.reshape(f' عمر الحيوان: {client.age} سنه'))


            arabic_text_display8 = get_display(reshaper.reshape(f' ملحوظه: {client.notes}'))

            # Create a table with three rows and two cells
            info_table_data = [
                [Paragraph(arabic_text_display2, custom_style), Paragraph(arabic_text_display1, custom_style)],
                [Paragraph(arabic_text_display3, custom_style), Paragraph(arabic_text_display4, custom_style)],
                [Paragraph(arabic_text_display6, custom_style), Paragraph(arabic_text_display5, custom_style)],
                [Paragraph(arabic_text_display7, custom_style), Paragraph(arabic_text_display8, custom_style)]

            ]
            info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
            info_table_data_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), 6),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),  # Bottom padding for all cells
                    ])
            info_table_data.setStyle(info_table_data_style)
            # Set the row heights

            # Add the table to the story
            story.append(info_table_data)
            # Add the table to the story
  
            story.append(spacer)
            story.append(spacer)  
            story.append(spacer)  
            story.append(spacer)  
             


            line_table_data = [['']]  # Empty cell content
            line_table_style = TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
            ])
            line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
            line_table.setStyle(line_table_style)  # Apply the table style
            story.append(line_table)
      
            logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
            # Create an Image object with the logo image
            # Set the logo's position to the left side of the page
            
            story.append(spacer)  

            logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
            # Add the logo image to the story before the table
            story.append(logo_image)  




            arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            story.append(Paragraph('0503721656 / 0537308922',center_style))
            # Build the PDF document
            doc.build(story)



            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response





    
@login_required(login_url='/ar/login/')
def check_all(request,pk):
    language_code = request.path.split('/')[1]  # Extract the first part of the path
    template_name='check_all.html' if language_code=='en' else 'check_all.html'
    """Process images uploaded by users"""
    form1 = HaematologyForm(request.POST)
    form2 = BloodChemistryForm(request.POST)
    form3 = BloodParasaiteForm(request.POST)
    form4 = IntestinalparasitesForm(request.POST)

    if request.method == 'POST':
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid():
            Haematology=form1.save(commit=False)  
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
            BAS=request.POST['BAS']
            



            BloodChemistry=form2.save(commit=False)   
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
            GGT=request.POST['GGT']
            ALP=request.POST['APL']
            Copper=request.POST['Copper']
            Phosphorous=request.POST['Phosphorous']
            Creatinine=request.POST['Creatinine']
            IRON=request.POST['IRON']


            Intestinalparasites=form4.save(commit=False)  
            client=Client.objects.get(clientnumber=pk) 
            Intestinalparasites.admin=request.user
            Intestinalparasites.client=client
            Intestinalparasites.save()
            
            COCCIDIA=request.POST['COCCIDIA']
            NEMATODE=request.POST['NEMATODE']
            CESTODE=request.POST['CESTODE']
        

            BloodParasaite=form3.save(commit=False)  
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
            response['Content-Disposition'] = f'attachment; filename="All Checkup Report-{client.clientname}.pdf"'

            # Create a PDF document object
         
            buffer = BytesIO()
            # Set the desired margin size (in this example, 1 inch)
            margin_size = 0.5 * inch
            # Create the PDF object
            doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=margin_size, rightMargin=margin_size,
                        topMargin=margin_size, bottomMargin=margin_size,showBoundary=True)
            
 
            # Create a custom ParagraphStyle
            custom_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=12,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                alignment=2,
         

            )
            # Create a custom ParagraphStyle
            custom_style2 = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=12,  # Specify the font size
                textColor=colors.black,  # Specify the font color
    
                alignment=1,


            )
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=10,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                #spaceBefore=12,  # Specify the space before the paragraph
                #spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

            # Define a style for center-aligned paragraph
           # Define a style for center-aligned paragraph
            head_style = ParagraphStyle(
                name='head_style',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=16,  # Specify the font size
                textColor=colors.black,  # Specify the font color
                #spaceBefore=12,  # Specify the space before the paragraph
                #spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )  
           

            # Load custom font file for Arabic text
            font_path = settings.STATIC_ROOT + '/webfonts/22016-adobearabic.ttf'  # Replace with the path to your font file
            print(font_path)
            pdfmetrics.registerFont(TTFont('22016-adobearabic', font_path))





            HaematologyTable=[
                [Paragraph('Haematology', custom_style2), Paragraph('Result', custom_style2),Paragraph('Normal', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('المناعه  	WBC')), custom_style2),Paragraph(WBC, custom_style2),Paragraph('8-16', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا اللمفاوية            	Lymph')), custom_style2),Paragraph(LYMPH, custom_style2),Paragraph('13 – 45', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('خلايا وحيدات النواة  		Mono')), custom_style2),Paragraph(MONO, custom_style2),Paragraph('2.0 – 8.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا المتعادلة	Neut')), custom_style2),Paragraph(NEUT, custom_style2),Paragraph('30 – 70', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا الحمضية    	Eosin')), custom_style2),Paragraph(EOSIN, custom_style2),Paragraph('0.0 – 6.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الخلايا القاعدية    	Bas')), custom_style2),Paragraph(BAS, custom_style2),Paragraph('0.0 – 1.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('كريات الدم الحمراء   	RBC')), custom_style2),Paragraph(RBC, custom_style2),Paragraph('7 – 11', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('هيمو جلوين  	Hgb')), custom_style2),Paragraph(HGB, custom_style2),Paragraph('11 – 16', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('حجم الدم  	Hct')), custom_style2),Paragraph(HCT, custom_style2),Paragraph('25 – 33', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('معدل حجم كريات الدم  	Mcv ')), custom_style2),Paragraph(MCV, custom_style2),Paragraph('26 – 35', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('هيمو جلوبين الكرية الوسط  	Mch')), custom_style2),Paragraph(MCH, custom_style2),Paragraph('12 – 17', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('متوسط تركيز هيمو جلوبين  Mchc')), custom_style2),Paragraph(MCHC, custom_style2),Paragraph('40 – 50', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الصفائح الدموية  	PLT')), custom_style2),Paragraph(PLT, custom_style2),Paragraph('150 - 500', custom_style2)],

      
                ]

            # Define table style
            # Set custom column widths
            column_widths = [3.5 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            HaematologyTable = Table(HaematologyTable,colWidths=column_widths)
            HaematologyTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), -2),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Bottom padding for all cells
                    ])
            HaematologyTable.setStyle(HaematologyTable_style)
            # Set the row heights

            BloodChemistryTable=[
                [Paragraph('Blood Chemistry', custom_style2), Paragraph('Result', custom_style2),Paragraph('Normal', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('يوريا UREA')), custom_style2),Paragraph(Urea, custom_style2),Paragraph('28 - 8', custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' الكلى Creatinine')), custom_style2),Paragraph(Creatinine, custom_style2),Paragraph('2.4 – 0.5', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الكبد1 Ast')), custom_style2),Paragraph(AST_GOT, custom_style2),Paragraph('135 – 31', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الكبد2 ALT')), custom_style2),Paragraph(ALT_GPT, custom_style2),Paragraph('25 – 3', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الكبد3 GGT ')), custom_style2),Paragraph(GGT, custom_style2),Paragraph('55 – 4.5', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('بروتين Protein')), custom_style2),Paragraph(TotalProtien, custom_style2),Paragraph('7.5 – 5.2', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الفوسفاتاز ALP')), custom_style2),Paragraph(ALP, custom_style2),Paragraph('98-279', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('قلب CK')), custom_style2),Paragraph(Ck, custom_style2),Paragraph('16 – 206', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('العضلات LDH')), custom_style2),Paragraph(LDH, custom_style2),Paragraph('185 - 550', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('كالسيوم CA')), custom_style2),Paragraph(Calcium, custom_style2),Paragraph('8.0 – 13.0', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('فسفور Phos')), custom_style2),Paragraph(Phosphorous, custom_style2),Paragraph(' 3.0 - 8.5', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('النحاس Copper')), custom_style2),Paragraph(Copper, custom_style2),Paragraph('55 – 110', custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' حديد  	IRON')), custom_style2),Paragraph(IRON, custom_style2),Paragraph('70 - 160', custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' جلوكوز  	Glucose')), custom_style2),Paragraph(Gluco, custom_style2),Paragraph('70 - 140', custom_style2)],

      
                ]  




            # Define table style
            # Set custom column widths
            column_widths = [3.5 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            BloodChemistryTable = Table(BloodChemistryTable,colWidths=column_widths)
            BloodChemistryTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), -2),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Bottom padding for all cells
                    ])
            BloodChemistryTable.setStyle(BloodChemistryTable_style)

            IntestinalparasitesTable=[
                [Paragraph('Intestinal parasites', custom_style2), Paragraph('Result', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الأكريات COCCIDIA')), custom_style2),Paragraph(COCCIDIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' الدِّيدانُ المَمْسودَة NEMATODE')), custom_style2),Paragraph(NEMATODE, custom_style2)],
                [Paragraph(get_display(reshaper.reshape('  الديدان الشريطية  CESTODE')), custom_style2),Paragraph(CESTODE, custom_style2)],
      
                ]  
            column_widths = [2 * inch, 0.6 * inch,2 * inch, 0.6 * inch]  # Adjust the widths as per your requirement
            TwoTableinone=[
                [Paragraph('Intestinal parasites', custom_style2), Paragraph('Result', custom_style2),Paragraph('Blood Parasite', custom_style2), Paragraph('Result', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('الأكريات COCCIDIA')), custom_style2),Paragraph(COCCIDIA, custom_style2),Paragraph(get_display(reshaper.reshape('التَيْلَريَّات THELERIA')), custom_style2),Paragraph(THELERIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' الدِّيدانُ المَمْسودَة NEMATODE')), custom_style2),Paragraph(NEMATODE, custom_style2),Paragraph(get_display(reshaper.reshape(' البابسيات BABESIA')), custom_style2),Paragraph(BABESIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape('  الديدان الشريطية  CESTODE')), custom_style2),Paragraph(CESTODE, custom_style2),Paragraph(get_display(reshaper.reshape('  داءُ الإيرليخِيَّات  ANAPLASMA')), custom_style2),Paragraph(ANAPLASMA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' ')), custom_style2),Paragraph('', custom_style2),Paragraph(get_display(reshaper.reshape('  الطلائعيات الطفيلية   TRYPANOSOMA')), custom_style2),Paragraph(TRYPANOSOMA, custom_style2)],
                ]  
            TwoTableinone = Table(TwoTableinone,colWidths=column_widths)
            TwoTableinone_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), -2),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Bottom padding for all cells
                    ])
            TwoTableinone.setStyle(TwoTableinone_style)


            # Define table style
            # Set custom column widths
            column_widths = [4 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            IntestinalparasitesTable = Table(IntestinalparasitesTable,colWidths=column_widths)
            IntestinalparasitesTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), -2),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Bottom padding for all cells
                    ])
            IntestinalparasitesTable.setStyle(IntestinalparasitesTable_style)
            # Set the row heights

            Blood_ParasiteTable=[
                [Paragraph('Blood Parasite', custom_style2), Paragraph('Result', custom_style2)],
                [Paragraph(get_display(reshaper.reshape('التَيْلَريَّات THELERIA')), custom_style2),Paragraph(THELERIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape(' البابسيات BABESIA')), custom_style2),Paragraph(BABESIA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape('  داءُ الإيرليخِيَّات  ANAPLASMA')), custom_style2),Paragraph(ANAPLASMA, custom_style2)],
                [Paragraph(get_display(reshaper.reshape('  الطلائعيات الطفيلية   TRYPANOSOMA')), custom_style2),Paragraph(TRYPANOSOMA, custom_style2)],

                ]  




            # Define table style
            # Set custom column widths
            column_widths = [4 * inch, 0.7 * inch, 1 * inch]  # Adjust the widths as per your requirement
            Blood_ParasiteTable = Table(Blood_ParasiteTable,colWidths=column_widths)
            Blood_ParasiteTable_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), -2),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Bottom padding for all cells
                    ])
            Blood_ParasiteTable.setStyle(Blood_ParasiteTable_style)          
           
           
           
            # Define a style for center-aligned paragraph
            center_style = ParagraphStyle(
                name='CustomStyle',
                fontName='22016-adobearabic',  # Specify your custom font name
                fontSize=12,  # Specify the font size
                textColor=colors.blue,  # Specify the font color
                spaceBefore=12,  # Specify the space before the paragraph
                spaceAfter=6,  # Specify the space after the paragraph
                alignment=1
            )

         

            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 

 


            # Add simple strings above the table
            client=Client.objects.get(clientnumber=pk) 

            # Add a spacer with horizontal space of 50 points
            spacer = Spacer(10, 10)
            
            # Build the story containing the table
            story = []    
            # Define the path to your logo image file
            logo_path = settings.STATIC_ROOT + '/img/logo.jpg'
            # Create an Image object with the logo image



            # Set the logo's position to the left side of the page
            
            logo_image = Image(logo_path, width=2 * inch, height=1 * inch)  # Adjust the width and height as per your requirement
            logo_image.hAlign = 'RIGHT'
            # Add the logo image to the story before the table
            story.append(logo_image)     

            arabic_text_display=reshaper.reshape('مختبر صحه الكائنات البيطريه')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            

            story.append(Paragraph("Veterinary animal Health Laboratory",head_style))
            story.append(spacer)
            arabic_text_display=reshaper.reshape('  بيانات العميل ')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,head_style))
            story.append(spacer)

            arabic_text_display=reshaper.reshape(f"الآسم:{client.clientname}")
            arabic_text_display1 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"رقم العميل:{client.clientnumber}")
            arabic_text_display2 = get_display(arabic_text_display)
            arabic_text_display=reshaper.reshape(f"نوع الحيوات :{client.animaltype}")
            arabic_text_display3 = get_display(arabic_text_display)

           
            
            arabic_text_display4 = get_display(reshaper.reshape(f' نوع العينه: Haematology '))
            now=datetime.datetime.now()
            arabic_text_display5 = get_display(reshaper.reshape(f' التاريخ:{now.year}/{now.month}/{now.day}'))
            analysis_prices = AnalysisPrices.objects.get(pk=1)  # Assuming you have only one instance
            field=str('All')
            price = getattr(analysis_prices, field)

            arabic_text_display6 = get_display(reshaper.reshape(f' السعر: {price} ريال'))
            arabic_text_display7 = get_display(reshaper.reshape(f' عمر الحيوان: {client.age} سنه'))


            arabic_text_display8 = get_display(reshaper.reshape(f' ملحوظه: {client.notes}'))

            # Create a table with three rows and two cells
            info_table_data = [
                [Paragraph(arabic_text_display2, custom_style), Paragraph(arabic_text_display1, custom_style)],
                [Paragraph(arabic_text_display3, custom_style), Paragraph(arabic_text_display4, custom_style)],
                [Paragraph(arabic_text_display6, custom_style), Paragraph(arabic_text_display5, custom_style)],
                [Paragraph(arabic_text_display7, custom_style), Paragraph(arabic_text_display8, custom_style)]

            ]
            info_table_data = Table(info_table_data,colWidths=[2 * inch,2 * inch])
            info_table_data_style= TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), '#9DB2BF'),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white) ,
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), '22016-adobearabic'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BACKGROUND', (0, 1), (-1, -1), '#9DB2BF'),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('TOPPADDING', (0, 0), (-1, -1), -2),  # Top padding for all cells
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),  # Bottom padding for all cells
                    ])
            info_table_data.setStyle(info_table_data_style)
            # Set the row heights

            # Add the table to the story
            story.append(info_table_data)
            # Add the table to the story

            story.append(spacer)
    

            story.append(BloodChemistryTable)  
            story.append(HaematologyTable)
        

            #story.append(IntestinalparasitesTable)   

    



            #story.append(Blood_ParasiteTable)              
 

               
            story.append(TwoTableinone)



   
            line_table_data = [['']]  # Empty cell content
            line_table_style = TableStyle([
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2, colors.black),  # Bottom padding of 2 points
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.black)  # Bottom border line with 0.5-point width
            ])
            line_table = Table(line_table_data, colWidths=[doc.width])  # Table with a single column spanning the width of the document
            line_table.setStyle(line_table_style)  # Apply the table style
            story.append(line_table)

            logo_path = settings.STATIC_ROOT + '/img/qrlogo.png'
            # Create an Image object with the logo image
            # Set the logo's position to the left side of the page
            
            #story.append(spacer)  

            logo_image = Image(logo_path, width=0.7 * inch, height=0.7 * inch)  # Adjust the width and height as per your requirement
            # Add the logo image to the story before the table
            
            story.append(spacer)
            story.append(logo_image)  




            arabic_text_display=reshaper.reshape('المملكه العربية/ الرياض/طريق الجنادرية')
            arabic_text_display = get_display(arabic_text_display)
            story.append(Paragraph(arabic_text_display,center_style))
            story.append(Paragraph('0503721656 / 0537308922',center_style))
            # Build the PDF document
            doc.build(story)



            # Get the value of the BytesIO buffer and write it to the response
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            
            return response
     

        return render(request,template_name , {'form1': form1,'form2': form2,'form3': form3,'form4': form4})
    return render(request,template_name , {'form1': form1,'form2': form2,'form3': form3,'form4': form4})
    
