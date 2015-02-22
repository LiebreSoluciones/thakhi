# -*- coding: utf-8 -*-
##############################################################################
#
#    Liebre Soluciones LTDA, ThaKhi
#    Copyright (C) 2014-now Liebre Soluciones LTDA (<http://www.liebresoluciones.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from osv import fields, osv
from openerp.osv.osv import except_osv
from base_geoengine import geo_model
from pyproj import Proj
from pyproj import transform
import json
import logging
import urllib
import math

_logger = logging.getLogger(__name__)


class res_city(geo_model.GeoModel):
    _name="res.city"
    _columns = {
        'name': fields.char('Nombre',size=256),
        'code': fields.char('Código',size=25),
        'state_id': fields.many2one('res.country.state','Departamento'),
        'shape': fields.geo_multi_polygon('Shape'),
    }
res_city()


class res_city_district(geo_model.GeoModel):
    _name = "res.city.district"
    _description = "Localidad"
    _columns = {
        'name': fields.char('Nombre',size=256),
        'code': fields.char('Código',size=25),
        'city_id': fields.many2one('res.city','Ciudad'),
        'shape': fields.geo_multi_polygon('Shape'),
    }
res_city_district()


class res_city_subdistrict(geo_model.GeoModel):
    _name = "res.city.subdistrict"
    _description = "UPZ - Unidad de Planeación Zonal"

    def _get_district_name(self, cr, uid, ids, fieldname, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context = context):
            query = "SELECT name FROM res_city_district \
                WHERE INTERSECTS(shape, ST_GEOMETRYFROMTEXT('{0}',900913)) IS TRUE".format(record.shape)
            cr.execute(query)
            district_id = False
            for n_ids in cr.fetchall():
                for i in n_ids :
                    district_id = i
            res[record.id] = district_id
        return  res

    _columns = {
        'name': fields.char('Nombre',size=256),
        'code': fields.char('Código',size=25),
        'classification': fields.integer('Clasificación'),
        'shape': fields.geo_multi_polygon('Shape'),
        'district_name': fields.function(
             _get_district_name,
             type="char",
             string='Localidad',
             store=True,
         ),
    }
res_city_subdistrict()


class res_city_neighborhood(geo_model.GeoModel):
    _name = 'res.city.neighborhood'
    _description = 'Barrio'
    _order = 'name asc'

    def _get_district_name(self, cr, uid, ids, fieldname, arg, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context = context):
            query = "SELECT name FROM res_city_district \
                WHERE INTERSECTS(shape, ST_GEOMETRYFROMTEXT('{0}',900913)) IS TRUE".format(record.shape)
            cr.execute(query)
            district_id = False
            for n_ids in cr.fetchall():
                for i in n_ids :
                    district_id = i
            res[record.id] = district_id
        return  res

    _columns = {
        'code': fields.char('Código',size=25),
        'name': fields.char('Nombre', size=256),
        'shape':fields.geo_multi_polygon('Geometry'),
        'district_name': fields.function(
             _get_district_name,
             type="char",
             string='Localidad',
             store=True,
         ),
    }
res_city_neighborhood()


def get_details_from_point(cr, uid, ids, point):
    try:
        if (point is not False):
            """
            Calculating District, Subdistrict and Neighborhood from point
            """
            coord = json.loads(point)["coordinates"]
            x = coord[0]
            y = coord[1]
            query = "SELECT id FROM res_city_district \
                WHERE INTERSECTS(shape, ST_GEOMETRYFROMTEXT('POINT({0} {1})',900913)) IS TRUE".format(x,y)
            cr.execute(query)
            district_id = False
            for n_ids in cr.fetchall():
                for i in n_ids :
                    district_id = i

            query = "SELECT id FROM res_city_subdistrict \
                WHERE INTERSECTS(shape, ST_GEOMETRYFROMTEXT('POINT({0} {1})',900913)) IS TRUE".format(x,y)
            cr.execute(query)
            subdistrict_id = False
            for n_ids in cr.fetchall():
                for i in n_ids :
                    subdistrict_id = i

            query_neigh = "SELECT id FROM res_city_neighborhood \
                WHERE INTERSECTS(shape, ST_GEOMETRYFROMTEXT('POINT({0} {1})',900913)) IS TRUE".format(x,y)
            cr.execute(query_neigh)
            neighborhood_id = False
            for n_ids in cr.fetchall():
                for i in n_ids :
                    neighborhood_id = i
            return {
                'district_id': district_id,
                'subdistrict_id': subdistrict_id,
                'neighborhood_id': neighborhood_id
            }
        else :
            return {}
    except Exception, exc:
        raise except_osv(_('Falló al procesar el punto geográfico'), str(exc))


def geocode_address(addr, srid, uri = '', zone = 1100100): #Default = Bogota
    """
    Resolve geo - location from address with REST web service technique
    Parameters :
    addr = Address to Geocode
    srid = Spatial Reference System ID. in this format ie "epsg:4326" or "other.extra:900913"
    uri = Geocoder Web Service addr, for idu = http://gi03cc01/ArcGIS/rest/services/GeocodeIDU/GeocodeServer/findAddressCandidates?
    zone = City or town code for example Bogota = 1100100
    REST POST Example http://gi03cc01/ArcGIS/rest/services/GeocodeIDU/GeocodeServer/findAddressCandidates?Street=cra+82+a+6+37&Zone=Bogot%C3%A1+D.C.&outFields=&outSR=&f=html
    """
    try:
        addr = addr.encode('utf8')
        url = "{0}Street={1}&Zone={2}&outSR={3}&f=pjson".format(uri, addr, zone, 4326)
        #Because to Geocoder Bug, first we need to get information in Geographic coordinate system
        _logger.info("URL: {0}".format(url))
        jsonstr = urllib.urlopen(url).read()
        vals = json.loads(jsonstr)
        if (len(vals) >= 2):
            candidates = vals['candidates']
            _logger.info("candidates: {0}".format(candidates))
            for candidate in candidates :
                location = candidate['location']
                x = location['x']
                y = location['y']
                if (not (math.isnan(x) or math.isnan(y))):
                    if (srid is "epsg:4326"):
                        x1 = x
                        y1 = y
                    else :
                        pGeographic = Proj(init="epsg:4326")
                        pOtherRefSys = Proj(init=srid)
                        x1,y1 = transform(pGeographic, pOtherRefSys, x, y)
                        #format :   {"type": "Point", "coordinates": [746676.106813609, 5865349.7175855]}            
                        return '{"type": "Point", "coordinates":[%10.12f, %10.12f]}' % (x1,y1)
    except Exception as e:
        _logger.error(str(e))
        return False
    return False
