# Proyecto de Créditos con Flask y SQLite

## Resumen

Al ejecutar el programa (`app.py`), Flask revisa si existe el archivo de la base de datos SQLite.  
Si no existe, lo crea automáticamente junto con la tabla necesaria para guardar los créditos.  
Así que no es necesario tener una carpeta ni un archivo previo.  

Cuando el usuario llena el formulario en la sección **Registrar un nuevo crédito** y da clic en **Agregar**,  
los datos se envían al servidor Flask mediante peticiones HTTP (`POST`, `PUT`, `DELETE`).  
El sistema guarda esa información en la base de datos y actualiza automáticamente la lista de créditos  
y las gráficas generadas con **matplotlib** y **Chart.js**, para reflejar los nuevos datos.  

Los IDs son autoincrementales, por lo que, aunque se elimine un registro, ese ID no se reutiliza.  
La interfaz se actualiza dinámicamente mediante JavaScript, que redibuja la tabla y las gráficas,  
sin que el usuario tenga que manejar directamente la base de datos.  

---

## Estructura del Proyecto

Josseline/
│ app.py
│ creditos.db
│ db.py
│
├── static/
│ └── style.css
│
└── templates/
└── index.html


- **app.py** → archivo principal, define la aplicación Flask y las rutas (`/`, `/api/creditos`, `/api/stats/...`).  
- **db.py** → contiene funciones para inicializar y manejar la base de datos SQLite.  
- **templates/** → contiene el HTML (`index.html`) que Flask renderiza.  
- **static/** → contiene el CSS y otros recursos estáticos.  

---

## Requisitos

- Python 3.10 o superior.  
- Gestor de paquetes de Python (`pip`, normalmente incluido con Python).  

- Verificar en terminal (cmd o powershell) con:  pip --version

## Instrucciones de instalación

1. Descargar el proyecto.

2. Abrir una terminal (CMD o PowerShell).

3. Una vez en la terminal. Entrar en la carpeta del proyecto con cd: ejemplo                                           " cd C:\users\persona1\desktop\nombre_proyecto "

4. Crear un entorno virtual: python -m venv venv

5. Activar el entorno virtual: venv\Scripts\activate

6. Instalar las dependencias necesarias: pip install flask matplotlib

## Ejecución

1. Con el entorno virtual activado, ejecutar el programa: python app.py

2. La terminal mostrará algo como: * Running on http://127.0.0.1:5000/

3. Abrir en el navegador: http://127.0.0.1:5000/

4. Desde la interfaz podrás:

- Registrar un nuevo crédito.

- Ver la lista de créditos y editar o eliminar registros.

- Consultar gráficas interactivas (por mes, por cliente, por distribución).

- Ver la gráfica generada por el servidor en formato PNG.

5. Para detener el servidor presiona: CTRL + C