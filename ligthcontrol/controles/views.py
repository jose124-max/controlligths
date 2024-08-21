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
            tempactual =float(temperatura)
            configuracion.temperaturaact = tempactual
            configuracion.save()
            if (configuracion.aireauto):
                dispositivo_aire = Dispositivo.objects.filter(tipo__nombre='Aire').first()
                if(configuracion.aire and configuracion.tempminima > tempactual):
                    configuracion.aire=False
                    configuracion.save()#encender luces
                    registro = Registro(
                        dispositivo=dispositivo_aire,
                        accion= False,
                        tipodeact='automatica'
                    )
                    registro.save()
                    print("Aire apagado automáticamente debido a detección de temperatura.")
                if(not configuracion.aire and configuracion.tempminima <= tempactual):
                    configuracion.aire=True
                    configuracion.save()#encender luces
                    registro = Registro(
                        dispositivo=dispositivo_aire,
                        accion= True,
                        tipodeact='automatica'
                    )
                    registro.save()
                    print("Aire encendido automáticamente debido a detección de temperatura.")


            return Response(f"Temperature updated to {temperatura}.", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class getCodOn(APIView):
    def get(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            estadotemp = configuracion.codonair

            return Response(estadotemp, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class postCodOn(APIView):
    def post(self, request, codon, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            configuracion.codonair = codon
            configuracion.solcodon=False
            configuracion.save()

            return Response(f"Temperature updated to {codon}.", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class getCodOff(APIView):
    def get(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            estadotemp = configuracion.codoffair

            return Response(estadotemp, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class postCodOff(APIView):
    def post(self, request, codoff, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            configuracion.codoffair = codoff
            configuracion.solcodoff=False
            configuracion.save()

            return Response(f"Temperature updated to {codoff}.", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class getSolOn(APIView):
    def get(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            estadotemp = configuracion.solcodon

            return Response(estadotemp, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class postSolOn(APIView):
    def post(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            configuracion.solcodon = True
            configuracion.save()

            return Response(f"Solon updated to TRUE.", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class getSolOff(APIView):
    def get(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            estadotemp = configuracion.solcodoff

            return Response(estadotemp, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class postSolOff(APIView):
    def post(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            configuracion.solcodoff = True
            configuracion.save()

            return Response(f"Soloff updated to TRUE.", status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AirStatusView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response("No configuration found.", status=status.HTTP_404_NOT_FOUND)

            # Obtener el estado de las luces
            estado_air = 1 if configuracion.aire else 0

            return Response(estado_air, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OnOffAirView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            configuracion = Configuracion.objects.first()

            if not configuracion:
                return Response({"detail": "No configuration found."}, status=status.HTTP_404_NOT_FOUND)

            # Cambiar el estado de 'luces'
            nuevo_estado = not configuracion.aire
            configuracion.aire = nuevo_estado
            configuracion.save()

            # Obtener el primer dispositivo de tipo "Luces"
            dispositivo_air = Dispositivo.objects.filter(tipo__nombre='Aire').first()

            if not dispositivo_air:
                return Response({"detail": "No device of type 'Aire' found."}, status=status.HTTP_404_NOT_FOUND)

            # Crear un registro
            registro = Registro(
                dispositivo=dispositivo_air,
                accion= nuevo_estado,  
                tipodeact='manual'
            )
            registro.save()

            # Serializar la respuesta
            serializer = ConfiguracionSerializer(configuracion)
            return Response({"detail": "Status updated successfully.", "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)