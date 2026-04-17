'''
Funciones:
- insert
- delete
- update
- selectAsTuples: dado un ID, devuelve lista con las filas que contengan el id
- selectAsDicts: dado un ID, devuelve un diccionario con las filas que contengan el id
'''

import psycopg
from psycopg.rows import dict_row
from myLib.connect2 import connect
from myLib.p1Settings2 import EPSG_CODE

class Nationals_TravelOOP():
    def __init__(self):
        self.conn=connect()
        self.cur=self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()    

    def insert(self, d):
        geom_wkt = d['geom']
        
        # Comprobar geometría
        self.cur.execute("SELECT ST_IsValid(ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))", [geom_wkt, EPSG_CODE])
        if not self.cur.fetchone()[0]:
            return {'ok': False, 'message': 'Error: la geometría de línea no es válida.', 'data': None}
            
        # Rechazar si cruza con otra línea 
        check_query = """
            SELECT id FROM haikyuu.nationals_travel 
            WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))
        """
        self.cur.execute(check_query, [geom_wkt, EPSG_CODE])
        if len(self.cur.fetchall()) > 0:
            return {'ok': False, 'message': 'Error: la ruta cruza con una línea existente.', 'data': None}

        # Insertar
        insert_query = """
            INSERT INTO haikyuu.nationals_travel 
            (team_name, origin_prefecture, vehicle_type, stops_made, toll_cost_yen, geom)
            VALUES (%s, %s, %s, %s, %s, ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))
            RETURNING id
        """
        values = [d['team_name'], d['origin_prefecture'], d['vehicle_type'], d['stops_made'], d['toll_cost_yen'], geom_wkt, EPSG_CODE]
        try:
            self.cur.execute(insert_query, values)
            new_id = self.cur.fetchone()[0]
            self.conn.commit()
            return {'ok': True, 'message': 'Data inserted', 'data': [{'id': new_id}]}
        except Exception as e:
            self.conn.rollback()
            return {'ok': False, 'message': str(e), 'data': None}

    def update(self, d):
        geom_wkt = d['geom']
        row_id = d['id']
        
        # Comprobar geometría
        self.cur.execute("SELECT ST_IsValid(ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001))", [geom_wkt, EPSG_CODE])
        if not self.cur.fetchone()[0]:
            return {'ok': False, 'message': 'Error: La geometría no es válida.', 'data': None}

        # Rechazar si cruza con otra línea      
        check_query = """
            SELECT id FROM haikyuu.nationals_travel 
            WHERE ST_Intersects(geom, ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001)) AND id != %s
        """
        self.cur.execute(check_query, [geom_wkt, EPSG_CODE, row_id])
        if len(self.cur.fetchall()) > 0:
            return {'ok': False, 'message': 'Error: la ruta intersecta con otra línea.', 'data': None}

        # Actualizar
        update_query = """
            UPDATE haikyuu.nationals_travel 
            SET team_name=%s, origin_prefecture=%s, vehicle_type=%s, stops_made=%s, toll_cost_yen=%s, 
                geom=ST_SnapToGrid(ST_GeometryFromText(%s, %s), 0.0001)
            WHERE id=%s
        """
        values = [d['team_name'], d['origin_prefecture'], d['vehicle_type'], d['stops_made'], d['toll_cost_yen'], geom_wkt, EPSG_CODE, row_id]
        try:
            self.cur.execute(update_query, values)
            rows_updated = self.cur.rowcount
            self.conn.commit()
            return {'ok': True, 'message': 'Data updated', 'data': [{'rows_updated': rows_updated}]}
        except Exception as e:
            self.conn.rollback()
            return {'ok': False, 'message': str(e), 'data': None}

    def delete(self, d):
        try:
            self.cur.execute("DELETE FROM haikyuu.nationals_travel WHERE id=%s", [d['id']])
            rows_deleted = self.cur.rowcount
            self.conn.commit()
            return {'ok': True, 'message': 'Data deleted', 'data': [{'rows_deleted': rows_deleted}]}
        except Exception as e:
            self.conn.rollback()
            return {'ok': False, 'message': str(e), 'data': None}

    def selectAsTuples(self, d):
        try:
            self.cur.execute("SELECT id, team_name, origin_prefecture, vehicle_type, stops_made, toll_cost_yen, ST_AsText(geom) FROM haikyuu.nationals_travel WHERE id=%s", [d['id']])
            results = self.cur.fetchall()
            return {'ok': True, 'message': 'Data retrieved', 'data': results}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': None}
    
    def selectAsDicts(self, d):
        try:
            dict_cur = self.conn.cursor(row_factory=dict_row)
            dict_cur.execute("SELECT id, team_name, origin_prefecture, vehicle_type, stops_made, toll_cost_yen, ST_AsText(geom) FROM haikyuu.nationals_travel WHERE id=%s", [d['id']])
            results = dict_cur.fetchall()
            dict_cur.close()
            return {'ok': True, 'message': 'Data retrieved', 'data': results}
        except Exception as e:
            return {'ok': False, 'message': str(e), 'data': None}