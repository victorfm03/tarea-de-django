from django.shortcuts import render
from .models import Libro

# Create your views here.
def lista_libros(request):
    libros = Libro.objects.all().order_by('titulo')
    contexto = {
        'libros': libros,
    }
    return render(request, 'catalogo/lista_libros.html', contexto)

def detalle_libro(request, pk):
    libro = Libro.objects.get(pk=pk)
    return render(request, 'catalogo/detalle_libro.html', {'libro': libro})
