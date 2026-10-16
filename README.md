# TechStore API

API REST desarrollada con **Python y FastAPI** para gestionar productos y consultar pedidos de una tienda de tecnología.

## Funcionalidades

- Listar y buscar productos.
- Filtrar por categoría y rango de precios.
- Consultar el producto más caro.
- Contar productos por categoría.
- Consultar pedidos y estadísticas de clientes.

## Tecnologías

- Python
- FastAPI
- Uvicorn

## Instalación y ejecución

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar el servidor:

```bash
uvicorn main:app --reload
```

Documentación de la API: http://127.0.0.1:8000/docs

## Nota

El proyecto utiliza listas de Python como base de datos simulada.

## Autor

Proyecto práctico de aprendizaje de Python y FastAPI.