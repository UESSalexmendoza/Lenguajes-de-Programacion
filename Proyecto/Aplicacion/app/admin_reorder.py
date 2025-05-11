from admin_reorder.admin import ModelAdminReorder

class MyModelAdminReorder(ModelAdminReorder):
    reorder = [
        'auth',  # Para mantener la sección de usuarios
        {
            'app': 'app',  # Reemplaza 'app' con el nombre real de tu app si no se llama así
            'models': [
                'app.Pais',
                'app.Ciudad',
                'app.EstadoCaso',
                'app.Usuario',
                'app.EntidadResponsable',
                'app.Incidente',
            ]
        },
    ]
