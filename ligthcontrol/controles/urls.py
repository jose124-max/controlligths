from django.urls import path, include,re_path
from rest_framework.routers import DefaultRouter
from .views import *
# Crear el router
router = DefaultRouter()
router.register(r'tipos', TipoViewSet)
router.register(r'dispositivos', DispositivoViewSet)
router.register(r'registros', RegistroViewSet)
router.register(r'configuraciones', ConfiguracionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('onofflights/', OnOffLightsView.as_view(), name='onofflights'),
    path('lights-status/', LightsStatusView.as_view(), name='lights_status'),
    path('temp-status/', tempsStatusView.as_view(), name='temps_status'),
    path('temp-statuspost/<str:temperatura>/', tempsStatusPost.as_view(), name='temps_statuspost'),
    path('codOn/', getCodOn.as_view(), name='codon'),
    path('codON/<str:codon>/', postCodOn.as_view(), name='postCodOn'),
    path('codOff/', getCodOff.as_view(), name='codoff'),
    path('codOff/<str:codoff>/', postCodOff.as_view(), name='postCodOff'),
    path('getsolon/', getSolOn.as_view(), name='getSolOn'),
    path('solcodon/', postSolOn.as_view(), name='postSolOn'),
    path('getsoloff/', getSolOff.as_view(), name='getSolOff'),
    path('solcodoff/', postSolOff.as_view(), name='postSolOff'),
]
