
CREATE PROCEDURE ObtenerEstadisticasJuego
    @IdJuego nchar(10)
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @Fecha date, @EquipoA nchar(3), @EquipoB nchar(3);
    DECLARE @NombreEquipoA nvarchar(100), @NombreEquipoB nvarchar(100);
    DECLARE @TotalA int = 0, @TotalB int = 0;

    -- Obtener datos del juego
    SELECT @Fecha = Fecha, @EquipoA = EquipoA, @EquipoB = EquipoB
    FROM Juego WHERE IdJuego = @IdJuego;

    SELECT @NombreEquipoA = Nombre FROM Equipo WHERE IdEquipo = @EquipoA;
    SELECT @NombreEquipoB = Nombre FROM Equipo WHERE IdEquipo = @EquipoB;

    -- Tabla para cálculos
    CREATE TABLE #EstadisticasJugador (
        IdJugador nchar(10),
        Nombre nvarchar(30),
        Numero nchar(10),
        IdEquipo nchar(3),
        Puntos int DEFAULT 0,
        Asistencias int DEFAULT 0,
        Rebotes int DEFAULT 0,
        Robadas int DEFAULT 0,
        Faltas int DEFAULT 0,
        Tecnicas int DEFAULT 0,
        Perdidas int DEFAULT 0
    );

    INSERT INTO #EstadisticasJugador (IdJugador, Nombre, Numero, IdEquipo)
    SELECT J.IdJugador, J.Nombre, J.Numero, J.IdEquipo
    FROM Jugador J
    INNER JOIN EstadisticaJuego EJ ON EJ.IdJugador = J.IdJugador
    WHERE EJ.IdJuego = @IdJuego
    GROUP BY J.IdJugador, J.Nombre, J.Numero, J.IdEquipo;

    -- Cargar estadísticas
    DECLARE @IdEstadistica nchar(10), @Valor int, @Jugador nchar(10);
    DECLARE cursor_estad CURSOR FOR
        SELECT IdEstadistica, Cantidad, IdJugador
        FROM EstadisticaJuego
        WHERE IdJuego = @IdJuego;

    OPEN cursor_estad;
    FETCH NEXT FROM cursor_estad INTO @IdEstadistica, @Valor, @Jugador;
    WHILE @@FETCH_STATUS = 0
    BEGIN
        IF @IdEstadistica IN ('01', '02', '09')
        BEGIN
            UPDATE #EstadisticasJugador
            SET Puntos = Puntos + @Valor * 
                CASE 
                    WHEN @IdEstadistica = '01' THEN 2
                    WHEN @IdEstadistica = '02' THEN 3
                    WHEN @IdEstadistica = '09' THEN 1
                END
            WHERE IdJugador = @Jugador;
        END
        ELSE IF @IdEstadistica = '03'
            UPDATE #EstadisticasJugador SET Asistencias = @Valor WHERE IdJugador = @Jugador;
        ELSE IF @IdEstadistica = '04'
            UPDATE #EstadisticasJugador SET Rebotes = @Valor WHERE IdJugador = @Jugador;
        ELSE IF @IdEstadistica = '05'
            UPDATE #EstadisticasJugador SET Robadas = @Valor WHERE IdJugador = @Jugador;
        ELSE IF @IdEstadistica = '06'
            UPDATE #EstadisticasJugador SET Faltas = @Valor WHERE IdJugador = @Jugador;
        ELSE IF @IdEstadistica = '07'
            UPDATE #EstadisticasJugador SET Tecnicas = @Valor WHERE IdJugador = @Jugador;
        ELSE IF @IdEstadistica = '08'
            UPDATE #EstadisticasJugador SET Perdidas = @Valor WHERE IdJugador = @Jugador;

        FETCH NEXT FROM cursor_estad INTO @IdEstadistica, @Valor, @Jugador;
    END
    CLOSE cursor_estad;
    DEALLOCATE cursor_estad;

    -- Calcular puntaje total por equipo
    SELECT @TotalA = SUM(Puntos) FROM #EstadisticasJugador WHERE IdEquipo = @EquipoA;
    SELECT @TotalB = SUM(Puntos) FROM #EstadisticasJugador WHERE IdEquipo = @EquipoB;

    IF @TotalA > @TotalB
        SET @NombreEquipoA = @NombreEquipoA + ' (Ganador)';
    ELSE IF @TotalB > @TotalA
        SET @NombreEquipoB = @NombreEquipoB + ' (Ganador)';

    -- Crear tabla única de salida
    CREATE TABLE #ResultadoFinal (
        Seccion nvarchar(100),
        Jugador nvarchar(50),
        Puntos int,
        Asistencias int,
        Rebotes int,
        [Bolas_Robadas] int,
        Faltas int,
        Técnicas int,
        [Bolas_Perdidas] int
    );

    -- Agregar encabezados
    INSERT INTO #ResultadoFinal (Seccion, Jugador)
    VALUES 
        ('ESTADÍSTICAS DEL JUEGO', ''),
        ('JUEGO: ' + @IdJuego + '     FECHA: ' + CONVERT(varchar(10), @Fecha, 105), ''),
        ('Equipo Local: ' + @NombreEquipoA, '');

    -- Equipo local
    INSERT INTO #ResultadoFinal
    SELECT 
        '',
        RIGHT('00' + CONVERT(varchar, CAST(Numero AS int)), 2) + ' – ' + Nombre,
        Puntos, Asistencias, Rebotes, Robadas, Faltas, Tecnicas, Perdidas
    FROM #EstadisticasJugador
    WHERE IdEquipo = @EquipoA;

    INSERT INTO #ResultadoFinal
    SELECT 
        '', 'Total:',
        SUM(Puntos), SUM(Asistencias), SUM(Rebotes), SUM(Robadas),
        SUM(Faltas), SUM(Tecnicas), SUM(Perdidas)
    FROM #EstadisticasJugador
    WHERE IdEquipo = @EquipoA;

    -- Encabezado visitante
    INSERT INTO #ResultadoFinal (Seccion, Jugador)
    VALUES ('Equipo Visitante: ' + @NombreEquipoB, '');

    -- Equipo visitante
    INSERT INTO #ResultadoFinal
    SELECT 
        '',
        RIGHT('00' + CONVERT(varchar, CAST(Numero AS int)), 2) + ' – ' + Nombre,
        Puntos, Asistencias, Rebotes, Robadas, Faltas, Tecnicas, Perdidas
    FROM #EstadisticasJugador
    WHERE IdEquipo = @EquipoB;

    INSERT INTO #ResultadoFinal
    SELECT 
        '', 'Total:',
        SUM(Puntos), SUM(Asistencias), SUM(Rebotes), SUM(Robadas),
        SUM(Faltas), SUM(Tecnicas), SUM(Perdidas)
    FROM #EstadisticasJugador
    WHERE IdEquipo = @EquipoB;

    -- Resultado final: todo en una tabla
    SELECT 
    ISNULL(Seccion, '') AS Seccion,
    ISNULL(Jugador, '') AS Jugador,
    ISNULL(CONVERT(varchar, Puntos), '') AS Puntos,
    ISNULL(CONVERT(varchar, Asistencias), '') AS Asistencias,
    ISNULL(CONVERT(varchar, Rebotes), '') AS Rebotes,
    ISNULL(CONVERT(varchar, [Bolas_Robadas]), '') AS [Bolas_Robadas],
    ISNULL(CONVERT(varchar, Faltas), '') AS Faltas,
    ISNULL(CONVERT(varchar, Técnicas), '') AS Técnicas,
    ISNULL(CONVERT(varchar, [Bolas_Perdidas]), '') AS [Bolas_Perdidas]
	FROM #ResultadoFinal;

    DROP TABLE #EstadisticasJugador;
    DROP TABLE #ResultadoFinal;
END;

EXEC ObtenerEstadisticasJuego @IdJuego = N'ACFA52A628'

DROP PROCEDURE ObtenerEstadisticasJuego

