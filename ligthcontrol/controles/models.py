from django.db import models

# Modelo Tipo
class Tipo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

# Modelo Dispositivo
class Dispositivo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name='dispositivos')

    def __str__(self):
        return self.nombre

# Modelo Registro
class Registro(models.Model):
    id = models.AutoField(primary_key=True)
    fechahora = models.DateTimeField(auto_now_add=True)
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name='registros')
    accion = models.BooleanField()  # True para encender, False para apagar
    tipodeact = models.CharField(max_length=10, choices=[('manual', 'Manual'), ('automatica', 'Automática')])

    def __str__(self):
        return f"{self.dispositivo.nombre} - {self.fechahora} - {'Encendido' if self.accion else 'Apagado'}"

# Modelo Configuracion
class Configuracion(models.Model):
    id = models.AutoField(primary_key=True)
    luces = models.BooleanField(default=False)
    aire = models.BooleanField(default=False)
    lucesauto = models.BooleanField(default=False)
    aireauto = models.BooleanField(default=False)
    tmmovON = models.IntegerField(help_text="Tiempo en segundos para encender luces al detectar movimiento")
    tmmovOFF = models.IntegerField(help_text="Tiempo en segundos sin movimiento para apagar luces")
    tempminima = models.FloatField(help_text="Temperatura mínima para encender aire acondicionado")
    temppagar = models.FloatField(help_text="Temperatura máxima para apagar aire acondicionado")

    def __str__(self):
        return "Configuración Actual"
