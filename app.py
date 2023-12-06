from flask import Flask, render_template, request, jsonify, redirect, url_for

import mysql.connector

# init
app = Flask(__name__)

class Producto:
    
    # Constructor de la clase
    def __init__(self, host, user, password, database):
        # Primero, establecemos una conexión sin especificar la base de datos
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor(dictionary=True)

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database};")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.cursor.execute(f"CREATE DATABASE {database};")
                self.conn.database = database
            else:
                raise err

        # Una vez que la base de datos está establecida, creamos la tabla si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
            codigo INT PRIMARY KEY AUTO_INCREMENT,
            descripcion VARCHAR(255) NOT NULL,
            cantidad INT NOT NULL,
            precio DECIMAL(10, 2) NOT NULL,
            imagen_url VARCHAR(255),
            proveedor VARCHAR(255));''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    # ----------------------------------------------------------------
    def agregar_producto(self, codigo, descripcion, cantidad, precio, proveedor):
        # Verificamos si ya existe un producto con el mismo código
        self.cursor.execute("SELECT * FROM productos WHERE codigo = %s;", (codigo,))
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO productos (codigo, descripcion, cantidad, precio, proveedor) VALUES (%s, %s, %s, %s, %s);"
        valores = (codigo, descripcion, cantidad, precio, proveedor)

        if codigo is not None:
            self.cursor.execute("SELECT * FROM productos WHERE codigo = %s;", (codigo,))
            # Resto del código
        else:
            self.cursor.execute(sql, valores)        
            self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------

    def consultar_producto(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute("SELECT * FROM productos WHERE codigo = %s;", (codigo,))
        return self.cursor.fetchone()

    #----------------------------------------------------------------
    def modificar_producto(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nuevo_proveedor):
        sql = "UPDATE productos SET descripcion = %s, cantidad = %s, precio = %s, proveedor = %s WHERE codigo = %s;"
        valores = (nueva_descripcion, nueva_cantidad, nuevo_precio, nuevo_proveedor, codigo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        
        return self.cursor.rowcount > 0
    
    
    #----------------------------------------------------------------
    def listar_productos(self):
        self.cursor.execute("SELECT * FROM productos;")
        productos = self.cursor.fetchall()
        return productos

    #----------------------------------------------------------------
    def eliminar_producto(self, codigo):
        # Eliminamos un producto de la tabla a partir de su código
        
        self.cursor.execute(f"DELETE FROM productos WHERE codigo = {codigo};")
        self.conn.commit()
        return True

    #----------------------------------------------------------------
    def mostrar_producto(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        producto = self.consultar_producto(codigo)
        if producto:
            print("-" * 40)
            print(f"Código.....: {producto['codigo']}")
            print(f"Descripción: {producto['descripcion']}")
            print(f"Cantidad...: {producto['cantidad']}")
            print(f"Precio.....: {producto['precio']}")
            print(f"Proveedor..: {producto['proveedor']}")
            print("-" * 40)
        else:
            print("Producto no encontrado.")


# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def menu():
    return render_template('index.html')

@app.route('/productos')
def productos():
    # Obtener la lista de productos desde la instancia de Producto
    lista_productos = producto_instance.listar_productos()
    return render_template('productos.html', productos=lista_productos)

@app.route('/trabajaConNosotros')
def trabajaConNosotros():
    return render_template('trabajaConNosotros.html')

@app.route('/contactenos')
def contactenos():
    return render_template('contactenos.html')

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    # Lógica para agregar un nuevo producto
    if request.method == 'POST':
        # Obtén los datos del formulario y realiza las operaciones necesarias
        nueva_descripcion = request.form.get('nueva_descripcion')
        nueva_cantidad = request.form.get('nueva_cantidad')
        nuevo_precio = request.form.get('nuevo_precio')
        nuevo_proveedor = request.form.get('nuevo_proveedor')

        # Aquí deberías usar tu instancia de Producto para agregar el nuevo producto
        producto_instance.agregar_producto(
            codigo=None,  # Puedes dejar que la base de datos genere el código automáticamente
            descripcion=nueva_descripcion,
            cantidad=nueva_cantidad,
            precio=nuevo_precio,
            proveedor=nuevo_proveedor
        )

        # Después de agregar el producto, redirige a la página de productos
        return redirect(url_for('productos'))

    # Si es una solicitud GET o si la adición es exitosa, renderiza el formulario de adición
    return render_template('agregar_producto.html')

@app.route('/mostrar_producto/<int:codigo>')
def mostrar_producto(codigo):
    # Utiliza el método consultar_producto de la instancia de Producto
    producto = producto_instance.consultar_producto(codigo)

    # Verifica si el producto existe
    if producto:
        return render_template('mostrar_producto.html', producto=producto)
    else:
        # Si el producto no existe, puedes renderizar una plantilla de error o redirigir a otra página
        return render_template('producto_no_encontrado.html')

@app.route('/modificar_producto/<int:codigo>', methods=['GET', 'POST'])
def modificar_producto(codigo):
    # Lógica para obtener información del producto basado en el código
    producto = producto_instance.consultar_producto(codigo)

    # Verifica si el producto existe
    if not producto:
        # Si el producto no existe, puedes renderizar una plantilla de error o redirigir a otra página
        return render_template('producto_no_encontrado.html')

    if request.method == 'POST':
        # Lógica para manejar el formulario de modificación
        nueva_descripcion = request.form.get('nueva_descripcion')
        nueva_cantidad = request.form.get('nueva_cantidad')
        nuevo_precio = request.form.get('nuevo_precio')
        nuevo_proveedor = request.form.get('nuevo_proveedor')

        # Lógica para actualizar el producto en la base de datos
        if producto_instance.modificar_producto(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nuevo_proveedor):
            # Redirige a la página de productos después de la modificación
            return redirect(url_for('productos'))

    # Si es una solicitud GET o si la modificación es exitosa, renderiza el formulario de modificación
    return render_template('modificar_producto.html', producto=producto)

@app.route('/borrar_producto/<int:codigo>', methods=['POST'])
def borrar_producto(codigo):
    if codigo:
        producto_existente = producto_instance.consultar_producto(codigo)

        if producto_existente:
            producto_instance.eliminar_producto(codigo)
            return redirect(url_for('productos'))  # Redirige a la página de productos después de la eliminación
        else:
            return render_template('producto_no_encontrado.html')  # O renderiza una plantilla de error
    else:
        return jsonify({"mensaje": "Código no proporcionado"}), 400

#--------------------------------------------------------------------


producto_instance = Producto(host='localhost', user='root', password='', database='miapp3')

# run
if __name__ == "__main__":
    app.run(debug=True)
