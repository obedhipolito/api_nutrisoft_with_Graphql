from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

"""class UserManager(BaseUserManager):
    def create_user(self, correo, password=None, tipoUsuario='normal', **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es necesario para crear un usuario')
        user = self.model(correo=self.normalize_email(correo), tipoUsuario=tipoUsuario, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, tipoUsuario='nutriologo', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('tipoUsuario', tipoUsuario)
        return self.create_user(correo, password, tipoUsuario, **extra_fields)"""


class Direcccion(models.Model):
    calle = models.CharField(max_length=50, blank=False, null=False)
    colonia = models.CharField(max_length=50, blank=False, null=False)
    numero = models.IntegerField(blank=False, null=False)
    codigoPostal = models.IntegerField(blank=False, null=False)
    ciudad = models.CharField(max_length=50, blank=False, null=False)
    estado = models.CharField(max_length=50, blank=False, null=False)
    pais = models.CharField(max_length=50, blank=False, null=False)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombresCompleto = models.CharField(max_length=100, blank=False, null=False)
    correo = models.EmailField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=10, blank=False, null=False)
    cedula = models.CharField(max_length=22, blank=True, null=True, default='')
    informacion = models.CharField(max_length=250, blank=True, null=True, default='')
    tipoUsuario = models.CharField(max_length=10, blank=False, null=False)
    calificacion =  models.ForeignKey('Calificacion', null=True, on_delete=models.CASCADE, related_name='calificacion_usuario')
    direccion = models.ForeignKey(Direcccion, null=True, on_delete=models.CASCADE)
    publicaciones = models.ForeignKey('Publicacion', null=True, on_delete=models.CASCADE)
    PublicacionGuardada = models.ForeignKey('PublicacionGuardada', null=True, on_delete=models.CASCADE, related_name='publicacion_guardada_usuario')

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['password', 'tipoUsuario']

class Publicacion(models.Model):
    titulo = models.CharField(max_length=250, blank=False, null=False)
    contenido = models.CharField(max_length=1000, blank=False, null=False)   
    url_imagen = models.CharField(max_length=250, blank=True, null=True, default='')  
    likes = models.IntegerField(blank=True, null=True, default=0)
    fecha = models.DateTimeField(null=False, auto_now_add=True)
    comentarios = models.ForeignKey('Comentario', null=True, on_delete=models.CASCADE, related_name='comentarios_publicacion') 
    Usuario = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE, related_name='publicaciones_usuario')

class Comentario(models.Model):
    comentario = models.CharField(max_length=1000, blank=False, null=False)   
    fecha = models.DateTimeField(null=False, auto_now_add=True)
    usuario = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE)
    publicacion = models.ForeignKey(Publicacion, null=False, on_delete=models.CASCADE)

class Calificacion(models.Model):
    Comentario = models.CharField(max_length=500, blank=False, null=False)
    fecha = models.DateTimeField(null=False, auto_now_add=True)
    calificacion = models.IntegerField(null=False)
    usuario = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE, related_name='calificaciones_usuario')

class PublicacionGuardada(models.Model):
    publicacion = models.ForeignKey(Publicacion, null=False, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, null=False, on_delete=models.CASCADE)