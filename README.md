# thakhi
Módulo de solicitudes, necesidades e inspecciones de obra

- Activar POSTGIS

    sudo su postgres -c "psql -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql  NOMBRE_BD"
    sudo su postgres -c "psql -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql  NOMBRE_BD"

- Instalar dependencias para geoengine

    sudo apt-get install python-shapely python-pyproj
    sudo pip install geojson

- Instalar geoengine addon

    git clone https://github.com/OCA/geospatial.git
    git checkout 6.1

