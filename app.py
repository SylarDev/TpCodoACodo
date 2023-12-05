from flask import Flask, render_template, request, jsonify, redirect, url_for
# # from flask_cors import CORS
# from flaskext.mysql import MySQL

import mysql.connector
# # from werkzeug.utils import secure_filename
# # import os
# # import time

# init
app = Flask(__name__)

# # Mysql Settings
# mysql = MySQL()
# app.config['MYSQL_DATABASE_HOST']     = 'localhost'
# app.config['MYSQL_DATABASE_USER']     = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'tomba30db'
# app.config['MYSQL_DATABASE_DB']       = 'flaskcontacts'
# app.config['MYSQL_DATABASE_TABLE']    = 'productos'
# mysql.init_app(app)



# CORS(app)

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
            proveedor INT);''')
        self.conn.commit()

        # Cerrar el cursor inicial y abrir uno nuevo con el parámetro dictionary=True
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)
        
    # ----------------------------------------------------------------
    def agregar_producto(self, codigo, descripcion, cantidad, precio, proveedor):
        # Verificamos si ya existe un producto con el mismo código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo};")
        producto_existe = self.cursor.fetchone()
        if producto_existe:
            return False

        sql = "INSERT INTO productos (codigo, descripcion, cantidad, precio, proveedor) VALUES (%s, %s, %s, %s, %s);"
        valores = (codigo, descripcion, cantidad, precio, proveedor)

        self.cursor.execute(sql, valores)        
        self.conn.commit()
        return self.cursor.rowcount > 0

    #----------------------------------------------------------------

    def consultar_producto(self, codigo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM productos WHERE codigo = {codigo};")
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
    lista_de_productos = producto_instance.listar_productos()
    return render_template('productos.html', products=lista_de_productos)


@app.route('/trabajaConNosotros')
def trabajaConNosotros():
    return render_template('trabajaConNosotros.html')

@app.route('/contactenos')
def contactenos():
    return render_template('contactenos.html')


@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nueva_descripcion = request.form.get('nueva_descripcion')
        nueva_cantidad = request.form.get('nueva_cantidad')
        nuevo_precio = request.form.get('nuevo_precio')
        nuevo_proveedor = request.form.get('nuevo_proveedor')

        # Validar los campos (agrega más validaciones según sea necesario)

        # Lógica para agregar un nuevo producto
        # Por ejemplo, podrías utilizar tu instancia de Producto
        producto_instance.agregar_producto(
            codigo=None,  # Puedes dejar que la base de datos genere el código automáticamente
            descripcion=nueva_descripcion,
            cantidad=nueva_cantidad,
            precio=nuevo_precio,
            proveedor=nuevo_proveedor
        )

    return redirect(url_for('productos'))

@app.route('/modificar_producto', methods=['POST'])
def modificar_producto():
    if request.method == 'POST':
        codigo = request.form.get('codigo')
        nueva_descripcion = request.form.get('nueva_descripcion')
        nueva_cantidad = request.form.get('nueva_cantidad')
        nuevo_precio = request.form.get('nuevo_precio')
        nuevo_proveedor = request.form.get('nuevo_proveedor')

        # Validar los campos (agrega más validaciones según sea necesario)

        # Lógica para modificar un producto
        # Por ejemplo, podrías utilizar tu instancia de Producto
        producto_instance.modificar_producto(
            codigo=codigo,
            nueva_descripcion=nueva_descripcion,
            nueva_cantidad=nueva_cantidad,
            nuevo_precio=nuevo_precio,
            nuevo_proveedor=nuevo_proveedor
        )

    return redirect(url_for('productos'))

@app.route('/eliminar_producto', methods=['POST'])
def eliminar_producto():
    if request.method == 'POST':
        codigo = request.form.get('codigo')

        # Lógica para eliminar un producto
        # Por ejemplo, podrías utilizar tu instancia de Producto
        producto_instance.eliminar_producto(codigo)

    return redirect(url_for('productos'))


producto_instance = Producto(host='localhost', user='root', password='', database='miapp')

producto_instance.agregar_producto(codigo=1, descripcion='Producto 1', cantidad=10, precio=19.99, proveedor=1)
producto_instance.agregar_producto(codigo=2, descripcion='Producto 2', cantidad=5, precio=29.99, proveedor=2)
producto_instance.agregar_producto(codigo=3, descripcion='Producto 3', cantidad=8, precio=39.99, proveedor=1)


# run
if __name__ == "__main__":
    app.run(debug=True)