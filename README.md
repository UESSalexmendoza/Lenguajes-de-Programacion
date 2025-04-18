
# VozUrbana 🌆

**Plataforma de Reporte Ciudadano de Problemas Urbanos**

VozUrbana es una aplicación web que permite a los ciudadanos reportar problemas del entorno urbano como baches, luminarias apagadas, acumulación de basura, entre otros. A través de un sistema con geolocalización, imágenes y votación comunitaria, la plataforma promueve la participación ciudadana y la colaboración con las autoridades locales para mejorar la calidad de vida en las ciudades.

---

## 🚀 Características principales

- 📍 Geolocalización de reportes mediante mapa interactivo.
- 📝 Creación de reportes con título, descripción, categoría e imagen.
- 🌐 Visualización de todos los reportes en un mapa público.
- ✅ Filtro por estado (nuevo, en proceso, resuelto) y categoría.
- 👍 Sistema de votación para priorizar los reportes más urgentes.
- 🔐 Gestión de usuarios: registro, login y recuperación de contraseña.
- 🛠️ Panel de administración para seguimiento y actualización de reportes.

---

## ⚙️ Tecnologías utilizadas

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap  
- **Backend**: Python, Django  
- **Base de datos**: MySQL  
- **Geolocalización**: Google Maps API  
- **Control de versiones**: Git  

---

## 📦 Requisitos de instalación

1. Python 3.x instalado
2. MySQL Server activo y configurado
3. Crear un entorno virtual:
   ```bash
   python -m venv env
   source env/bin/activate  # En Linux/Mac
   env\Scripts\activate     # En Windows
   ```
4. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Configurar conexi贸n a base de datos en `settings.py`
6. Ejecutar migraciones y correr el servidor:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

---

## 👨‍💻 Equipo de desarrollo

- **Alex Mendoza**  
  - _Documentación_  
  - _Desarrollo_
  - _QA_
- **Carlos Plua**  
  - _Backend_
  - _Reportes_
- **David Tello**  
  - _Frontend_
  - _QA_

---

## 📝 Licencia

Este proyecto fue desarrollado con fines académicos para la asignatura Lenguajes de Programación. Puedes utilizarlo como referencia para proyectos educativos.

---

## 📌 Notas

-Este repositorio contiene la versión prototipo funcional del sistema.
-Se recomienda desplegar en servidor con soporte para Django + MySQL.
-Futuras versiones podrán incluir app móvil, autenticación avanzada y más estadísticas.
