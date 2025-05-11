from django.views.generic import CreateView
from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
from .forms import CustomLoginForm
from .forms import CustomPasswordResetForm
from .forms import CustomSetPasswordForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Usuario
from .forms import UsuarioCreationForm
from django.utils import timezone

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Incidente, EstadoCaso
from django.utils.timezone import localtime
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from .models import EntidadResponsable, Pais, Ciudad
from .forms import ContactoForm

def index(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

class CustomLoginView(LoginView):
    template_name = 'app/login.html'  # usará esta plantilla
    redirect_authenticated_user = True
    authentication_form = CustomLoginForm
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'app/password_reset.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'app/password_reset_email.html'
    subject_template_name = 'app/password_reset_subject.txt'
    success_url = '/recuperar-clave/enviado/'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'app/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = '/recuperar-clave/completado/'
    
def logout_view(request):
    logout(request)
    return redirect('/')

class UsuarioCreateView(CreateView):
    model = Usuario
    form_class = UsuarioCreationForm
    template_name = 'app/usuario_form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.fecha_aceptacion = timezone.now() if form.cleaned_data['acepta_politicas'] else None
        user = form.save(commit=False)
        user.estado = False
        user.is_active = False
        user.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_link = self.request.build_absolute_uri(
            reverse('activar_cuenta', kwargs={'uidb64': uid, 'token': token})
        )

        # Email
        subject = 'Activa tu cuenta en VozUrbana'
        message = render_to_string('app/email_activacion.html', {
            'user': user,
            'activation_link': activation_link
        })
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        return super().form_valid(form)        

def activar_cuenta(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Usuario.objects.get(pk=uid)
        print("Usuario:", user.username)       
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None: #and default_token_generator.check_token(user, token):
        user.estado = True
        user.is_active = True
        user.save()

        # Verifica inmediatamente si se guardó
        user.refresh_from_db()
        print("✅ Activado:", user.username, "Estado:", user.estado, "is_active:", user.is_active)

        messages.success(request, 'Tu cuenta ha sido activada correctamente.')
        return redirect('login')
    else:
        print("❌ Token inválido o usuario no encontrado.")
        messages.error(request, 'El enlace de activación no es válido o ha expirado.')
        return redirect('login')

def mapa_incidentes(request):
    return render(request, 'app/mapa.html')


def incidentes_json(request):
    publicado = EstadoCaso.objects.filter(nombre__icontains='publicado').first()
    
    if request.user.is_authenticated:
        incidentes = Incidente.objects.filter(
            Q(usuario=request.user) | Q(estado=publicado)
        ).select_related('estado', 'entidad_responsable', 'usuario')
    else:
        incidentes = Incidente.objects.filter(
            estado=publicado
        ).select_related('estado', 'entidad_responsable', 'usuario')
    
    data = [
        {
            'lat': i.latitud,
            'lng': i.longitud,
            'detalle': i.detalle,
            'estado': i.estado.nombre,
            'icono': i.estado.icono,
            'entidad': i.entidad_responsable.nombre if i.entidad_responsable else 'No asignada',
            'usuario': i.usuario.name if i.usuario else 'Desconocido',
            'fecha': localtime(i.fecha_registro).strftime('%d/%m/%Y %H:%M'),
        }
        for i in incidentes
    ]
    return JsonResponse(data, safe=False)

def mapa_incidentes(request):
    entidades = EntidadResponsable.objects.all()
    paises = Pais.objects.all()
    ciudades = Ciudad.objects.all()

    return render(request, 'app/mapa.html', {
        'entidades': entidades,
        'paises': paises,
        'ciudades': ciudades,
    })

@login_required
def crear_incidente(request):
    if request.method == 'POST':
        detalle = request.POST.get('detalle')
        lat = request.POST.get('latitud')
        lng = request.POST.get('longitud')
        entidad_id = request.POST.get('entidad_responsable')
        pais_id = request.POST.get('pais')
        ciudad_id = request.POST.get('ciudad')
        direccion = request.POST.get('direccion')

        entidad = get_object_or_404(EntidadResponsable, pk=entidad_id)
        pais = get_object_or_404(Pais, pk=pais_id)
        ciudad = get_object_or_404(Ciudad, pk=ciudad_id)

        Incidente.objects.create(
            detalle=detalle,
            usuario=request.user,
            latitud=lat,
            longitud=lng,
            entidad_responsable=entidad,
            pais=pais,
            ciudad=ciudad,
            direccion=direccion
        )

        return redirect('mapa_incidentes')

def politica_privacidad(request):
    return render(request, 'app/politica_privacidad.html')

def terminos_condiciones(request):
    return render(request, 'app/terminos_condiciones.html')

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacto_exito')
    else:
        form = ContactoForm()
    return render(request, 'app/contacto.html', {'form': form})

def contacto_exito(request):
    return render(request, 'app/contacto_exito.html')

@login_required
def mis_incidentes(request):
    incidentes = Incidente.objects.filter(usuario=request.user).select_related('ciudad', 'pais', 'estado', 'entidad_responsable')
    return render(request, 'app/mis_incidentes.html', {'incidentes': incidentes})