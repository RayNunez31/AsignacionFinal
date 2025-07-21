from django.db import models
import uuid

def generate_id(length=8):
    return uuid.uuid4().hex[:length].upper()  # Ej: '3F2504E0'

class Ciudad(models.Model):
    id = models.CharField(max_length=8, primary_key=True, db_column='IdCiudad')
    nombre = models.CharField(max_length=25, db_column='Nombre')

    class Meta:
        db_table = 'Ciudad'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(8)
        super().save(*args, **kwargs)


class Equipo(models.Model):
    id = models.CharField(max_length=8, primary_key=True, db_column='IdEquipo')
    nombre = models.CharField(max_length=25, db_column='Nombre')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, db_column='IdCiudad')

    class Meta:
        db_table = 'Equipo'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(8)
        super().save(*args, **kwargs)


class Jugador(models.Model):
    id = models.CharField(max_length=10, primary_key=True, db_column='IdJugador')
    nombre = models.CharField(max_length=30, db_column='Nombre')
    ciudad_nacim = models.ForeignKey(
        Ciudad, on_delete=models.SET_NULL, null=True,
        db_column='CiudadNacim', related_name='jugadores_nacidos'
    )
    fecha_nacim = models.DateField(db_column='FechaNacim')
    numero = models.CharField(max_length=10, db_column='Numero')
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, db_column='IdEquipo')

    class Meta:
        db_table = 'Jugador'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(10)
        super().save(*args, **kwargs)


class Juego(models.Model):
    id = models.CharField(max_length=10, primary_key=True, db_column='IdJuego')
    descripcion = models.CharField(max_length=50, db_column='Descripcion')
    equipo_a = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='EquipoA', related_name='juegos_como_equipo_a')
    equipo_b = models.ForeignKey(Equipo, on_delete=models.CASCADE, db_column='EquipoB', related_name='juegos_como_equipo_b')
    fecha = models.DateField(db_column='Fecha')

    class Meta:
        db_table = 'Juego'

    def __str__(self):
        return f"{self.descripcion} - {self.fecha}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(10)
        super().save(*args, **kwargs)


class Estadistica(models.Model):
    id = models.CharField(max_length=10, primary_key=True, db_column='IdEstadistica')
    descripcion = models.CharField(max_length=25, db_column='Descripcion')
    valor = models.IntegerField(db_column='Valor')

    class Meta:
        db_table = 'Estadistica'

    def __str__(self):
        return self.descripcion

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(10)
        super().save(*args, **kwargs)


class EstadisticaJuego(models.Model):
    id = models.CharField(max_length=10, primary_key=True, db_column='IdEstadisticaJuego')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, db_column='IdJuego')
    estadistica = models.ForeignKey(Estadistica, on_delete=models.CASCADE, db_column='IdEstadistica')
    jugador = models.ForeignKey(Jugador, on_delete=models.CASCADE, db_column='IdJugador')
    cantidad = models.IntegerField(null=True, blank=True, db_column='Cantidad')

    class Meta:
        db_table = 'EstadisticaJuego'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(10)
        super().save(*args, **kwargs)
