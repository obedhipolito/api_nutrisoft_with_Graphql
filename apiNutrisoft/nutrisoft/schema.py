import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql import GraphQLError


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
        model = get_user_model()
        fields = '__all__'

#crear usuario normal
class createUsuario(graphene.Mutation):
    usuario = graphene.Field(UsuarioType)

    class Arguments:
        nombresCompleto = graphene.String()
        correo = graphene.String()
        password = graphene.String()
        tipoUsuario = graphene.String()
    
    def mutate(self, info, nombresCompleto, correo, password, tipoUsuario):

        Usuario = get_user_model()

        usuario = Usuario.objects.create_user(correo=correo, password=password, nombresCompleto = nombresCompleto, tipoUsuario = tipoUsuario)

        usuario.set_password(password)
        usuario.save()
        return createUsuario(usuario=usuario)
    
#crear usuario nutriologo
class createNutriologo(graphene.Mutation):
    usuario = graphene.Field(UsuarioType)

    class Arguments:
        nombresCompleto = graphene.String()
        correo = graphene.String()
        password = graphene.String()
        tipoUsuario = graphene.String()
        cedula = graphene.String()
        informacion = graphene.String()
        direccion = graphene.Int()
    
    def mutate(self, info, nombresCompleto, correo, password, tipoUsuario, cedula, informacion, direccion):
        Usuario = get_user_model()
    
        direccion_id = None
        if direccion is not None:
            direccion_id = Direcccion.objects.get(pk=direccion)

        usuario = Usuario.objects.create_superuser(
            correo=correo,
            password=password,
            nombresCompleto=nombresCompleto,
            tipoUsuario=tipoUsuario,
            cedula=cedula,
            informacion=informacion,
            direccion=direccion_id
        )

        usuario.is_staff = True
        usuario.is_superuser = True

        usuario.set_password(password)
        usuario.save()
        return createNutriologo(usuario=usuario)



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
    
    def mutate(self, info, titulo, contenido, url_imagen): 

        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Debes estar logueado para crear una publicacion')
        
        if user.tipoUsuario != 'nutriologo':
            raise GraphQLError('Debes ser nutriologo para crear una publicacion')
        
        Usuario_autenticado = user

        publicacion = Publicacion(titulo=titulo, contenido=contenido, url_imagen=url_imagen, Usuario=Usuario_autenticado)
        publicacion.save()
        return createPublicacion(publicacion=publicacion)
    
#likes de publicacion
class createlikes(graphene.Mutation):
    publicacion = graphene.Field(PublicacionType)

    class Arguments:
        id = graphene.Int()
        likes = graphene.Int()
    
    def mutate(self, info, id, likes): 

        publicacion = Publicacion.objects.get(pk=id)
        publicacion.likes = likes
        publicacion.save()
        return createlikes(publicacion=publicacion)


#comentario

class ComentarioType(DjangoObjectType):
    class Meta:
        model = Comentario
        fields = '__all__'

class createComentario(graphene.Mutation):
    comentario = graphene.Field(ComentarioType)

    class Arguments:
        comentario = graphene.String()
        publicacion = graphene.Int()
    
    def mutate(self, info, comentario, publicacion):

        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Debes estar logueado para crear una publicacion')

        usuario = get_user_model().objects.get(pk=user.id)
    
        publicacion_id = Publicacion.objects.get(pk=publicacion)

        comentario = Comentario(comentario=comentario, usuario=usuario, publicacion=publicacion_id)
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
        nutrilogo_id = graphene.Int()
    
    def mutate(self, info, Comentario, calificacion, nutrilogo_id): 
        
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Debes estar logueado para crear una publicacion')

        usuario = get_user_model().objects.get(pk=user.id)
        nutriologo = Usuario.objects.get(pk=nutrilogo_id)


        calificacion = Calificacion(Comentario=Comentario, calificacion=calificacion, usuario=usuario, nutriologo=nutriologo)
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
    
    def mutate(self, info, publicacion): 

        user = info.context.user
        if user.is_anonymous:   
            raise GraphQLError('Debes estar logueado para crear guardar una publicacion')

        usuario = get_user_model().objects.get(pk=user.id)  
        publicacion = Publicacion.objects.get(pk=publicacion)
        
        publicacionGuardada = PublicacionGuardada(publicacion=publicacion, usuario=usuario)
        publicacionGuardada.save()
        return createPublicacionGuardada(publicacionGuardada=publicacionGuardada)

#query

class Query(graphene.ObjectType):
    direcciones = graphene.List(DireccionType)
    usuarios = graphene.List(UsuarioType)
    publicaciones = graphene.List(PublicacionType)
    comentarios = graphene.List(ComentarioType,id=graphene.Int())
    calificaciones = graphene.List(CalificacionType)
    publicacionesGuardadas = graphene.List(PublicacionGuardadaType)

    likesPublicacion = graphene.Int(id=graphene.Int())
    conectado = graphene.Field(UsuarioType)

    def resolve_conectado(self, info):
        usuario = info.context.user
        if usuario.is_anonymous:
            raise Exception('no se a iniciado sesion')
        return usuario
    
    def resolve_likesPublicacion(self, info, id):
        publicacion=Publicacion.objects.get(pk=id)
        return publicacion.likes
    

    def resolve_direcciones(self, info):
        return Direcccion.objects.all()
    
    def resolve_usuarios(self, info):
        return get_user_model().objects.all()
    
    def resolve_publicaciones(self, info):
        return Publicacion.objects.all()
    
    def resolve_comentarios(self, info, id):
        publicacion=Publicacion.objects.get(pk=id)
        return Comentario.objects.filter(publicacion=publicacion)
    
    def resolve_calificaciones(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Debes estar logueado para ver tus calificaciones')
        usuario = get_user_model().objects.get(pk=user.id)
        return Calificacion.objects.filter(usuario=usuario)
    
    def resolve_publicacionesGuardadas(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Debes estar logueado para ver tus publicaciones guardadas')
        usuario = get_user_model().objects.get(pk=user.id)
        return PublicacionGuardada.objects.filter(usuario=usuario)
    


#mutation

class Mutation(graphene.ObjectType):
    create_direccion = createDireccion.Field()
    create_usuario = createUsuario.Field()
    create_publicacion = createPublicacion.Field()
    create_comentario = createComentario.Field()
    create_calificacion = createCalificacion.Field()
    create_publicacionGuardada = createPublicacionGuardada.Field()
    createNutriologo = createNutriologo.Field()
    create_like = createlikes.Field()

    