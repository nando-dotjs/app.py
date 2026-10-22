import streamlit as st
import pyodbc

st.title("Consultar Espacio SQL Server")

with st.form("connection_form"):
    server = st.text_input("Instancia")
    database = st.text_input("Base de Datos")
    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    submitted = st.form_submit_button("Consultar")

if submitted:
    conn_str = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={user};PWD={password};Encrypt=no;TrustServerCertificate=yes;"
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        query = """
        SELECT 
            name AS [Archivo],
            size * 8.0 / 1024 AS [Tamaño_MB],
            CAST(FILEPROPERTY(name, 'SpaceUsed') AS INT) * 8.0 / 1024 AS [Usado_MB],
            (size - CAST(FILEPROPERTY(name, 'SpaceUsed') AS INT)) * 8.0 / 1024 AS [Libre_MB]
        FROM sys.database_files;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        
        st.success("¡Conexión exitosa!")
        
        for row in rows:
            st.subheader(f"Archivo: {row[0]}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Tamaño Total", f"{row[1]:.2f} MB")
            col2.metric("Espacio Usado", f"{row[2]:.2f} MB")
            col3.metric("Espacio Libre", f"{row[3]:.2f} MB")
            
        conn.close()
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")