# ⚽ Metsi Manager

Metsi Manager es un **juego de manager de fútbol online y multijugador**, inspirado en clásicos como Hattrick, pero con una arquitectura moderna, motores separados y una progresión más controlada y realista.

El juego está pensado para ejecutarse **100% online**, con usuarios reales, ligas compartidas y persistencia total de datos en servidor.

---

## 🎯 Concepto General

Cada usuario crea una cuenta, recibe un equipo de fútbol y compite en una **liga madre única** contra otros usuarios reales.

El jugador asume el rol de **manager**, tomando decisiones sobre:
- Alineaciones
- Entrenamientos
- Economía
- Desarrollo de jugadores
- Estrategia de temporada

Los partidos se simulan mediante motores lógicos basados en atributos reales de los jugadores.

---

## 🌍 Multiplayer Online (desde la versión 1)

- Usuarios reales
- Un equipo por usuario
- Liga compartida
- Partidos sincronizados
- Datos persistentes en base de datos
- Autenticación mediante login y tokens

No hay simulación offline ni IA controlando equipos de liga.

---

## 🏆 Sistema de Liga

- **Liga madre única**
- **8 equipos**
- Formato ida y vuelta
- **14 partidos de liga**
- **16 semanas por temporada**
  - 14 semanas de liga
  - 2 semanas libres
- En semanas libres:
  - 1 amistoso automático por semana

Una temporada equivale a **1 año en el juego**.

---

## 👥 Equipos y Jugadores

### Plantilla inicial
- 16 jugadores:
  - 2 arqueros
  - 5 defensas
  - 5 mediocampistas
  - 4 delanteros

### Edades
- Los jugadores pueden jugar hasta los **32 años**
- Mientras más joven el jugador:
  - Más rápido entrena
- Cada año:
  - La velocidad de entrenamiento disminuye

---

## 📊 Habilidades de los Jugadores

Sistema de habilidades estilo Hattrick (1–20):

- Portería
- Defensa
- Jugadas
- Pases
- Lateral
- Anotación
- Balón parado
- Forma
- Condición

No existen:
- Habilidades especiales
- Rarezas
- Niveles de equipo (25–100 eliminados)

---

## 🧠 Motores del Juego

El juego está dividido en **motores independientes**, lo que permite escalar y modificar sin romper el sistema.

### ⚙️ Team Creation Engine
- Crea el equipo inicial
- Genera jugadores con nombres realistas
- Distribuye habilidades según posición
- Asigna estadio, dinero y entrenador

---

### ⚽ Match Engine
- Simulación de partidos de **90 minutos**
- Descanso de **15 minutos**
- Ocasiones distribuidas durante el partido
- Comparación lógica:
  - Mediocampo vs Mediocampo → control del juego
  - Ataque vs Defensa → generación de ocasiones
  - Delantero vs Portero → definición de gol
- Incluye:
  - Goles en jugada
  - Goles de balón parado
  - Eventos especiales

---

### 🏋️ Training Engine
- El usuario elige **una habilidad a entrenar**
- Solo entrenan los jugadores de la posición correspondiente:
  - Jugadas → mediocampistas
  - Defensa → defensores
  - Anotación → delanteros
  - Portería → arqueros
- Habilidades secundarias entrenan todos
- Entrenador:
  - Nivel máximo: 5
  - Cada 5 partidos:
    - +1 nivel efectivo de entrenamiento
- El progreso es lento y realista:
  - Jóvenes no se vuelven leyendas en 2 temporadas

---

### 💰 Economy Engine
- Ingresos por partidos de local:
  - Asistencia
  - Precio de entradas
- Bonos por resultado:
  - Victoria
  - Empate
- Costos:
  - Mantenimiento del estadio
- Sistema básico pero estable para v1

---

### 🏆 League Engine
- Generación automática del calendario
- Gestión de semanas
- Control de temporadas
- Manejo de amistosos en semanas libres

---

## 🗄️ Arquitectura del Proyecto

```text
backend/
│
├── app/
│   ├── engines/              # Lógica del juego
│   ├── models/               # Base de datos
│   ├── routes/               # API REST
│   └── main.py               # Backend principal
│
└── requirements.txt
