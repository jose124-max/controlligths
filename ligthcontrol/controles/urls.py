from django.urls import path, include,re_path
from rest_framework.routers import DefaultRouter
from .views import TipoViewSet, DispositivoViewSet, RegistroViewSet, ConfiguracionViewSet,OnOffLightsView,LightsStatusView,tempsStatusView,tempsStatusPost

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
]
