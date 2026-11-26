from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from .models import Libro,Editorial,Autor,Participacion,Prestamo
from django.db.models import Q,Prefetch,Count
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils import timezone


# Create your views here.
def lista_libros(request):
    """libros = Libro.objects.filter(Q(Q(titulo__icontains='Django') & Q(titulo__icontains='Python')))
    for libro in libros:
        print(libro.titulo)"""
    libros =Libro.objects.all()
    contexto={
        "libros":libros
    }
    return render(request, 'catalogo/lista_libros.html',contexto)

def detalle_libro(request, pk):
    libro = get_object_or_404(
        Libro.objects.select_related("editorial").prefetch_related("autores"),
        pk=pk
    )

    return render(request, 'catalogo/detalle_libro.html', {'libro': libro})


def editorial(request, pk):
    editorial= get_object_or_404(Editorial, pk=pk)
    """libros= editorial.libros.all()"""
    return render(request, "catalogo/editorial.html",{'editorial':editorial})

def autor(request, pk):
    autor=get_object_or_404(Autor, pk=pk)

    return render(request, "catalogo/autor.html", {'autor':autor})

def editoriales(request):
    editoriales = Editorial.objects.annotate(total_libros=Count("libros")).prefetch_related(
        Prefetch(
            "libros",
            queryset=Libro.objects.filter(disponible=True),
            to_attr="libros_disponibles",
        )
    )
    return render(request, "catalogo/editoriales.html",{'editoriales':editoriales})

def participaciones(request):

    participaciones=Participacion.objects.select_related("libro","autor")
    return render(request, "catalogo/participaciones.html",{'participaciones':participaciones})


def prestar_libro(request,pk_libro, pk_usuario):
    with transaction.atomic():
        libro=Libro.objects.select_for_update().get(pk=pk_libro)
        if not libro.disponible:
            raise ValueError("El libro no esta disponible")

        usuario=get_user_model().objects.get(pk=pk_usuario)

        prestamo= Prestamo.objects.create(
            libro=libro,
            usuario=usuario,
        )
        libro.disponible=False
        libro.save(update_fields=["disponible"])
        return HttpResponse("prestamo realizado")


def devolver_libro(request,pk_prestamo):
    with transaction.atomic():
        prestamo=Prestamo.objects.select_for_update().get(pk=pk_prestamo)

        if prestamo.fecha_devolucion is not None:
            raise ValueError("El prestamo ya se devolvio")

        prestamo.fecha_devolucion= timezone.now()
        prestamo.save(update_fields=["fecha_devolucion"])
        prestamo.libro.disponible = True
        prestamo.libro.save(update_fields=["disponible"])

        return render(request,'catalogo/devolucion_realizada.html',{'prestamo':prestamo})