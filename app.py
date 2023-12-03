from flask import Flask, render_template

# init
app = Flask(__name__)

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def menu():
    return render_template('index.html')

@app.route('/productos')
def productos():
    return render_template('productos.html')

@app.route('/trabajaConNosotros')
def trabajaConNosotros():
    return render_template('trabajaConNosotros.html')

@app.route('/contactenos')
def contactenos():
    return render_template('contactenos.html')


# run
if __name__ == "__main__":
    app.run(debug=True)
