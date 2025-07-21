from datetime import timezone
import json
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import Ciudad, Equipo, Jugador, Juego, Estadistica, EstadisticaJuego
from .forms import JugadorForm, JuegoForm, EstadisticaJuegoInlineForm  
from django.db import connection
from django.shortcuts import render
from collections import defaultdict
from django.db.models import Sum
from datetime import datetime
from django.utils.dateformat import DateFormat
from django.utils.timezone import now

class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Métricas generales
        context['total_jugadores'] = Jugador.objects.count()
        context['equipos_activos'] = Equipo.objects.count()
        context['juegos_este_mes'] = Juego.objects.filter(fecha__month=now().month).count()

        # MVP: jugador con más puntos (usando descripcion)
        puntos = EstadisticaJuego.objects.filter(
            estadistica__descripcion__in=[
                'Puntos de dos            ',
                'Puntos de tres           ',
                'Tiros libres             '
            ]
        )

        mvp = puntos.values('jugador__nombre') \
            .annotate(total=Sum('cantidad')) \
            .order_by('-total') \
            .first()

        context['mvp'] = mvp['jugador__nombre'] if mvp else 'N/A'

        # Próximos juegos
        context['juegos'] = Juego.objects.filter(fecha__gte=now()).order_by('fecha')[:5]

        # Posesión por equipo (solo mostrando totales)
        estadisticas_posesion = EstadisticaJuego.objects.filter(estadistica__descripcion='Posesión')
        posesion = estadisticas_posesion.values('jugador__equipo__nombre').annotate(total=Sum('cantidad')).order_by('-total')
        context['posesion_equipos'] = posesion

        return context
    
def estadisticas_juego(request, id_juego):
    with connection.cursor() as cursor:
        cursor.execute("EXEC ObtenerEstadisticasJuego %s", [id_juego])
        columns = [col[0] for col in cursor.description]
        resultados = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render(request, 'core/estadistica.html', {'resultados': resultados})

class JuegoDashboardView(TemplateView):
    template_name = 'core/juego_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        juego = get_object_or_404(Juego, pk=kwargs['pk'])

        estadisticas = EstadisticaJuego.objects.filter(juego=juego).select_related('jugador', 'estadistica')

        tipos_estadistica = Estadistica.objects.all()
        jugadores = Jugador.objects.filter(equipo__in=[juego.equipo_a, juego.equipo_b])

        def agrupar_estadisticas(jugadores_equipo):
            resultado = []
            for jugador in jugadores_equipo:
                fila = {
                    'jugador': jugador,
                    'estadisticas': []
                }
                for tipo in tipos_estadistica:
                    total = sum(e.cantidad for e in estadisticas if e.jugador == jugador and e.estadistica == tipo)
                    fila['estadisticas'].append({'tipo': tipo.descripcion, 'cantidad': total})
                resultado.append(fila)
            return resultado

        context.update({
            'juego': juego,
            'form': EstadisticaJuegoInlineForm(juego=juego),
            'tipos_estadistica': tipos_estadistica,
            'equipo_a_nombre': juego.equipo_a.nombre,
            'equipo_b_nombre': juego.equipo_b.nombre,
            'equipo_a_estadisticas': agrupar_estadisticas(jugadores.filter(equipo=juego.equipo_a)),
            'equipo_b_estadisticas': agrupar_estadisticas(jugadores.filter(equipo=juego.equipo_b)),
        })
        return context

    def post(self, request, *args, **kwargs):
        juego = get_object_or_404(Juego, pk=kwargs['pk'])
        form = EstadisticaJuegoInlineForm(request.POST, juego=juego)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.juego = juego
            instancia.save()
            return redirect('juego-dashboard', pk=juego.pk)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
    
# ---- CIUDAD ----
class CiudadListView(ListView):
    model = Ciudad
    template_name = 'core/ciudad_list.html'

