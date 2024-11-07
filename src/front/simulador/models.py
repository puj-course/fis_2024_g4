from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    contrasena = models.CharField(max_length=255)
    numero_telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre
