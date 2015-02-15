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
from base_geoengine import geo_model


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
    _name="res.city.district"
    _columns = {
        'name': fields.char('Nombre',size=256),
        'code': fields.char('Código',size=25),
        'city_id': fields.many2one('res.city','Ciudad'),
        'shape': fields.geo_multi_polygon('Shape'),
    }
res_city_district()


class res_city_subdistrict(geo_model.GeoModel):
    _name="res.city.subdistrict"
    _columns={
        'name': fields.char('Nombre',size=256),
        'code': fields.char('Código',size=25),
        'classification': fields.integer('Clasificación'),
        'shape': fields.geo_multi_polygon('Shape'),
    }
res_city_subdistrict()


class res_city_neighborhood(geo_model.GeoModel):
    _name = 'res.city.neighborhood'
    _order = 'name asc'
    _columns = {
        'code': fields.char('Código',size=25),
        'name': fields.char('Nombre', size=256),
        'shape':fields.geo_multi_polygon('Geometry'),
    }
res_city_neighborhood()

