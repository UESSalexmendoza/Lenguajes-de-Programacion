from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Incidente, HistorialEstadoIncidente

@receiver(post_save, sender=Incidente)
def crear_historial_inicial(sender, instance, created, **kwargs):
    if created:
        HistorialEstadoIncidente.objects.create(
            incidente=instance,
            estado=instance.estado,
            usuario=instance.usuario,
            comentario='Creación inicial del incidente.'
        )

@receiver(post_save, sender=HistorialEstadoIncidente)
def actualizar_estado_incidente(sender, instance, created, **kwargs):
    if created:
        incidente = instance.incidente
        incidente.estado = instance.estado
        incidente.save()
        
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from django.utils.timezone import now

from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now

def completar_usuario(user):
    """Completa campos si están vacíos (útil si ya inició sesión antes)."""
    updated = False
    if not user.name:
        user.name = user.get_full_name() or user.username
        updated = True
    if user.fecha_aceptacion is None:
        user.fecha_aceptacion = now()
        updated = True
    if not user.acepta_politicas:
        user.acepta_politicas = True
        updated = True
    if not user.estado:
        user.estado = True
        updated = True
    if updated:
        user.save()

@receiver(user_signed_up)
def on_google_signup(request, user, **kwargs):
    completar_usuario(user)

@receiver(user_logged_in)
def on_google_login(request, user, **kwargs):
    completar_usuario(user)

