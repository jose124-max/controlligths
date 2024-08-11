from rest_framework import serializers
from .models import Tipo, Dispositivo, Registro, Configuracion

# Serializador para el modelo Tipo
class TipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipo
        fields = ['id', 'nombre', 'descripcion']

# Serializador para el modelo Dispositivo
class DispositivoSerializer(serializers.ModelSerializer):
    tipo = TipoSerializer(read_only=True)
    tipo_id = serializers.PrimaryKeyRelatedField(queryset=Tipo.objects.all(), source='tipo')

    class Meta:
        model = Dispositivo
        fields = ['id', 'nombre', 'tipo', 'tipo_id']

# Serializador para el modelo Registro
class RegistroSerializer(serializers.ModelSerializer):
    dispositivo = DispositivoSerializer(read_only=True)
    dispositivo_id = serializers.PrimaryKeyRelatedField(queryset=Dispositivo.objects.all(), source='dispositivo')

    class Meta:
        model = Registro
        fields = ['id', 'fechahora', 'dispositivo', 'dispositivo_id', 'accion', 'tipodeact']

# Serializador para el modelo Configuracion
class ConfiguracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Configuracion
        fields = [
            'id', 'luces', 'aire', 'lucesauto', 'aireauto', 
            'tmmovON', 'tmmovOFF', 'tempminima', 'temppagar'
        ]
