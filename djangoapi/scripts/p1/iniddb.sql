CREATE EXTENSION IF NOT EXISTS postgis;
CREATE SCHEMA IF NOT EXISTS haikyuu;

CREATE TABLE haikyuu.schools (
    id serial primary key,
    name text,                 
    principal_name text,      
    students integer,        
    volleyball_club_name text,         
    captain text,      
    geom geometry("POINT", 4326));

CREATE TABLE haikyuu.stadiums (
    id serial primary key,
    name text,                
    city text,                 
    capacity integer,         
    surface_type text,         
    num_courts integer,        
    geom geometry("POLYGON", 4326));

CREATE TABLE haikyuu.nationals_travel (
    id serial primary key,
    team_name text,            
    origin_prefecture text,    
    vehicle_type text,         
    stops_made integer,        
    toll_cost_yen double precision, 
    geom geometry("LINESTRING", 4326));

INSERT INTO haikyuu.schools (
    name, 
    principal_name, 
    students, 
    volleyball_club_name, 
    captain, 
    geom
) VALUES (
    'Karasuno High School', 
    'Makoto Takeda', 
    500, 
    'Karasuno Boys Volleyball Club', 
    'Daichi Sawamura', 
    ST_GeometryFromText('POINT(140.8719 38.2682)', 4326));

INSERT INTO haikyuu.stadiums (
    name, city, capacity, surface_type, num_courts, geom
) VALUES (
    'Sendai City Gymnasium',
    'Sendai',
    5705,
    'Madera',
    4, 
    ST_GeometryFromText('POLYGON((140.8735 38.2212, 140.8752 38.2212, 140.8752 38.2198, 140.8735 38.2198, 140.8735 38.2212))', 4326));

INSERT INTO haikyuu.nationals_travel (
    team_name, 
    origin_prefecture, 
    vehicle_type, 
    stops_made, 
    toll_cost_yen, 
    geom
) VALUES (
    'Karasuno', 
    'Miyagi', 
    'Autobús escolar alquilado', 
    3, 
    8500.00, 
    ST_GeometryFromText('LINESTRING(140.8719 38.2682, 140.3800 37.5000, 139.6917 35.6895)', 4326));