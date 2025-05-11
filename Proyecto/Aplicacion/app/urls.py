from django.urls import path
from .views import index, about, CustomLoginView, CustomPasswordResetView, UsuarioCreateView

from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView
from django.contrib.auth.views import LogoutView

from .views import CustomPasswordResetConfirmView
from .views import activar_cuenta
from .views import mapa_incidentes
from .views import incidentes_json
from .views import crear_incidente
from .views import politica_privacidad
from .views import terminos_condiciones
from .views import contacto
from .views import contacto_exito
from .views import mis_incidentes

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('login/', CustomLoginView.as_view(), name='login'),path('recuperar-clave/', CustomPasswordResetView.as_view(), name='password_reset'),
    path( 'recuperar-clave/enviado/', PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),   
    path( 'recuperar-clave/confirmar/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm' ),
    path( 'recuperar-clave/completado/', PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete' ), 
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registro/', UsuarioCreateView.as_view(), name='registro'),
    path('activar/<uidb64>/<token>/', activar_cuenta, name='activar_cuenta'),    
    path('mapa/', mapa_incidentes, name='mapa_incidentes'),
    path('incidentes-json/', incidentes_json, name='incidentes_json'), 
    path('incidente/crear/', crear_incidente, name='crear_incidente'),    
    path('politica-privacidad/', politica_privacidad, name='politica_privacidad'),    
    path('terminos-condiciones/', terminos_condiciones, name='terminos_condiciones'),    
    path('contacto/', contacto, name='contacto'),
    path('contacto/exito/', contacto_exito, name='contacto_exito'),    
    path('mis-incidentes/', mis_incidentes, name='mis_incidentes'),    
]
