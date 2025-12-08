# Gestión de Productos - Joyería

Aplicación web para la gestión de inventario de una joyería, desarrollada con **Python**, **Flask** y **MongoDB**.

## 📋 Requisitos Previos

- Python 3.10 o superior (recomendado Python 3.12).
- Servidor MongoDB ejecutándose localmente (o acceso a un clúster remoto).

## 🚀 Instalación y Configuración

Sigue estos pasos para configurar el proyecto en tu entorno local:

1.  **Clonar el repositorio** (si aplica) o descargar el código fuente.

2.  **Crear un entorno virtual** (opcional pero recomendado):
    ```bash
    # En Windows
    python -m venv venv
    venv\Scripts\activate

    # En macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuración de Base de Datos**:
    - Asegúrate de que MongoDB esté corriendo en `mongodb://localhost:27017/`.
    - La aplicación utiliza la base de datos llamada `dbb_products_app`.
    - Si necesitas cambiar la URI de conexión, edita el archivo `app/database/database.py`.

## 💻 Ejecución

Para iniciar el servidor de desarrollo:

```bash
python app.py
```

La aplicación estará disponible en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📂  Estructura del Proyecto

- **app.py**: Punto de entrada de la aplicación.
- **app/**: Paquete principal.
    - **database/**: Conexión a MongoDB.
    - **models/**: Modelos de datos (Producto).
    - **routes/**: Definición de rutas y controladores.
    - **templates/**: Plantillas HTML (Jinja2).
    - **static/**: Archivos estáticos (imágenes subidas en `uploads/`).

## 🛠️ Funcionalidades

- **CRUD de Productos**: Crear, Leer, Actualizar y Eliminar productos.
- **Filtros**: Búsqueda por nombre, categoría y rango de precios.
- **Imágenes**: Carga y gestión de imágenes de productos.
- **Validaciones**: Verificación de campos obligatorios y tipos de datos.

## ⚠️ Notas Importantes

- **Imágenes**: Las imágenes se guardan en `app/static/uploads/`. Asegúrate de no borrar la carpeta `static` aunque esté vacía inicialmente.
