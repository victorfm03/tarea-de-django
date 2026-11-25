from django.db import models
from django.conf import settings

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
    editorial=models.ForeignKey("Editorial", on_delete=models.PROTECT, related_name="libros",null=True, blank=True)
    autores=models.ManyToManyField("Autor",related_name="libros",blank=True)

    def __str__(self):
        return f"{self.isbn} {self.titulo} {self.precio} {self.disponible} {self.editorial}"

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

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil"
    )
    telefono = models.CharField(max_length=20, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario}"


class PerfilUsuario(models.Model):
    usuario=models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
        )
    telefono = models.CharField(max_length=20, blank=True)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario}"


class Participacion(models.Model):
     class Funcion(models.TextChoices):
          PRINCIPAL="PRI","Autor principal"
          COAUTOR="COA", "Coautor"
          COLABORADOR="COL","Colaborador"

     libro=models.ForeignKey(Libro, on_delete=models.CASCADE, related_name="participaciones")
     autor=models.ForeignKey(Autor, on_delete=models.CASCADE, related_name="participaciones")
     funcion=models.CharField(max_length=3, choices=Funcion.choices, default=Funcion.COAUTOR)

class Prestamo(models.Model):
    libro = models.ForeignKey(
        "Libro", on_delete=models.PROTECT,
        related_name="prestamos"
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="prestamos_biblioteca"
    )
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    fecha_devolucion = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Préstamo {self.pk}: {self.libro}"


class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["libro", "autor"], name="participacion_unica_libro_autor"
            )
        ]

def __str__(self):
        return f"{self.autor} - {self.libro} ({self.get_funcion_display()})"
