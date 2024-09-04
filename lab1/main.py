from flask import Flask, jsonify, request
import random
from proximo_feriado import NextHoliday
from unidecode import unidecode

app = Flask(__name__)
peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]

 
def peliculas_genero(genero) : 
    "devuelve una lista con peliculas del mismo genero"
    resultado = []
    genero = unidecode(genero.capitalize())
    for pelicula in peliculas :
        if (unidecode(pelicula['genero'])) == genero :
            resultado.append(pelicula)
    return resultado


def obtener_peliculas():
    return jsonify(peliculas)


def obtener_pelicula(id):
    for pelicula in peliculas:
        if pelicula['id'] == id:
            return jsonify(pelicula), 200
    return jsonify({"error":"No existe la pelicula"}), 404


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    return jsonify(nueva_pelicula), 201


def actualizar_pelicula(id):
    for index, pelicula in enumerate(peliculas, start = 0):
        if pelicula['id'] == id:
            peli_act = {
                'id': id,
                'genero': request.json['genero'],
                'titulo': request.json['titulo']
            }
            peliculas[index] = peli_act
            return jsonify(peli_act), 200
        
    return jsonify({"error":"Pelicula no encontrada"}), 404


def eliminar_pelicula(id):
    for index, pelicula in enumerate(peliculas, start=0):
        if pelicula['id'] == id:
            del peliculas[index]
            return jsonify({"mensaje":"Pelicula eliminada correctamente"}), 200
        
    return jsonify({f"mensaje": "no existe pelicula con ID : {id}"}), 404


def listado_peliculas(genero):
    pelis_mismo_genero = peliculas_genero(genero)
    if pelis_mismo_genero == []:
        return jsonify({"error" : "no existe pelicula con tal genero"}), 404
    return jsonify(pelis_mismo_genero), 200


def determinado_string(det_string):
    resultado = []
    det_string = det_string.lower()
    for pelicula in peliculas:
        pelicula_lower = pelicula['titulo'].lower()
        if pelicula_lower.find(det_string) != -1:
            resultado.append(pelicula['titulo'])
    if resultado == []:
        return jsonify({"mensaje": f"No se encontró ninguna película con el string '{det_string}'"}), 404
    else :
        return jsonify(resultado), 200


def pelicula_aleatoria() :
    if (len(peliculas) > 0) :
        num_random = random.randint(0,len(peliculas)-1)
        resultado = {'pelicula_sugerida': peliculas[num_random]['titulo']}
        return jsonify(resultado), 200
    else :
        return jsonify({"error" : "no existe ninguna pelicula"}), 404


def pelicula_aleatoria_genero(genero) :
    pelis_mismo_genero = peliculas_genero(genero)
    if  pelis_mismo_genero != [] :
        num_random = random.randint(0,len(pelis_mismo_genero)-1)        
        return jsonify(pelis_mismo_genero[num_random]['titulo']), 200
    return jsonify({"error" : "no se entregó correctamenta la pelicula"}), 404


def recomendar_pelicula(genero):
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    pelis_mismo_genero = peliculas_genero(genero)
    if pelis_mismo_genero != [] :
        num_random = random.randint(0,len(pelis_mismo_genero)-1)
        month = next_holiday.holiday['mes']
        day = next_holiday.holiday['dia']
        return jsonify({"feriado": f"{day}/{month}", "puedes mirar esta pelicula": pelis_mismo_genero[num_random]['titulo']}), 200
    return {"error" : "no se entregó correctamente la pelicula"}, 404


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])
app.add_url_rule('/peliculas/<string:genero>','obtener_listado_genero',listado_peliculas,methods=['GET'])
app.add_url_rule('/peliculas/determinado_string/<string:det_string>','determinado_string',determinado_string,methods=['GET'])
app.add_url_rule('/peliculas/aleatorio','determinar_peli_random',pelicula_aleatoria,methods=['GET'])
app.add_url_rule('/peliculas/aleatorio/<string:genero>','determinar_peli_random_genero',pelicula_aleatoria_genero,methods=['GET'])
app.add_url_rule('/peliculas/recomendar/<string:genero>','recomendar_peli_feriado',recomendar_pelicula,methods=['GET'])


if __name__ == '__main__':
    app.run()