class CiudadCreateView(CreateView):
    model = Ciudad
    fields = ['nombre']
    template_name = 'core/ciudad_form.html'
    success_url = reverse_lazy('ciudad-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Crear Ciudad"
        return context

class CiudadUpdateView(UpdateView):
    model = Ciudad
    fields = ['nombre']  # ID removido
    template_name = 'core/ciudad_form.html'
    success_url = reverse_lazy('ciudad-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Editar Ciudad"
        return context

class CiudadDeleteView(DeleteView):
    model = Ciudad
    template_name = 'core/ciudad_confirm_delete.html'
    success_url = reverse_lazy('ciudad-list')


# ---- EQUIPO ----
class EquipoListView(ListView):
    model = Equipo
    template_name = 'core/equipo_list.html'

class EquipoCreateView(CreateView):
    model = Equipo
    fields = ['nombre', 'ciudad']  # ID removido
    template_name = 'core/form.html'
    success_url = reverse_lazy('equipo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Crear Equipo"
        return context

class EquipoUpdateView(UpdateView):
    model = Equipo
    fields = ['nombre', 'ciudad']  # ID removido
    template_name = 'core/form.html'
    success_url = reverse_lazy('equipo-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Editar Equipo"
        return context

class EquipoDeleteView(DeleteView):
    model = Equipo
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('equipo-list')


# ---- JUGADOR ----
class JugadorListView(ListView):
    model = Jugador
    template_name = 'core/jugador_list.html'

class JugadorCreateView(CreateView):
    model = Jugador
    form_class = JugadorForm            # <—
    template_name = 'core/form.html'
    success_url = reverse_lazy('jugador-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo_formulario'] = "Crear Jugador"
        return ctx

class JugadorUpdateView(UpdateView):
    model = Jugador
    form_class = JugadorForm         
    template_name = 'core/form.html'
    success_url = reverse_lazy('jugador-list')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo_formulario'] = "Editar Jugador"
        return ctx

class JugadorDeleteView(DeleteView):
    model = Jugador
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('jugador-list')


# ---- JUEGO ----
class JuegoListView(ListView):
    model = Juego
    template_name = 'core/juego_list.html'

class JuegoCreateView(CreateView):
    model = Juego
    form_class = JuegoForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('juego-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Crear Juego"
        return context

class JuegoUpdateView(UpdateView):
    model = Juego
    form_class = JuegoForm
    template_name = 'core/form.html'
    success_url = reverse_lazy('juego-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Editar Juego"
        return context

class JuegoDeleteView(DeleteView):
    model = Juego
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('juego-list')


# ---- ESTADISTICA ----
class EstadisticaListView(ListView):
    model = Estadistica
    template_name = 'core/estadistica_list.html'

class EstadisticaCreateView(CreateView):
    model = Estadistica
    fields = ['descripcion', 'valor']  # ID removido
    template_name = 'core/form.html'
    success_url = reverse_lazy('estadistica-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Crear Estadística"
        return context

class EstadisticaUpdateView(UpdateView):
    model = Estadistica
    fields = ['descripcion', 'valor']  # ID removido
    template_name = 'core/form.html'
    success_url = reverse_lazy('estadistica-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Editar Estadística"
        return context

class EstadisticaDeleteView(DeleteView):
    model = Estadistica
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('estadistica-list')


# ---- ESTADISTICA JUEGO ----
class EstadisticajuegoListView(ListView):
    model = EstadisticaJuego
    template_name = 'core/estadisticajuego_list.html'

class EstadisticajuegoCreateView(CreateView):
    model = EstadisticaJuego
    fields = ['juego', 'estadistica', 'jugador', 'cantidad']  # ID removido
    template_name = 'core/form.html'
    success_url = reverse_lazy('estadisticajuego-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Crear Estadística de Juego"
        return context

class EstadisticajuegoUpdateView(UpdateView):
    model = EstadisticaJuego
    fields = ['juego', 'estadistica', 'jugador', 'cantidad']  # ID removido
    template_name = 'core/form.html'
    success_url = reverse_lazy('estadisticajuego-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_formulario'] = "Editar Estadística de Juego"
        return context

class EstadisticajuegoDeleteView(DeleteView):
    model = EstadisticaJuego
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('estadisticajuego-list')
