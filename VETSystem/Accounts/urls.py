from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

# app_name="accounts"



urlpatterns=[
    path('register/',views.register_request,name='register'),
    path('login/',views.login_request,name='login'),
    path('logout/',views.logout_request,name='logout'),
    path('',views.home_page,name='homepage'),
    path('add_user/',views.add_client,name='adduser'),

    path('haema_tology/<int:pk>',views.Haematology,name='haematology'),
    path('blood_chemistry/<int:pk>',views.BloodChemistry,name='bloodchemistry'),

    path('search_user/',views.search_user,name='searchuser'),
    path('form_created/',views.form_created,name='formcreated'),
    path('create_report/<int:pk>',views.create_report,name='createreport'),
    #path('change-language/<str:language_code>/',views.change_language,name='changelanguage'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]




if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
        

