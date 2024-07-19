from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('libros/', views.libros, name='libros'),
    path('crear_libro/', views.crear_libro, name='crear_libro'),
    path('autores/', views.autores, name='autores'),
    path('cupones/', views.cupones, name='cupones'),
    path('crear_cupon/', views.crear_cupon, name='crear_cupon'),
    path('libros/<uuid:libro_id>/', views.detalle_libro, name='detalle_libro'),
]
