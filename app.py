from flask import Flask, render_template, request
import csv

app = Flask(__name__)

productos = []
with open('Products.txt', 'r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    for fila in lector:
        productos.append({
            "nombre": fila['product'],
            "category": fila['category'],
            "rating": float(fila['rating'])
        })

def sugerir_productos_dfs(producto_nombre, num_recomendaciones=5):
    producto_ingresado = next((p for p in productos if producto_nombre.lower() in p['nombre'].lower()), None)

    if not producto_ingresado:
        return f"Producto '{producto_nombre}' no encontrado."

    # Crear un grafo de productos por categoría
    grafo = {}
    for p in productos:
        if p['category'] not in grafo:
            grafo[p['category']] = []
        grafo[p['category']].append(p)

    # DFS para buscar productos relacionados
    stack = grafo[producto_ingresado['category']]  # Empezamos con los productos de la misma categoría
    visitados = set()
    productos_relacionados = []

    while stack:
        producto = stack.pop()
        if producto['nombre'] not in visitados:
            visitados.add(producto['nombre'])
            if producto['category'] == producto_ingresado['category'] and producto['nombre'] != producto_ingresado['nombre']:
                productos_relacionados.append(producto)

    # Ordenar los productos por rating
    productos_relacionados.sort(key=lambda x: x['rating'], reverse=True)

    # Seleccionamos los primeros 'num_recomendaciones' productos
    recomendaciones = productos_relacionados[:num_recomendaciones]

    if recomendaciones:
        return recomendaciones  # Regresamos la lista de productos recomendados
    else:
        return "No se encontraron productos relacionados."


@app.route('/', methods=['GET', 'POST'])
def index():
    sugerencia = ""
    if request.method == 'POST':
        producto_nombre = request.form['producto']
        sugerencia = sugerir_productos_dfs(producto_nombre)
    return render_template('index.html', sugerencia=sugerencia)

if __name__ == '__main__':
    app.run(debug=True)