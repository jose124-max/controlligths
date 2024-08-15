from rest_framework import generics, viewsets
from .models import Tipo, Dispositivo, Registro, Configuracion
from .serializers import TipoSerializer, DispositivoSerializer, RegistroSerializer, ConfiguracionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Configuracion

# Vista para el modelo Tipo
class TipoViewSet(viewsets.ModelViewSet):
    queryset = Tipo.objects.all()
    serializer_class = TipoSerializer

# Vista para el modelo Dispositivo
class DispositivoViewSet(viewsets.ModelViewSet):
    queryset = Dispositivo.objects.all()
    serializer_class = DispositivoSerializer

# Vista para el modelo Registro
class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

# Vista para el modelo Configuracion
class ConfiguracionViewSet(viewsets.ModelViewSet):
    queryset = Configuracion.objects.all()
    serializer_class = ConfiguracionSerializer


class OnOffLightsView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response({"detail": "No configuration found."}, status=status.HTTP_404_NOT_FOUND)

            # Cambiar el estado de 'luces'
            nuevo_estado = not configuracion.luces
            configuracion.luces = nuevo_estado
            configuracion.save()

            # Obtener el primer dispositivo de tipo "Luces"
            dispositivo_luces = Dispositivo.objects.filter(tipo__nombre='Luces').first()

            if not dispositivo_luces:
                return Response({"detail": "No device of type 'Luces' found."}, status=status.HTTP_404_NOT_FOUND)

            # Crear un registro
            registro = Registro(
                dispositivo=dispositivo_luces,
                accion= nuevo_estado,  
                tipodeact='manual'
            )
            registro.save()

            # Serializar la respuesta
            serializer = ConfiguracionSerializer(configuracion)
            return Response({"detail": "Status updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class LightsStatusView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            # Obtener el estado de las luces
            estado_luces = 1 if configuracion.luces else 0

            return Response(estado_luces, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class tempsStatusView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            estadotemp = configuracion.temperaturaact

            return Response(estadotemp, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class tempsStatusPost(APIView):
    def post(self, request, temperatura, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            configuracion.temperaturaact = float(temperatura)
            configuracion.save()

            return Response(f"Temperature updated to {temperatura}.", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)