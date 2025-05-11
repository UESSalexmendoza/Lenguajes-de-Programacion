
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from ckeditor.fields import RichTextField

# Catálogo de Países
class Pais(models.Model):
    nombre = models.CharField("País", max_length=100)
    codigo_iso = models.CharField("Código ISO", max_length=3, unique=True)
    estado = models.BooleanField("Estado", default=True)
    def __str__(self):
        return self.nombre

# Catálogo de Ciudades
class Ciudad(models.Model):
    nombre = models.CharField("Ciudad", max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, verbose_name="País" )
    codigo_iso = models.CharField("Código ISO",max_length=5, blank=True, null=True)
    latitud = models.FloatField("Longitud",default=0.0)
    longitud = models.FloatField("Latitud",default=0.0)
    estado = models.BooleanField("Estado", default=True)

    def __str__(self):
        return f"{self.nombre}"

#Usuarios
class Usuario(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField("Nombre completo", max_length=200)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)
    es_admin = models.BooleanField(default=False)
    acepta_politicas = models.BooleanField(default=False)
    fecha_aceptacion = models.DateTimeField(null=True, blank=True)
    estado = models.BooleanField(default=False)  
    numero_intentos = models.PositiveIntegerField(default=0)
    fecha_ultimo_intento = models.DateTimeField(null=True, blank=True)
    es_autoridad = models.BooleanField(default=False)
    def __str__(self):
        return self.name or self.username

class EstadoCaso(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    icono = models.CharField(
        max_length=100,
        help_text="Clase CSS del ícono Bootstrap (ej: 'bi-check-circle')",
        blank=True,
        null=True
    )
    def __str__(self):
        return self.nombre
    
class EntidadResponsable(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=250)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    usuarios = models.ManyToManyField(Usuario, related_name='entidades', blank=True)

    def __str__(self):
        return self.nombre

class Incidente(models.Model):
    numero_caso = models.AutoField(primary_key=True)
    detalle = RichTextField() 
    estado = models.ForeignKey(EstadoCaso, on_delete=models.PROTECT, default=1)  # Estado actual
    fecha_registro = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reportes_creados')
    entidad_responsable = models.ForeignKey(EntidadResponsable, on_delete=models.SET_NULL, null=True, blank=True)
    pais = models.ForeignKey(Pais, on_delete=models.SET_NULL, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    direccion = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Incidente #{self.numero_caso} - {self.estado.nombre}"

class HistorialEstadoIncidente(models.Model):
    incidente = models.ForeignKey(Incidente, on_delete=models.CASCADE, related_name='historial_estados')
    estado = models.ForeignKey(EstadoCaso, on_delete=models.PROTECT)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)
    comentario = models.TextField(blank=True, null=True)
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.incidente} - {self.estado.nombre} por {self.usuario}"


class Contacto(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField()
    comentario = models.TextField(max_length=1000)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_envio = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.correo}"
