from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Miembros.models import Miembro, Membresia, MembresiaTipo
from rest_framework_simplejwt.tokens import RefreshToken

from Rutinas.models import RutinaEjercicio, Rutina


class LoginAPIView(APIView):
    def post(self, request):
        id = None
        print("Solicitud recibida")
        # Obtener los datos de la solicitud
        nombre = request.data.get('nombre')
        apellido = request.data.get('apellido')
        clave = request.data.get('clave')

        print(f"Intentando iniciar sesión con: {nombre} {apellido} {clave}")
        # Buscar al miembro por nombre y clave
        try:
            miembro = Miembro.objects.get(nombre=nombre, apellido=apellido, clave=clave)
            id = miembro.id
        except Miembro.DoesNotExist:
            print("Usuario no encontrado o datos incorrectos.")
            return Response({
                'detail': 'Usuario no encontrado o datos incorrectos.',
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Verificar que la membresía esté activa
        membresia = Membresia.obtner_membresia_activa(miembro)
        if not membresia:
            print("Membresía no activa o ha expirado.")
            return Response({
                'detail': 'La membresía no está activa o ha expirado.',
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Generación del token JWT
        refresh = RefreshToken.for_user(miembro)
        access_token = str(refresh.access_token)

        # Devolver el token
        return Response({
            'access_token': access_token,
            'id':id
        }, status=status.HTTP_200_OK)


class HomeAPIView(APIView):
    def post(self, request):
        clave=request.data.get('clave')
        miembro=Miembro.objects.get(clave=clave)
        membresia=Membresia.objects.get(miembro=miembro)
        membresia_tipo=MembresiaTipo.objects.get(membresia=membresia)
        rutina =Rutina.obtener_id_rutina(miembro)
        ejercicios=RutinaEjercicio.obtener_ejercicios_home(rutina.id_rutina)
        return Response(
        {
        'imagen':miembro.foto_cloud.url ,
        'nombre':miembro.nombre,
        'apellido':miembro.apellido,
        'membresia':membresia_tipo.nombre,
        'rutina':ejercicios,
        'rutina_nota':rutina.nota,
        }
        ,status=status.HTTP_200_OK)


class EjerciciosAPIView(APIView):
    def post(self, request):
        clave=request.data.get('clave')
        miembro=Miembro.objects.get(clave=clave)
        rutina =Rutina.obtener_id_rutina(miembro)
        ejercicios=RutinaEjercicio.obtener_ejercicios(rutina.id_rutina)
        return Response(
        {
        'rutina':ejercicios,
        }
        ,status=status.HTTP_200_OK)

class DatosAPIView(APIView):
    def post(self, request):
        clave = request.data.get('clave')
        miembro = Miembro.objects.get(clave=clave)
        membresia = Membresia.objects.get(miembro=miembro)
        membresia_tipo = MembresiaTipo.objects.get(membresia=membresia)
        return Response(
        {
        'imagen':miembro.foto_cloud.url ,
        'nombre':miembro.nombre,
        'apellido':miembro.apellido,
        'membresia':membresia_tipo.nombre,
        'expiracion':membresia.fecha_final,
        'clave':clave,
        'membresia_estado':'true',
        }
        ,status=status.HTTP_200_OK)