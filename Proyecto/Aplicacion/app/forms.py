from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Usuario, Contacto

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuario',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
        })

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'id': 'id_email'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        UserModel = get_user_model()
        if not UserModel.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError(_("No existe ninguna cuenta activa con este correo electrónico."))
        return email
    
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nueva contraseña',
            'id': 'new_password1',
        })

        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'id': 'new_password2',
        })    
        
class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'password1', 'password2', 'name', 'email', 'telefono',
            'fecha_nacimiento', 'pais', 'ciudad', 'es_admin', 'acepta_politicas'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'acepta_politicas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'es_admin': forms.CheckboxInput(attrs={'class': 'form-check-input'}),            
            'es_autoridad ': forms.CheckboxInput(attrs={'class': 'form-check-input'}),            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields[field_name]
            existing_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing_classes} form-control'.strip()
            field.widget.attrs['placeholder'] = field.label        

class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombres', 'apellidos', 'correo', 'telefono', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'maxlength': 1000,
                'style': 'resize: none;height: 120px;',
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario u observación...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'comentario':  # Ya configurado arriba
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label




        
