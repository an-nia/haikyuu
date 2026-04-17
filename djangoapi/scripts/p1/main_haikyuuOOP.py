import sys
from schools.schoolsOOP import SchoolsOOP
from stadiums.stadiumsOOP import StadiumsOOP
from nationals_travel.nationals_travelOOP import Nationals_TravelOOP

def main():
    # Comprobar que el usuario pasa exactamente 2 parámetros adicionales
    if len(sys.argv) == 3:
        tableName = sys.argv[1]
        functionName = sys.argv[2]
    else:
        print("Error: hay que dar 2 parámetros: tableName y functionName.")
        sys.exit(0)

    # Comprobar que la tabla existe
    if tableName not in ["stadiums", "schools", "nationals_travel"]:
        print("Error: los nombres de las tablas son: stadiums, schools, nationals_travel")
        sys.exit(0)

    # Comprobar que la función exista 
    valid_functions = ["insert", "update", "delete", "selectAsTuples", "selectAsDicts"]
    if functionName not in valid_functions:
        print(f"Error: las funciones existentes son: {', '.join(valid_functions)}")
        sys.exit(0)

    
    # TABLA STADIUMS
   
    if tableName == "stadiums":
        st = StadiumsOOP()
        
        if functionName == "insert":
            datos = {
                'name': 'Sendai City Gymnasium', 
                'city': 'Sendai', 
                'capacity': 5705, 
                'surface_type': 'Madera', 
                'num_courts': 4, 
                'geom': 'POLYGON((140.8710 38.2680, 140.8720 38.2680, 140.8720 38.2690, 140.8710 38.2690, 140.8710 38.2680))'}
            print("Ejecutando insert en stadiums...")
            print(st.insert(datos))
            
        elif functionName == "selectAsTuples":
            print(st.selectAsTuples({'id': 1}))

        elif functionName == "selectAsDicts":
            print(st.selectAsDicts({'id': 1}))
            
        elif functionName == "update":
            datos = {
                'id': 1,
                'name': 'Kamei Arena Sendai',
                'city': 'Sendai', 
                'capacity': 6000, 
                'surface_type': 'Madera', 
                'num_courts': 4, 
                'geom': 'POLYGON((140.8710 38.2680, 140.8720 38.2680, 140.8720 38.2690, 140.8710 38.2690, 140.8710 38.2680))'}
            print(st.update(datos))
            
        elif functionName == "delete":
            print(st.delete({'id': 1}))
            
        st.disconnect()

    
    # TABLA SCHOOLS 

    elif tableName == "schools":
        sc = SchoolsOOP()
        
        if functionName == "insert":
            datos = {
                'name': 'Karasuno High',
                'principal_name': 'Makoto Takeda',
                'students': 500,
                'volleyball_club_name': 'Karasuno Boys',
                'captain': 'Daichi Sawamura',
                'geom': 'POINT(140.8715 38.2685)'}
            print("Ejecutando insert en schools...")
            print(sc.insert(datos))
            
        elif functionName == "selectAsTuples":
            print(sc.selectAsTuples({'id': 1}))

        elif functionName == "selectAsDicts":
            print(sc.selectAsDicts({'id': 1}))
            
        elif functionName == "update":
            datos = {
                'id': 1,
                'name': 'Karasuno High',
                'principal_name': 'Makoto Takeda',
                'students': 510, 
                'volleyball_club_name': 'Karasuno Boys',
                'captain': 'Ennoshita', 
                'geom': 'POINT(140.8715 38.2685)'}
            print(sc.update(datos))
            
        elif functionName == "delete":
            print(sc.delete({'id': 1}))
            
        sc.disconnect()

    
    # TABLA NATIONALS_TRAVEL
    
    elif tableName == "nationals_travel":
        nt = Nationals_TravelOOP()
        
        if functionName == "insert":
            datos = {
                'team_name': 'Nekoma',
                'origin_prefecture': 'Tokyo',
                'vehicle_type': 'Tren',
                'stops_made': 0,
                'toll_cost_yen': 5000,
                'geom': 'LINESTRING(139.6917 35.6895, 140.8719 38.2682)'}
            print("Ejecutando insert en nationals_travel...")
            print(nt.insert(datos))
            
        elif functionName == "selectAsTuples":
            print(nt.selectAsTuples({'id': 1}))

        elif functionName == "selectAsDicts":
            print(nt.selectAsDicts({'id': 1}))
            
        elif functionName == "update":
            datos = {
                'id': 1,
                'team_name': 'Nekoma',
                'origin_prefecture': 'Tokyo',
                'vehicle_type': 'Tren Bala',
                'stops_made': 1,
                'toll_cost_yen': 8500,
                'geom': 'LINESTRING(139.6917 35.6895, 140.0000 37.0000, 140.8719 38.2682)'}
            print(nt.update(datos))
            
        elif functionName == "delete":
            print(nt.delete({'id': 1}))
            
        nt.disconnect()

if __name__ == "__main__":
    main()