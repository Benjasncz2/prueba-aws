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
from django.urls import path
from myapp import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('boxes/', views.disponibilidad_boxes, name='disponibilidad_boxes'),
    path('panel/', views.panel_admin),
    path('dashboard/', views.dashboard),
    path('personal/', views.personal),
    path('agenda/', views.agenda),
    path('implementos/', views.implementos),
    path('cambiar_estado/<int:implemento_id>/<int:box_id>/<int:nuevo_estado>/',views.cambiar_estado_implemento,name='cambiar_estado'),
    path('box/<int:box_id>/', views.box_detail, name='box_detail')
]
