from django.db import models

# Create your models here.
class Libro(models.Model):
    class Genero(models.TextChoices):
            TEATRO = 'Teatro', 'Teatro'
            ENSAYO = 'Ensayo', 'Ensayo'
            COMIC  = 'Cómic', 'Cómic'
            POESIA = 'Poesía', 'Poesía'
            NOVELA ='Novela', 'Novela'

    class Dificultad(models.TextChoices):
            BASICA = 'Básica', 'Básica'
            INTERMEDIA = 'Intermedia', 'Intermedia'
            AVANZADA = 'Avanzada', 'Avanzada'

    titulo = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    sinopsis = models.TextField(blank=True, null=True)
    fecha_publicacion = models.DateField()
    paginas = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    genero = models.CharField(max_length=20, choices=Genero.choices, default=Genero.NOVELA)
    dificultad = models.CharField(max_length=20, choices=Dificultad.choices, default=Dificultad.BASICA)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Editorial(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

class Meta:
        ordering = ["titulo", "nombre"]
        verbose_name = ["Libro", "Autor"]
        verbose_name_plural = ["Libros", "Autores"]