import streamlit as st
import pandas as pd

def calcular_break_even(cantidad_inicial, precio_inicial, factor_martingala, espacios_precio, niveles):
    tamanio_lote = 100  # Tamaño fijo del lote
    cantidad_total = cantidad_inicial * tamanio_lote
    costo_total = cantidad_inicial * tamanio_lote * precio_inicial

    precio_actual = precio_inicial
    cantidad_actual = cantidad_inicial * tamanio_lote

    transacciones = []

    # Agregar los datos iniciales (Nivel 0)
    transacciones.append({
        "Nivel": 0,
        "Precio": precio_actual,
        "Cantidad a comprar (lotes)": cantidad_inicial,
        "Costo acumulado": costo_total,
        "Cantidad acumulada (lotes)": cantidad_total / tamanio_lote
    })

    for nivel in range(1, niveles + 1):
        precio_actual += espacios_precio[nivel - 1]
        cantidad_a_comprar = cantidad_actual / tamanio_lote * factor_martingala
        cantidad_actual = cantidad_a_comprar * tamanio_lote
        costo_total += cantidad_actual * precio_actual
        cantidad_total += cantidad_actual

        transacciones.append({
            "Nivel": nivel,
            "Precio": precio_actual,
            "Cantidad a comprar (lotes)": cantidad_a_comprar,
            "Costo acumulado": costo_total,
            "Cantidad acumulada (lotes)": cantidad_total / tamanio_lote
        })

    break_even = costo_total / cantidad_total
    return break_even, transacciones


# Interfaz de Streamlit
st.title("Calculadora de Break Even para Martingala")

# Entradas del usuario
cantidad_inicial = st.number_input("Cantidad inicial de lotes comprados:", min_value=0.01, value=1.0, step=0.01)
precio_inicial = st.number_input("Precio inicial del oro:", min_value=0.01, value=2000.0, step=0.01)
factor_martingala = st.number_input("Factor de martingala:", min_value=1.0, value=2.0, step=0.1)
niveles = st.number_input("Número de niveles:", min_value=1, value=3, step=1)

# Selección de espacios de precio
opcion_espacio = st.selectbox("Seleccione el tipo de espacio:", ["Fijo", "Variable", "Arbitrario"])

espacios_precio = []

if opcion_espacio == "Fijo":
    espacio_precio = st.number_input("Espacio fijo entre precios (número negativo para caídas):", value=-10.0, step=0.1)
    espacios_precio = [espacio_precio] * niveles
elif opcion_espacio == "Variable":
    base_espacio = st.number_input("Base del espacio entre precios:", value=10.0, step=0.1)
    multiplicador = st.number_input("Multiplicador para el espacio entre precios:", value=1.5, step=0.1)
    espacios_precio = [base_espacio * (multiplicador ** i) for i in range(niveles)]
elif opcion_espacio == "Arbitrario":
    espacios_input = st.text_input("Espacios entre precios separados por comas (e.g., 10,-5,15):")
    try:
        espacios_precio = list(map(float, espacios_input.split(',')))
        if len(espacios_precio) != niveles:
            st.error("El número de espacios debe coincidir con el número de niveles.")
    except ValueError:
        st.error("Por favor, ingrese valores numéricos separados por comas.")

# Calcular y mostrar resultados
if espacios_precio and st.button("Calcular Break Even"):
    break_even, transacciones = calcular_break_even(cantidad_inicial, precio_inicial, factor_martingala, espacios_precio, niveles)

    st.write(f"### El precio de break even es: {break_even:.2f}")

    # Mostrar la tabla con los resultados
    df_transacciones = pd.DataFrame(transacciones)
    st.write("### Detalles de las transacciones:")
    st.dataframe(df_transacciones)
