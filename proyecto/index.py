import requests
from flask import Flask, render_template, request, jsonify, redirect

base_url= "http://localhost:5000"

app = Flask(__name__)

def imp(datos):
    for profesor in datos:
        id = profesor['id']
        nombre = profesor['nombre']
        correo = profesor['correo']
        direccion = profesor['direccion']
        print(id, nombre, correo, direccion)

def agregar(url, id, nombre, correo, direccion):
    payload = {
        'nombre': nombre,
        'correo': correo,
        'direccion': direccion
    }
    response = requests.post(f"{url}/profesor/registrar", json=payload)
    
    if response.status_code == 200:
        print("Profesor agregado exitosamente.")
    else:
        print(f"Error: {response.status_code}, {response.text}")


def eliminar(url, id):
    response = requests.delete(f"{url}/profesor/eliminar/{id}")
    
    if response.status_code == 200:
        print("Profesor eliminado exitosamente.")
    else:
        print(f"Error: {response.status_code}, {response.text}")

def editar(url, id, nombre, correo, direccion):
    payload = {
        'nombre': nombre,
        'correo': correo,
        'direccion': direccion
    }
    response = requests.put(f"{url}/profesor/modificar/{id}", json=payload)
    
    if response.status_code == 200:
        print("Profesor editado exitosamente.")
    else:
        print(f"Error: {response.status_code}, {response.text}")


def buscar(url, nombre):
    response = requests.get(f"{url}/profesor/{nombre}")
    
    if response.status_code == 200:
        profesores = response.json()
        if len(profesores) > 0:
            print("Profesores encontrados:")
            for profesor in profesores:
                id = profesor['id']
                id = int(id)
                nombre = profesor['nombre']
                correo = profesor['correo']
                direccion = profesor['direccion']
                print(f"ID: {id}, Nombre: {nombre}, Correo: {correo}, Dirección: {direccion}")
            return profesores
        else:
            print("No se encontraron profesores con ese nombre.")
            return []
    else:
        print(f"Error al buscar profesores: {response.status_code}, {response.text}")
        return []
    

@app.route('/agregar', methods=['POST'])
def agregar_profesor():
    global base_url
    nombre = request.form['nombre']
    correo = request.form['correo']
    direccion = request.form.get('direccion', '')

    # Llamar a la función agregar para añadir el nuevo profesor
    agregar(base_url, None, nombre, correo, direccion)

    return redirect('/')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_profesor(id):
    global base_url
    
    try:
        response = requests.get(f"{base_url}/profesor/editar/{id}")
        response.raise_for_status()
        profesor = response.json()
        print(profesor)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener los detalles del profesor: {e}")
        return "Error al obtener los detalles del profesor", 500
    
    if request.method == 'POST':
        # Procesar la actualización del formulario
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        direccion = request.form.get('direccion')
        
        editar(base_url, id, nombre, correo, direccion)
        
        return redirect('/')
    
    return render_template('editar.html', profesor=profesor)

@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_profesor(id):
    global base_url
    eliminar(base_url, id)
    return redirect('/')

@app.route('/')
@app.route('/')
def index():
    global base_url
    search_query = request.args.get('search')
    
    if search_query:
        data = buscar(base_url, search_query)
    else:
        try:
            response = requests.get(f"{base_url}/")
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al conectarse con el servidor Node.js: {e}")
            data = []

    return render_template('index.html', data=data, search_query=search_query if search_query else "")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    # Obtener y mostrar todos los profesores
    base_url = "http://localhost:5000"
    response = requests.get(f"{base_url}/")
    
    if response.status_code == 200:
        datos = response.json()
        imp(datos)
    else:
        print(f"Error: {response.status_code}")
    