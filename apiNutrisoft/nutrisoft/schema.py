import graphene
from graphene_django import DjangoObjectType

from nutrisoft.models import Direcccion, Usuario, Publicacion, Comentario, Calificacion, PublicacionGuardada

#direccion

class DireccionType(DjangoObjectType):
    class Meta:
        model = Direcccion
        fields = '__all__'

class createDireccion(graphene.Mutation):
    direccion = graphene.Field(DireccionType)

    class Arguments:
        calle = graphene.String()
        numero = graphene.Int()
        colonia = graphene.String()
        codigoPostal = graphene.Int()
        ciudad = graphene.String()
        estado = graphene.String()
        pais = graphene.String()
    
    def mutate(self, info, calle, numero, colonia, codigoPostal, ciudad, estado, pais): 
        direccion = Direcccion(calle=calle, numero=numero, colonia=colonia, codigoPostal=codigoPostal, ciudad=ciudad, estado=estado, pais=pais)
        direccion.save()
        return createDireccion(direccion=direccion)
    

#usuario

class UsuarioType(DjangoObjectType):
    class Meta:
        model = Usuario
        fields = '__all__'

class createUsuario(graphene.Mutation):
    usuario = graphene.Field(UsuarioType)

    class Arguments:
        nombresCompleto = graphene.String()
        correo = graphene.String()
        password = graphene.String()
        cedula = graphene.String()
        informacion = graphene.String()
        tipoUsuario = graphene.String()
        calificacion = graphene.Int()
        direccion = graphene.Int()
        publicaciones = graphene.Int()
        PublicacionGuardada = graphene.Int()
    
    def mutate(self, info, nombresCompleto, correo, password, cedula, informacion, tipoUsuario, calificacion, direccion, publicaciones, PublicacionGuardada): 

        calificacion = Calificacion.objects.get(pk=calificacion)
        direccion = Direcccion.objects.get(pk=direccion)
        publicaciones = Publicacion.objects.get(pk=publicaciones)
        PublicacionGuardada = PublicacionGuardada.objects.get(pk=PublicacionGuardada)

        usuario = Usuario(nombresCompleto=nombresCompleto, correo=correo, password=password, cedula=cedula, informacion=informacion, tipoUsuario=tipoUsuario, calificacion=calificacion, direccion=direccion, publicaciones=publicaciones, PublicacionGuardada=PublicacionGuardada)
        usuario.save()
        return createUsuario(usuario=usuario)


#publicacion

class PublicacionType(DjangoObjectType):
    class Meta:
        model = Publicacion
        fields = '__all__'

class createPublicacion(graphene.Mutation):
    publicacion = graphene.Field(PublicacionType)

    class Arguments:
        titulo = graphene.String()
        contenido = graphene.String()
        url_imagen = graphene.String()
        likes = graphene.Int()
        comentarios = graphene.String()
        Usuario = graphene.Int()
    
    def mutate(self, info, titulo, contenido, url_imagen, likes, comentarios, Usuario): 

        Usuario = Usuario.objects.get(pk=Usuario)
        comentarios = Comentario.objects.get(pk=comentarios)

        publicacion = Publicacion(titulo=titulo, contenido=contenido, url_imagen=url_imagen, likes=likes, comentarios=comentarios, Usuario=Usuario)
        publicacion.save()
        return createPublicacion(publicacion=publicacion)


#comentario

class ComentarioType(DjangoObjectType):
    class Meta:
        model = Comentario
        fields = '__all__'

class createComentario(graphene.Mutation):
    comentario = graphene.Field(ComentarioType)

    class Arguments:
        comentario = graphene.String()
        usuario = graphene.Int()
        publicacion = graphene.Int()
    
    def mutate(self, info, comentario, usuario, publicacion):

        usuario = Usuario.objects.get(pk=usuario)
        publicacion = Publicacion.objects.get(pk=publicacion)

        comentario = Comentario(comentario=comentario, usuario=usuario, publicacion=publicacion)
        comentario.save()
        return createComentario(comentario=comentario)


#calificacion

class CalificacionType(DjangoObjectType):
    class Meta:
        model = Calificacion
        fields = '__all__'

class createCalificacion(graphene.Mutation):
    calificacion = graphene.Field(CalificacionType)

    class Arguments:
        Comentario = graphene.String()
        calificacion = graphene.Int()
        usuario = graphene.Int()
    
    def mutate(self, info, Comentario, calificacion, usuario): 

        usuario = Usuario.objects.get(pk=usuario)


        calificacion = Calificacion(Comentario=Comentario, calificacion=calificacion, usuario=usuario)
        calificacion.save()
        return createCalificacion(calificacion=calificacion)


#publicacion guardada

class PublicacionGuardadaType(DjangoObjectType):
    class Meta:
        model = PublicacionGuardada
        fields = '__all__'

class createPublicacionGuardada(graphene.Mutation):
    publicacionGuardada = graphene.Field(PublicacionGuardadaType)

    class Arguments:
        publicacion = graphene.Int()
        usuario = graphene.Int()
    
    def mutate(self, info, publicacion, usuario): 

        publicacion = Publicacion.objects.get(pk=publicacion)
        usuario = Usuario.objects.get(pk=usuario)
        
        publicacionGuardada = PublicacionGuardada(publicacion=publicacion, usuario=usuario)
        publicacionGuardada.save()
        return createPublicacionGuardada(publicacionGuardada=publicacionGuardada)

#query

class Query(graphene.ObjectType):
    direcciones = graphene.List(DireccionType)
    usuarios = graphene.List(UsuarioType)
    publicaciones = graphene.List(PublicacionType)
    comentarios = graphene.List(ComentarioType)
    calificaciones = graphene.List(CalificacionType)
    publicacionesGuardadas = graphene.List(PublicacionGuardadaType)

    def resolve_direcciones(self, info):
        return Direcccion.objects.all()
    
    def resolve_usuarios(self, info):
        return Usuario.objects.all()
    
    def resolve_publicaciones(self, info):
        return Publicacion.objects.all()
    
    def resolve_comentarios(self, info):
        return Comentario.objects.all()
    
    def resolve_calificaciones(self, info):
        return Calificacion.objects.all()
    
    def resolve_publicacionesGuardadas(self, info):
        return PublicacionGuardada.objects.all()

#mutation

class Mutation(graphene.ObjectType):
    create_direccion = createDireccion.Field()
    create_usuario = createUsuario.Field()
    create_publicacion = createPublicacion.Field()
    create_comentario = createComentario.Field()
    create_calificacion = createCalificacion.Field()
    create_publicacionGuardada = createPublicacionGuardada.Field()

    