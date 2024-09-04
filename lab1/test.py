import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/peliculas')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()


# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()


# Obtener detalles de una película específica
id_pelicula = 40 # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()


# Actualizar los detalles de una película
id_pelicula = 15  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()


# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.\n")
else:
    print("Error al eliminar la película.\n")


# Obtener listado de películas por género
genero = "drama"
response = requests.get(f'http://localhost:5000/peliculas/{genero}')
if response.status_code == 200 :
    date = response.json()
    print(f"listado de peliculas del genero: {genero}:\n")
    for peli in date :
        print(f"ID : {peli['id']}, Titulo: {peli['titulo']}, Género : {peli['genero']}\n")
else :
    print("error al pasar el genero")
  

# Obtener película por determinado string
string = "park"
response = requests.get(f'http://localhost:5000/peliculas/determinado_string/{string}')
if response.status_code == 200 :
    print(f"se encuentra la palabra {string} dentro de un titulo\n")
else :
    print(f"no se encuentra la palabra {string}\n")
    

# Obtener película aleatoria
response = requests.get('http://localhost:5000/peliculas/aleatorio')
if response.status_code == 200 :
    peli_aleatoria = response.json()
    print(f"se dió correctamenta la pelicula aleatoria : {peli_aleatoria}\n")
else :
    print("no se dio correctamente una pelicula aleatoria\n")

    
# Obtener película aleatoria por genero
genero = "Drama"
response = requests.get(f'http://localhost:5000/peliculas/aleatorio/{genero}')
if response.status_code == 200 :
    peli_aleatoria_genero = response.json()
    print(f"se entrego correctamenta la pelicula aleatoria del genero : {genero}\n")
else :
    print(f"no se entrego correctamente la pelicula aleatoria del genero : {genero}\n")

# Obtener película aleatoria
genero = "crimenes"
response = requests.get(f'http://localhost:5000/peliculas/recomendar/{genero}')
if response.status_code == 200 :
    print("se entrego correctamente la pelicula")
else :
    print("no se entrego correctamente la pelicula")