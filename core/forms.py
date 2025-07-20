
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

        # Mostrar todos los equipos por defecto
        self.fields['equipo_b'].queryset = Equipo.objects.all()

        # Filtrar equipo_b si equipo_a ya está seleccionado
        if 'equipo_a' in self.data:
            equipo_a_id = self.data.get('equipo_a')
            if equipo_a_id:
                self.fields['equipo_b'].queryset = Equipo.objects.exclude(id=equipo_a_id)
        elif self.instance.pk and self.instance.equipo_a_id:
            self.fields['equipo_b'].queryset = Equipo.objects.exclude(id=self.instance.equipo_a_id)

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