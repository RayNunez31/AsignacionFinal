from django.urls import path
from .views import (
    CiudadListView, CiudadCreateView, CiudadUpdateView, CiudadDeleteView,
    EquipoListView, EquipoCreateView, EquipoUpdateView, EquipoDeleteView,
    JugadorListView, JugadorCreateView, JugadorUpdateView, JugadorDeleteView,
    JuegoListView, JuegoCreateView,JuegoDashboardView, JuegoUpdateView, JuegoDeleteView,
    EstadisticaListView, EstadisticaCreateView, EstadisticaUpdateView, EstadisticaDeleteView,
    EstadisticajuegoListView, EstadisticajuegoCreateView, EstadisticajuegoUpdateView, EstadisticajuegoDeleteView,
)

urlpatterns = [


    path('ciudades/', CiudadListView.as_view(), name='ciudad-list'),
    path('ciudades/crear/', CiudadCreateView.as_view(), name='ciudad-create'),
    path('ciudades/<str:pk>/editar/', CiudadUpdateView.as_view(), name='ciudad-edit'),
    path('ciudades/<pk>/eliminar/', CiudadDeleteView.as_view(), name='ciudad-delete'),
    # Equipo
path('equipos/', EquipoListView.as_view(), name='equipo-list'),
path('equipos/crear/', EquipoCreateView.as_view(), name='equipo-create'),
path('equipos/<pk>/editar/', EquipoUpdateView.as_view(), name='equipo-edit'),
path('equipos/<pk>/eliminar/', EquipoDeleteView.as_view(), name='equipo-delete'),

# Jugador
path('jugadores/', JugadorListView.as_view(), name='jugador-list'),
path('jugadores/crear/', JugadorCreateView.as_view(), name='jugador-create'),
path('jugadores/<pk>/editar/', JugadorUpdateView.as_view(), name='jugador-edit'),
path('jugadores/<pk>/eliminar/', JugadorDeleteView.as_view(), name='jugador-delete'),

# Juego
path('juegos/', JuegoListView.as_view(), name='juego-list'),
path('juegos/crear/', JuegoCreateView.as_view(), name='juego-create'),
path('juegos/<pk>/editar/', JuegoUpdateView.as_view(), name='juego-edit'),
path('juegos/<pk>/eliminar/', JuegoDeleteView.as_view(), name='juego-delete'),

path('juegos/<str:pk>/dashboard/', JuegoDashboardView.as_view(), name='juego-dashboard'),


# Estadistica
path('estadisticas/', EstadisticaListView.as_view(), name='estadistica-list'),
path('estadisticas/crear/', EstadisticaCreateView.as_view(), name='estadistica-create'),
path('estadisticas/<pk>/editar/', EstadisticaUpdateView.as_view(), name='estadistica-edit'),
path('estadisticas/<pk>/eliminar/', EstadisticaDeleteView.as_view(), name='estadistica-delete'),

# EstadisticaJuego
path('estadisticas-juego/', EstadisticajuegoListView.as_view(), name='estadisticajuego-list'),
path('estadisticas-juego/crear/', EstadisticajuegoCreateView.as_view(), name='estadisticajuego-create'),
path('estadisticas-juego/<pk>/editar/', EstadisticajuegoUpdateView.as_view(), name='estadisticajuego-edit'),
path('estadisticas-juego/<pk>/eliminar/', EstadisticajuegoDeleteView.as_view(), name='estadisticajuego-delete'),

]