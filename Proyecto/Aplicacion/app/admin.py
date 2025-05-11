from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Pais, Ciudad, Usuario, EstadoCaso, EntidadResponsable, Incidente, HistorialEstadoIncidente, Contacto

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codigo_iso', 'estado')
    list_filter = ('estado',)
    search_fields = ('nombre', 'codigo_iso')
    fieldsets = (
        ('Información general del país', {
            'fields': ('nombre', 'codigo_iso')
        }),
        ('Estado del registro', {
            'fields': ('estado',)
        }),
    )    
    
    
@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('pais', 'nombre', 'codigo_iso',  'estado') 
    list_filter = ('estado', 'pais')
    search_fields = ('nombre', 'codigo_iso')
    fieldsets = (
        ('Información general', {
            'fields': ('pais', 'nombre', 'codigo_iso')
        }),
        ('Coordenadas geográficas', {
            'fields': ('latitud', 'longitud')
        }),
        ('Estado del registro', {
            'fields': ('estado',)
        }),
    )

@admin.register(EstadoCaso)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'icono']  # o cualquier otro campo que tengas    
    fieldsets = (
        ('Información general', {
            'fields': ('nombre', 'icono')
        }),
    )
        
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    
    list_display = ('pais','ciudad','username', 'email', 'name', 'es_admin', 'estado', 'is_staff', 'es_autoridad')
    list_filter = ('es_admin', 'estado', 'is_staff')

    fieldsets = (
        ('Informacion de Usuario', {'fields': ('username', 'password')}),
        ('Datos personales', {
            'fields': ('name', 'email', 'telefono', 'fecha_nacimiento', 'pais', 'ciudad')
        }),
        ('Políticas y accesos', {
            'fields': ('acepta_politicas', 'fecha_aceptacion', 'numero_intentos', 'fecha_ultimo_intento')
        }),
        ('Permisos y estado', {
            'fields': ('es_admin', 'estado', 'es_autoridad', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'name', 'email', 'password1', 'password2', 'pais', 'ciudad', 'es_admin', 'estado')}
        ),
    )

    search_fields = ('username', 'email', 'name')
    ordering = ('username',)
    
@admin.register(EntidadResponsable)
class EntidadResponsableAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'ciudad')
    filter_horizontal = ('usuarios',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'usuarios':
            kwargs["queryset"] = Usuario.objects.filter(es_autoridad=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def mostrar_autoridades(self, obj):
        return ", ".join([u.name for u in obj.usuarios.all()])
    mostrar_autoridades.short_description = "Autoridades"
    
    fieldsets = (
        ('Información general', {
            'fields': ('nombre', 'direccion', 'pais', 'ciudad')
        }),
        ('Autoridades', {
            'fields': ('usuarios',)
        }),
    )

class HistorialEstadoInline(admin.TabularInline):
    model = HistorialEstadoIncidente
    extra = 0
    readonly_fields = ('estado', 'usuario', 'comentario', 'fecha_cambio')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False  # evita añadir manualmente

    
@admin.register(Incidente)
class IncidenteAdmin(admin.ModelAdmin):
    list_display = ('numero_caso', 'usuario', 'estado', 'fecha_registro')
    list_filter = ('estado', 'fecha_registro', 'ciudad')
    search_fields = ('detalle', 'usuario__username', 'numero_caso')
    inlines = [HistorialEstadoInline]    
    fieldsets = (
        ('Datos del incidente', {
            'fields': ('direccion', 'detalle',)
        }),
        ('Ubicación', {
            'fields': ('pais', 'ciudad', 'latitud', 'longitud')
        }),
        ('Estado y usuario', {
            'fields': ('estado', 'usuario')
        }),
    )
        
    def save_model(self, request, obj, form, change):
        es_nuevo = not obj.pk
        estado_anterior = None

        if not es_nuevo:
            obj_anterior = Incidente.objects.get(pk=obj.pk)
            estado_anterior = obj_anterior.estado

        super().save_model(request, obj, form, change)

        # Solo guarda en historial si se cambió el estado
        if not es_nuevo and estado_anterior != obj.estado:
            HistorialEstadoIncidente.objects.create(
                incidente=obj,
                estado=obj.estado,
                usuario=request.user if request.user.is_authenticated else None,
                comentario="Cambio de estado desde el admin"
            )
            
@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'correo', 'telefono', 'fecha_envio')
    search_fields = ('nombres', 'apellidos', 'correo')
    list_filter = ('fecha_envio',)
    readonly_fields = ('fecha_envio',)
    fieldsets = (
        ('Datos del Contato', {
            'fields': ('nombres', 'apellidos', 'correo', 'telefono',)
        }),
        ('Reporte', {
            'fields': ('comentario','fecha_envio')
        }),
    )
