import streamlit as st
import pandas as pd
import pyodbc

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Extractor de Datos Coninsa", page_icon="📊")
st.title("📥 Descarga de datos - Azure SQL")

# --- CREDENCIALES (Usa las de tu imagen) ---
server = 'replica-sql.database.windows.net,1433'
database = 'replica_btk_coninsa'
username = 'coninsalectura'
password = 'obw9DcMoyP7T5i' 
driver = '{ODBC Driver 18 for SQL Server}'

# --- FUNCIÓN PARA CONECTAR Y EXTRAER ---
def obtener_datos(query):
    try:
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        # Usamos pandas para leer directamente con la conexión
        with pyodbc.connect(conn_str) as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return None

# --- INTERFAZ DE USUARIO ---
nombre_tabla = st.text_input("Escribe el nombre de la tabla:", value="FNX_GTH.Empleados")

if st.button("Consultar Información"):
    with st.spinner("Consultando base de datos..."):
        query = f"SELECT * FROM {nombre_tabla}"
        df_resultado = obtener_datos(query)

        if df_resultado is not None:
            st.success(f"¡Éxito! Se encontraron {len(df_resultado)} filas.")
            
            # Mostrar vista previa
            st.dataframe(df_resultado.head(10))

            # --- BOTÓN DE DESCARGA ---
            # Convertimos el DataFrame a CSV
            csv = df_resultado.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Confirmar y Descargar CSV",
                data=csv,
                file_name=f'datos_{nombre_tabla}.csv',
                mime='text/csv',
            )