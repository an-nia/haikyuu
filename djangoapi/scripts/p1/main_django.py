from scripts.p1.haikyuu_django.schools_django import Schools
from scripts.p1.haikyuu_django.stadiums_django import Stadiums
from scripts.p1.haikyuu_django.nationals_travel_django import NationalsTravel

def run(*args):
    if len(args) != 2:
        print("Error: Se necesitan dos parámetros: nombre_tabla y nombre_funcion.")
        print("Uso: python manage.py runscript scripts.p1.main_django --script-args <tabla> <funcion>")
        return

    table_name = args[0]
    function_name = args[1]

    valid_tables = ["schools", "stadiums", "nationals_travel"]
    valid_functions = ["insert", "update", "delete", "selectAsDicts", "selectAsTuples"]

    # Validaciones de entrada
    if table_name not in valid_tables:
        print(f"Error: La tabla debe ser una de {valid_tables}")
        return

    if function_name not in valid_functions:
        print(f"Error: La función debe ser una de {valid_functions}")
        return

    # ==========================================
    # Datos de prueba 
    # Para probar las funciones en consola.
    
    data_schools = {
        'id': 1,
        'description': 'Escuela de prueba',
        'name': 'Karasuno High',
        'principal_name': 'Director Karasuno',
        'students': 800,
        'volleyball_club_name': 'Cuervos',
        'captain': 'Daichi Sawamura',
        'geom': 'POINT(5 5)'}

    data_stadiums = {
        'id': 1,
        'description': 'Estadio de prueba',
        'name': 'Tokyo Metropolitan Gymnasium',
        'city': 'Tokyo',
        'capacity': 10000,
        'surface_type': 'Madera',
        'num_courts': 4,
        'geom': 'POLYGON((0 0, 10 0, 10 10, 0 10, 0 0))'}

    data_travel = {
        'id': 1,
        'description': 'Viaje a las nacionales',
        'team_name': 'Karasuno',
        'origin_prefecture': 'Miyagi',
        'vehicle_type': 'Autobús',
        'stops_made': 2,
        'total_cost_yen': 50000,
        'geom': 'LINESTRING(0 0, 10 10, 20 20)'}
    
    #Datos que darían error. Hay que tener los otros añadidos primero.
    # data_schools = {
    #     'id': 2,
    #     'description': 'Nekoma High',
    #     'name': 'Nekoma',
    #     'principal_name': 'Director Nekoma',
    #     'students': 600,
    #     'volleyball_club_name': 'Gatos',
    #     'captain': 'Kuroo Tetsuro',
    #     'geom': 'POINT(50 50)'} #Está fuera del estadio (0 a 10).
    
    # data_stadiums = {
    #     'id': 2,
    #     'description': 'Estadio Inarizaki',
    #     'name': 'Inarizaki Gym',
    #     'city': 'Hyogo',
    #     'capacity': 8000,
    #     'surface_type': 'Sintético',
    #     'num_courts': 3,
    #     'geom': 'POLYGON((5 5, 15 5, 15 15, 5 15, 5 5))'}  #Invade el espacio del estadio 1.
    
    # data_travel = {
    #     'id': 2,
    #     'description': 'Viaje de Fukurodani',
    #     'team_name': 'Fukurodani',
    #     'origin_prefecture': 'Tokyo',
    #     'vehicle_type': 'Tren bala',
    #     'stops_made': 1,
    #     'total_cost_yen': 30000,
    #     'geom': 'LINESTRING(0 20, 20 0)'} #Se choca con la línea 1 en el punto (10 10).
    
    #Geometría inválida
    # data_stadiums = {
    #     'id': 2,
    #     'description': 'Estadio Inarizaki',
    #     'name': 'Inarizaki Gym',
    #     'city': 'Hyogo',
    #     'capacity': 8000,
    #     'surface_type': 'Sintético',
    #     'num_courts': 3,
    #     'geom': 'POLYGON((0 0, 10 0, 10 10, 0 10))'} # Falta el ", 0 0" al final para cerrarlo.

    # ==========================================
    # Instanciar las clases

    if table_name == "schools":
        obj = Schools()
        d = data_schools
    elif table_name == "stadiums":
        obj = Stadiums()
        d = data_stadiums
    elif table_name == "nationals_travel":
        obj = NationalsTravel()
        d = data_travel

    # ==========================================
    # Ejecución

    print(f"\nEjecutando '{function_name}' en la tabla '{table_name}'...")
    
    if function_name == "insert":
        resultado = obj.insert(d)
    elif function_name == "update":
        resultado = obj.update(d)
    elif function_name == "delete":
        resultado = obj.delete(d)
    elif function_name == "selectAsDicts":
        resultado = obj.selectAsDicts(d)
    elif function_name == "selectAsTuples":
        resultado = obj.selectAsTuples(d)

    # Mostrar resultado
    print("-" * 50)
    print("Respuesta del servidor:")
    print(resultado)
    print("-" * 50)