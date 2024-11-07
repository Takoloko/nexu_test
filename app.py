from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import json

# Inicializamos la app y la base de datos
app = Flask(__name__)

# Configuración de la base de datos (SQLite en este caso)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definimos el modelo para 'Model'
class Model(db.Model):
    __tablename__ = 'models'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    average_price = db.Column(db.Integer, nullable=False)
    brand_name = db.Column(db.String(100), nullable=False)

# Cargar los datos desde el archivo models.json a la base de datos
def load_data_from_json():
    """Carga los datos desde el archivo JSON a la base de datos"""
    with open('models.json', 'r') as file:
        data = json.load(file)

    for item in data:
        model = Model(id=item['id'], name=item['name'], average_price=item['average_price'], brand_name=item['brand_name'])
        db.session.add(model)
    
    db.session.commit()

    # Endpoint para obtener los modelos de una marca específica
@app.route('/brands/<string:brand_name>/models', methods=['GET'])
def get_models_by_brand(brand_name):
    # Buscar todos los modelos que pertenezcan a una marca dada
    models = Model.query.filter_by(brand_name=brand_name).all()

    # Si no se encuentran modelos para esa marca, retornar un error 404
    if not models:
        abort(404, description="Brand not found")

    return jsonify([{
        'id': model.id,
        'name': model.name,
        'average_price': model.average_price
    } for model in models])

# Endpoint para actualizar el precio promedio de un modelo
@app.route('/models/<int:id>', methods=['PUT'])
def update_model_price(id):
    # Obtener el modelo por su ID
    model = Model.query.get(id)

    # Si el modelo no existe, retornar un error 404
    if not model:
        return jsonify({"error": "Model not found"}), 404

    # Obtener los datos desde el cuerpo de la solicitud
    data = request.get_json()

    # Verificar si el precio promedio fue proporcionado
    if 'average_price' not in data:
        return jsonify({"error": "Average price is required"}), 400

    average_price = data['average_price']

    # Validar que el precio promedio sea mayor que 100,000
    if average_price <= 100000:
        return jsonify({"error": "Average price must be greater than 100,000"}), 400

    # Actualizar el precio promedio
    model.average_price = average_price

    # Guardar los cambios en la base de datos
    db.session.commit()

    # Retornar la respuesta exitosa con el modelo actualizado
    return jsonify({
        'id': model.id,
        'name': model.name,
        'average_price': model.average_price,
        'brand_name': model.brand_name
    })


"""
# Este código se ejecuta antes de la primera solicitud
@app.before_request
def initialize():
    #Inicializa la base de datos con los datos desde el JSON
    db.create_all()  # Crear las tablas
    load_data_from_json()  # Cargar los datos del JSON
    """

# Ruta principal
@app.route('/')
def home():
    return "Bienvenido a la API de Nexu"

# Endpoint para obtener todas las marcas
@app.route('/brands', methods=['GET'])
def get_brands():
    brands = db.session.query(Model.brand_name).distinct().all()  # Obtener las marcas únicas
    return jsonify([brand[0] for brand in brands])

# Endpoint para obtener todos los modelos
@app.route('/models', methods=['GET'])
def get_models():
    models = Model.query.all()

# Obtener los parámetros 'greater' y 'lower' de la consulta
    greater_than = request.args.get('greater', type=int)
    lower_than = request.args.get('lower', type=int)
    
    # Filtrar los modelos según los parámetros proporcionados
    filtered_models = models

  # Filtrar si se proporciona el parámetro 'greater'
    if greater_than:
        filtered_models = [model for model in filtered_models if model.average_price > greater_than]
    
    # Filtrar si se proporciona el parámetro 'lower'
    if lower_than:
        filtered_models = [model for model in filtered_models if model.average_price < lower_than]
    
    # Devolver los modelos filtrados

    return jsonify([{
        'id': model.id,
        'name': model.name,
        'average_price': model.average_price,
        'brand_name': model.brand_name
    } for model in filtered_models])

if __name__ == '__main__':
    # Inicia la aplicación Flask
    app.run(debug=True)
