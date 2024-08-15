import cv2
import numpy as np
import time
from controles.models import Configuracion, Registro, Dispositivo 

# Usar la cámara conectada
video = cv2.VideoCapture(0)

i = 0
bgGray = None
accumulated_diff = None
reset_interval = 300  # Número de cuadros después del cual se reinicia el fondo
last_motion_time = time.time()  # Tiempo de la última detección de movimiento
dispositivo_luces = Dispositivo.objects.filter(tipo__nombre='Luces').first()

url_camara = Configuracion.objects.first().urlcamara

try:
    camera_index = int(url_camara)
    video = cv2.VideoCapture(camera_index)  
except ValueError:
    video = cv2.VideoCapture(url_camara) 

print('XD')
while True:
    config = Configuracion.objects.first() 
    no_motion_time_limit = config.tmmovOFF  # Tiempo en segundos para apagar las luces después de no detectar movimiento
    if config.lucesauto==True:
        ret, frame = video.read()
        if not ret:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (11, 11), 0)  # Reducir el desenfoque para detectar detalles más pequeños
        
        # Reiniciar el fondo y acumulado después de un cierto número de cuadros
        if i % reset_interval == 0:
            bgGray = None
            accumulated_diff = None
            i = 0  # Reiniciar contador para evitar overflow
        
        # Establecer el fondo al primer frame después de reiniciar
        if bgGray is None and i == 20:
            bgGray = gray
        elif i > 20 and bgGray is not None:
            dif = cv2.absdiff(gray, bgGray)
            _, th = cv2.threshold(dif, 30, 255, cv2.THRESH_BINARY) 
            
            if accumulated_diff is None:
                accumulated_diff = np.zeros_like(th)
            
            accumulated_diff = cv2.addWeighted(accumulated_diff, 0.7, th, 0.3, 0)  # Ajustar el suavizado temporal
            
            cnts, _ = cv2.findContours(accumulated_diff, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            motion_detected = False
            for c in cnts:
                area = cv2.contourArea(c)
                if area > 700:  #  área mínima para detectar movimientos más pequeños
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    motion_detected = True

            if motion_detected:
                if not config.luces:
                    config.luces = True
                    config.save()#encender luces
                    registro = Registro(
                        dispositivo=dispositivo_luces,
                        accion= True,
                        tipodeact='automatica'
                    )
                    registro.save()
                    print("Luces encendidas automáticamente debido a detección de movimiento.")
                last_motion_time = time.time()  # Actualizar el tiempo de la última detección de movimiento
            else:
                
                # Apagar las luces después del tiempo configurado sin movimiento 
                if config.luces and (time.time() - last_motion_time) > no_motion_time_limit:
                    config.luces = False
                    config.save()
                    registro = Registro(
                        dispositivo=dispositivo_luces,
                        accion= False,
                        tipodeact='automatica'
                    )
                    registro.save()
                    print("Luces apagadas debido a la falta de movimiento.")

        cv2.imshow('Frame', frame)
        
        i += 1
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()
