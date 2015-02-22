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
from res_city import get_details_from_point, geocode_address

class thakhi_solicitud(osv.osv):
    _name = "thakhi.solicitud"

    _columns = {
        'id': fields.integer('Identificador', readonly=True),
        'name': fields.char('Asunto', size=128),
        'descripcion': fields.text('Descripción'),
        'solicitante_id': fields.many2one('res.partner.address','Solicitante'),
        'radicado': fields.char('Número de radicado',
            size=32,
            help="Número de radicado del sistema de PQRS",
            required=True
        ),
        'fecha_radicado': fields.datetime('Fecha del radicado', required=True),
        'state': fields.selection(
            [('abierta','Abierta'),('cerrada','Cerrada'),('rechazada','Rechazada')],
            'Estado',
            required=True,
        ),
        'necesidad_ids': fields.one2many('thakhi.necesidad',
            'solicitud_id',
            'Necesidades',
        )
    }

    _defaults = {
        'state': 'abierta',
    }

thakhi_solicitud()


class thakhi_necesidad(geo_model.GeoModel):
    _name = "thakhi.necesidad"

    _columns = {
        'id': fields.integer('Identificador', readonly=True),
        'name': fields.char('Asunto', size=128),
        'direccion': fields.char('Dirección', size=128),
        'descripcion': fields.text('Descripción'),
        'prioridad': fields.selection(
            [(1,'Alta'),(3,'Media'),(5,'Baja')],
            'Prioridad',
            required=True,
        ),
        'state': fields.selection(
            [('abierta','Abierta'),('cerrada','Cerrada'),('rechazada','Rechazada')],
            'Estado',
            required=True,
        ),
        'solicitud_id': fields.many2one('thakhi.solicitud','Solicitud'),
        'inspeccion_ids': fields.one2many('thakhi.inspeccion',
            'necesidad_id',
            'Inspecciones',
        ),
        'project_id': fields.many2one('project.project','Proyecto'),
        'shape': fields.geo_point('Ubicación'),
        'district_id': fields.many2one('res.city.district','Localidad'),
        'subdistrict_id': fields.many2one('res.city.subdistrict','UPZ'),
        'neighborhood_id': fields.many2one('res.city.neighborhood','Barrio'),
    }

    _defaults = {
        'state': 'abierta',
        'prioridad': 3,
    }

    def onchange_geopoint(self, cr, uid, ids, point):
        res = {
            'value': get_details_from_point(cr, uid, ids, point),
        }
        return res

    def onchange_direccion(self, cr, uid, ids, direccion):
        res = {'value':{'shape':False}}
        if direccion:
            url_geocoder = self.pool.get('ir.config_parameter').get_param(cr, uid, 'geo_coder.ws.url', default='http://webidu.idu.gov.co:9090/arcgis1/rest/services/Geocodificador/GeocodeIDU/GeocodeServer/findAddressCandidates?', context=None)
            srid = self.pool.get('ir.config_parameter').get_param(cr, uid, 'geo_coder.srid', default='esri.extra:900913', context=None)
            zone = 1100100 #Bogota
            point = geocode_address(direccion, srid, url_geocoder, zone)
            res['value']['shape'] = point
        return res

thakhi_necesidad()


class thakhi_inspeccion(osv.osv):
    _name = "thakhi.inspeccion"

    _columns = {
      'id': fields.integer('Identificador', readonly=True),
      'name': fields.char('Asunto', size=128),
      'state': fields.selection(
            [('abierta','Abierta'),('cerrada','Cerrada'),('rechazada','Rechazada')],
            'Estado',
            required=True,
        ),
        'fecha': fields.datetime('Fecha', required=True),
        'duracion_programada_horas': fields.float('Duración', help="Duración de la inspección"),
        'necesidad_id': fields.many2one('thakhi.necesidad','Necesidad'),
        'funcionario_id': fields.many2one('res.users','Funcionario'),
        'elemento_infraestructura_id': fields.many2one('thakhi.elemento_infraestructura','Elemento'),
        'tipo_trabajo_id': fields.many2one('thakhi.tipo_trabajo','Tipo de Trabajo',
            domain="[('elemento_infraestructura_id','=',elemento_infraestructura_id)]",
        ),
        'actividad_obra_ids': fields.one2many('thakhi.actividad_obra',
            'inspeccion_id',
            'Actividades de Obra',
        ),
        'causa_ids': fields.many2many('thakhi.causa_dano',
                 'thakhi_inspecion_causa_rel',
                 'inspeccion_id',
                 'causa_id',
                 'Causas del daño'
        ),
        'valor_total': fields.float('Valor Total'),
        'project_id': fields.many2one('project.project','Proyecto'),
    }

    _defaults = {
        'state': 'abierta',
    }

thakhi_inspeccion()


class thakhi_elemento_infraestructura(osv.osv):
    _name = "thakhi.elemento_infraestructura"

    _columns = {
      'name': fields.char('Nombre', size=128),
      'descripcion': fields.text('Descripción'),
    }

thakhi_elemento_infraestructura()


class thakhi_tipo_trabajo(osv.osv):
    _name = "thakhi.tipo_trabajo"

    _columns = {
      'name': fields.char('Nombre', size=128),
      'descripcion': fields.text('Descripción'),
      'elemento_infraestructura_id': fields.many2one('thakhi.elemento_infraestructura','Elemento'),
    }

thakhi_tipo_trabajo()


class thakhi_actividad_obra(osv.osv):
    _name = "thakhi.actividad_obra"

    _columns = {
      'name': fields.char('Nombre', size=128),
      'descripcion': fields.text('Descripción'),
      'product_id': fields.many2one('product.product','Producto', required=True),
      'uom_id': fields.many2one('product.uom','Unidad de Medida', required=True),
      'valor_unidad': fields.float('Valor Unidad', required=True),
      'valor_total': fields.float('Valor Total', required=True),
      'cantidad': fields.float('Cantidad', required=True),
      'inspeccion_id': fields.many2one('thakhi.inspeccion','Inspección', required=True),
    }

thakhi_actividad_obra()


class thakhi_causa_dano(osv.osv):
    _name = "thakhi.causa_dano"

    _columns = {
      'name': fields.char('Nombre', size=128),
      'descripcion': fields.text('Descripción'),
    }


thakhi_causa_dano()
