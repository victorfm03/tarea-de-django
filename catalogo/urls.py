from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('<int:pk>/', views.detalle_libro, name='detalle_libro'),
    path('editorial/<int:pk>/', views.editorial, name='editorial'),
    path('autor/<int:pk>/', views.autor, name='autor'),
    path('editoriales', views.editoriales, name='editoriales'),
    path('participaciones',views.participaciones,name="participaciones"),
    path('prestar_libro/<int:pk_libro>/<int:pk_usuario>',views.prestar_libro,name='prestar_libro'),
    path('devolver_libro/<int:pk_prestamo>',views.devolver_libro,name='devolver_libro'),
]