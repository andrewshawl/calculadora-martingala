import streamlit as st
import math

def calcular_martingala(riesgo_maximo, probabilidad_exito, dinero_inicial):
    if not (0 < riesgo_maximo < 1):
        st.error("El nivel de riesgo debe estar entre 0 y 1 (por ejemplo, 1% = 0.01).")
        return
    if not (0 < probabilidad_exito <= 1):
        st.error("La probabilidad de ganar debe estar entre 0 y 1 (por ejemplo, 55% = 0.55).")
        return
    if dinero_inicial <= 0:
        st.error("El dinero inicial debe ser mayor que 0.")
        return

    # Número máximo de rondas para mantener la probabilidad acumulada bajo el riesgo máximo
    num_rondas = math.floor(math.log(riesgo_maximo) / math.log(1 - probabilidad_exito))

    # Calcular cuánto apostar en cada ronda para usar el presupuesto disponible
    total_apuesta = 0
    apuesta_base = dinero_inicial / (2 ** num_rondas - 1)  # Base para distribuir las apuestas
    apuestas = []

    for ronda in range(num_rondas):
        apuesta = apuesta_base * (2 ** ronda)
        total_apuesta += apuesta
        apuestas.append(apuesta)

    st.write("### Resultados:")
    st.write(f"Número máximo de rondas: {num_rondas}")
    st.write(f"Dinero total necesario: {total_apuesta:.2f} (de {dinero_inicial:.2f} inicial)")
    st.write("### Detalle de apuestas por ronda:")
    for i, apuesta in enumerate(apuestas, start=1):
        st.write(f"Ronda {i}: Apostar {apuesta:.2f}")

# Interfaz con Streamlit
st.title("Calculadora de Martingala")

riesgo_maximo = st.number_input("Nivel de riesgo máximo (%)", min_value=0.01, max_value=100.0, value=1.0, step=0.01) / 100
probabilidad_exito = st.number_input("Probabilidad de ganar (%)", min_value=0.01, max_value=100.0, value=55.0, step=0.01) / 100
dinero_inicial = st.number_input("Dinero inicial", min_value=1.0, value=1000.0, step=1.0)

if st.button("Calcular"):
    calcular_martingala(riesgo_maximo, probabilidad_exito, dinero_inicial)


