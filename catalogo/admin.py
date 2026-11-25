from django.contrib import admin

# Register your models here.
from .models import Libro,Autor,Editorial,Participacion

#admin.site.register(Libro)
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display=("titulo","isbn", "precio", "disponible", "editorial")
    list_filter = ("disponible", "editorial")
    search_fields = ("titulo", "isbn", "autores__nombre")
    ordering = ("titulo",)
    list_per_page = 20

admin.site.register(Autor)
admin.site.register(Editorial)
admin.site.register(Participacion)

