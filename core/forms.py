
from django import forms
from .models import Jugador, Ciudad, Juego, Equipo, Estadistica, EstadisticaJuego

class EstadisticaJuegoInlineForm(forms.ModelForm):
    """Formulario compacto para registrar una estadística dentro del dashboard."""
    class Meta:
        model = EstadisticaJuego
        fields = ["jugador", "estadistica", "cantidad"]

        widgets = {
            "cantidad": forms.NumberInput(
                attrs={"min": 0, "class": "input input-bordered w-full"}
            ),
            "estadistica": forms.Select(
                attrs={"class": "select select-bordered w-full"}
            ),
            "jugador": forms.Select(
                attrs={"class": "select select-bordered w-full"}
            ),
        }

    def __init__(self, *args, juego=None, **kwargs):
        super().__init__(*args, **kwargs)
        if juego:
            equipos = [juego.equipo_a, juego.equipo_b]
            self.fields["jugador"].queryset = Jugador.objects.filter(equipo__in=equipos)


class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['descripcion', 'equipo_a', 'equipo_b', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ── Filtrado dinámico ────────────────────────────────────────────────
        # 1) mostrar todos los equipos por defecto
        self.fields['equipo_b'].queryset = Equipo.objects.all()

        # 2) si viene equipo_a (en POST o en GET con ?equipo_a=...)
        equipo_a_id = self.data.get('equipo_a') or getattr(self.instance, 'equipo_a_id', None)
        if equipo_a_id:
            self.fields['equipo_b'].queryset = Equipo.objects.exclude(id=equipo_a_id)

    # ── Validación para que no se repita el mismo equipo ───────────────────
    def clean(self):
        cleaned_data = super().clean()
        equipo_a = cleaned_data.get('equipo_a')
        equipo_b = cleaned_data.get('equipo_b')

        if equipo_a and equipo_b and equipo_a == equipo_b:
            # Asignamos el error al campo equipo_b para que sea más claro
            self.add_error('equipo_b', 'Equipo B no puede ser el mismo que Equipo A.')

        return cleaned_data
    
class JugadorForm(forms.ModelForm):
    class Meta:
        model  = Jugador
        fields = ['nombre', 'ciudad_nacim', 'fecha_nacim', 'numero', 'equipo']

        widgets = {
            'ciudad_nacim': forms.Select(
                attrs={'class': 'select select-bordered w-full'}
            ),
            'fecha_nacim': forms.DateInput(
                attrs={'type': 'date', 'class': 'input input-bordered w-full'}
            ),
            'nombre': forms.TextInput(
                attrs={'class': 'input input-bordered w-full'}
            ),
            'numero': forms.TextInput(
                attrs={'class': 'input input-bordered w-full'}
            ),
            'equipo': forms.Select(
                attrs={'class': 'select select-bordered w-full'}
            ),
        }
        labels = {
            'ciudad_nacim': 'Ciudad de nacimiento',
            'fecha_nacim': 'Fecha de nacimiento',
        }