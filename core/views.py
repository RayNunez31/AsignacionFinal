from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from .models import Ciudad, Equipo, Jugador, Juego, Estadistica, EstadisticaJuego
from .forms import JugadorForm, JuegoForm, EstadisticaJuegoInlineForm  


class JuegoDashboardView(TemplateView):
    template_name = 'core/juego_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        juego = get_object_or_404(Juego, pk=kwargs['pk'])

        jugadores = Jugador.objects.filter(equipo__in=[juego.equipo_a, juego.equipo_b])
        estadisticas = EstadisticaJuego.objects.filter(juego=juego)

        context.update({
            'juego': juego,
            'jugadores': jugadores,
            'estadisticas': estadisticas,
            'form': EstadisticaJuegoInlineForm(juego=juego),
        })
        return context

    def post(self, request, *args, **kwargs):
        juego = get_object_or_404(Juego, pk=kwargs['pk'])
        form = EstadisticaJuegoInlineForm(request.POST, juego=juego)

        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.juego = juego
            nueva.save()
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
    form_class = JugadorForm            # <—
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
