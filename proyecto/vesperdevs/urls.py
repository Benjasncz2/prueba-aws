"""
URL configuration for vesperdevs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp import views 
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1) Ruta para el archivo de verificación de Google:
    path(
        'boxes/google0eab2047eed3db07a.html',
        TemplateView.as_view(
            template_name='google0eab2047eed3db07a.html',
            content_type='text/html'
        ),
        name='google_site_verification'
    ),

    # 2) Tus rutas normales:
    path('', views.login),
    path('login/', views.login, name='login'),
    path('boxes/', views.disponibilidad_boxes, name='disponibilidad_boxes'),
    path('panel/', views.panel_admin),
    path('dashboard/', views.dashboard),
    path('personal/', views.personal),
    path('agenda/', views.agenda),
    path('implementos/', views.implementos),
    path(
        'cambiar_estado/<int:implemento_id>/<int:box_id>/<int:nuevo_estado>/',
        views.cambiar_estado_implemento,
        name='cambiar_estado'
    ),
    path('box/<int:box_id>/', views.box_detail, name='box_detail'),
]