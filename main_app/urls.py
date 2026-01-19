# main_app/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from main_app.views import (
    CustomLoginView, logout_view, dashboard,
    AbiturientListView, AbiturientDetailView, AbiturientCreateView, AbiturientUpdateView, AbiturientDeleteView,
    DogovorListView, DogovorCreateView, DogovorDetailView, DogovorUpdateView, DogovorDeleteView,
    DocumentCreateView,
    get_parents_by_abiturient_ajax, get_news, save_news,
    search_students,
    search_students_legacy,
    AbiturientAutocomplete,
    RoditelAutocomplete, 
    SpecialnostAutocomplete,
    get_abit_info_ajax 
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Аутентификация
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    
    # СБРОС ПАРОЛЯ
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
         name='password_reset_complete'),

    # Главная панель
    path('dashboard/', dashboard, name='dashboard'),
    path('', dashboard, name='home'), 

     # Autocomplete-light
    path('abiturient-autocomplete/', AbiturientAutocomplete.as_view(), name='abiturient-autocomplete'),
    path('roditel-autocomplete/', RoditelAutocomplete.as_view(), name='roditel-autocomplete'),
    path('specialnost-autocomplete/', SpecialnostAutocomplete.as_view(), name='specialnost-autocomplete'),

    # Абитуриенты
    path('abiturients/', AbiturientListView.as_view(), name='abiturient_list'),
    path('abiturients/new/', AbiturientCreateView.as_view(), name='abiturient_create'),
    path('abiturients/<int:pk>/', AbiturientDetailView.as_view(), name='abiturient_detail'),
    path('abiturients/<int:pk>/edit/', AbiturientUpdateView.as_view(), name='abiturient_update'),
    path('abiturients/<int:pk>/delete/', AbiturientDeleteView.as_view(), name='abiturient_delete'),

    # Договоры
    path('dogovors/', DogovorListView.as_view(), name='dogovor_list'),
    path('dogovors/new/', DogovorCreateView.as_view(), name='dogovor_create'),
    path('dogovors/new/<int:abiturient_id>/', DogovorCreateView.as_view(), name='dogovor_create_for_abiturient'),
    path('dogovors/<int:pk>/', DogovorDetailView.as_view(), name='dogovor_detail'),
    path('dogovors/<int:pk>/edit/', DogovorUpdateView.as_view(), name='dogovor_update'),
    path('dogovors/<int:pk>/delete/', DogovorDeleteView.as_view(), name='dogovor_delete'),

    # Документы
    path('documents/new/', DocumentCreateView.as_view(), name='document_create'),

    # AJAX / API
    path('api/parents_by_abiturient/<int:abiturient_id>/', get_parents_by_abiturient_ajax, name='parents_by_abiturient_ajax'),
    path('api/abit_info/<int:abit_id>/', get_abit_info_ajax, name='abit_info_ajax'), # Теперь это заработает
    path('api/get_news/', get_news, name='get_news'),
    path('api/save_news/', save_news, name='save_news'),
    path('api/search_students_legacy/', search_students_legacy, name='search_students_legacy'),
    path('api/search_students/', search_students, name='search_students'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)