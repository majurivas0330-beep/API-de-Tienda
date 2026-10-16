from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI(title="TechStore API")

#-------------- BASE DE DATOS FALSA ----------------------
productos = [
    {"id" : 1, "nombre": "Laptop Pro", "categoria": "computadoras", "precio": 1200, "stock": 5},
    {"id" : 2, "nombre": "Mouse Inalámbrico", "categoria": "accesorios", "precio": 25, "stock": 50},
    {"id" : 3, "nombre": "Teclado Mecánico", "categoria": "accesorios", "precio": 80, "stock": 0},
    {"id" : 4, "nombre": "Monitor 27\"", "categoria": "computadoras", "precio": 300, "stock": 12},
    {"id" : 5, "nombre": "Audífonos BT", "categoria": "audio", "precio": 60, "stock": 30},
    {"id" : 6, "nombre": "Parlante Mini", "categoria": "audio", "precio": 45, "stock": 8},
    {"id" : 7, "nombre": "Tablet 10\"", "categoria": "computadoras", "precio": 250, "stock": 15},
]

# ---------------------- Reto 1: Categorías ----------------------
@app.get("/categorias")
async def contar_categorias():
    categorias = {}

    for producto in productos:
        categoria = producto["categoria"]

        if categoria in categorias:
            categorias[categoria] += 1
        else:
            categorias[categoria] = 1

    return categorias

# ----------------------Tabla Pedidos------------------------------------
pedidos = [
    {"id": 101, "cliente_id": 1, "producto": "Laptop Pro", "total": 1200,  "estado": "completado"},
    {"id": 102, "cliente_id": 1, "producto": "Mouse Inalámbrico", "total": 25,  "estado": "pendiente"},
    {"id": 103, "cliente_id": 1, "producto": "Monitor 27\"", "total": 300,  "estado": "completado"},
    {"id": 104, "cliente_id": 2, "producto": "Audífonos BT", "total": 60,  "estado": "pendiente"},
    {"id": 105, "cliente_id": 2, "producto": "Tablet 10\"", "total": 250,  "estado": "completado"},
]


# ------------------endpoint de pedidos--------------------------
# Se hizo una modificación del código debido al reto 4
# ---------------------- Reto 4: Estadísticas del cliente ----------------------
@app.get("/clientes/{cliente_id}/pedidos")
async def pedidos_del_cliente(
    cliente_id: int,
    estado: str | None = None,
    orden: str = "id"
):
    mis_pedidos = [
        p for p in pedidos
        if p["cliente_id"] == cliente_id
    ]

    if not mis_pedidos:
        raise HTTPException(
            status_code=404,
            detail=f"El cliente {cliente_id} no tiene pedidos"
        )

    if estado:
        mis_pedidos = [
            p for p in mis_pedidos
            if p["estado"] == estado
        ]

    if orden == "total_desc":
        mis_pedidos.sort(
            key=lambda p: p["total"],
            reverse=True
        )

    gasto_total = sum(p["total"] for p in mis_pedidos)
    cantidad_pedidos = len(mis_pedidos)

    if cantidad_pedidos > 0:
        pedido_mas_caro = max(
            mis_pedidos,
            key=lambda p: p["total"]
        )
        promedio_gasto = gasto_total / cantidad_pedidos
    else:
        pedido_mas_caro = None
        promedio_gasto = 0

    return {
        "cliente_id": cliente_id,
        "cantidad_pedidos": cantidad_pedidos,
        "gasto_total": gasto_total,
        "pedido_mas_caro": pedido_mas_caro,
        "promedio_gasto": promedio_gasto,
        "pedidos": mis_pedidos
    }


# ------------------endpoint de productos------------------------
@app.get("/")
async def inicio():
    return {"mensaje": "Bienvenido a TechStore", "total_productos": len(productos)}

# ---------------------- Reto 2: Producto más caro ----------------------
@app.get("/productos/mas-caro")
async def producto_mas_caro():
    producto = max(productos, key=lambda p: p["precio"])
    return producto

# ---------------------- Reto 5: Búsqueda por texto ----------------------
@app.get("/productos/buscar")
async def buscar_productos(q: str):
    resultado = [
        p for p in productos
        if q.lower() in p["nombre"].lower()
    ]

    return {
        "busqueda": q,
        "cantidad": len(resultado),
        "productos": resultado
    }

@app.get("/productos/{producto_id}")
async def obtener_producto(producto_id: int):
    for producto in productos:
        if producto["id"] == producto_id:
            return producto

    raise HTTPException(
        status_code=400,
        detail=f"El producto con id {producto_id} no existe"
    )


@app.get("/productos")
async def listar_productos(
    categoria: str | None = None,
    min_precio: float | None = None,
    max_precio: float | None = None,
    solo_disponibles: bool = False,
    orden: str = "id",
    pagina: int = 1,
    tamano: int = 3
):
    resultado = productos.copy()

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]

    if min_precio is not None:
        resultado = [p for p in resultado if p["precio"] >= min_precio]

    if max_precio is not None:
        resultado = [p for p in resultado if p["precio"] <= max_precio]

    if solo_disponibles:
        resultado = [p for p in resultado if p["stock"] > 0]

    if orden == "precio_asc":
        resultado.sort(key=lambda p:  p["precio"])
    elif orden == "precio_desc":
        resultado.sort(key=lambda p: p["precio"], reverse=True)


    inicio = (pagina - 1) * tamano
    fin = inicio + tamano
    pagina_resultados = resultado[inicio:fin]

    return {
        "total_encontrados": len(resultado),
        "pagina": pagina,
        "tamano": tamano,
        "productos": pagina_resultados
    }