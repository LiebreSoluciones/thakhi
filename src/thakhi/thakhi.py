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
        'origen_solicitud_id': fields.many2one('thakhi.solicitud.origen','Tipo Solicitud'),
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


class thakhi_solicitud_origen(osv.osv):
    _name = "thakhi.solicitud.origen"

    _columns = {
        'name': fields.char('Asunto', size=128),
    }

thakhi_solicitud_origen()


class thakhi_necesidad(geo_model.GeoModel):
    _name = "thakhi.necesidad"

    _columns = {
        'id': fields.integer('Identificador', readonly=True),
        'name': fields.char('Asunto', size=128),
        'direccion': fields.char('Dirección', size=128),
        'descripcion': fields.text('Descripción'),
        'prioridad': fields.selection(
            [('alta','Alta'),('media','Media'),('baja','Baja')],
            'Prioridad',
            required=True,
        ),
        'state': fields.selection(
            [('abierta','Abierta'),('cerrada','Cerrada'),('rechazada','Rechazada')],
            'Estado',
            required=True,
        ),
        'solicitud_id': fields.many2one('thakhi.solicitud','Solicitud'),
        'visita_ids': fields.one2many('thakhi.visita',
            'necesidad_id',
            'Visitas',
        ),
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


class thakhi_visita(osv.osv):
    _name = "thakhi.visita"

    _columns = {
        'id': fields.integer('Identificador', readonly=True),
        'name': fields.char('Asunto', size=128),
        'state': fields.selection(
            [('abierta','Abierta'),('cerrada','Cerrada'),('rechazada','Rechazada')],
            'Estado',
            required=True,
        ),
        'fecha': fields.datetime('Fecha', required=True),
        'duracion_programada_horas': fields.float('Duración', help="Duración de la inspección en horas"),
        'necesidad_id': fields.many2one('thakhi.necesidad','Necesidad'),
        'funcionario_id': fields.many2one('res.users','Funcionario'),
        'solicitud_id': fields.related('necesidad_id', 'solicitud_id',
            type="many2one",
            relation="thakhi.solicitud",
            string="Solicitud",
            store=True,
            readonly=True,
        ),
        'inspeccion_ids': fields.one2many('thakhi.inspeccion',
            'visita_id',
            'Inspecciones',
        ),
    }

    _defaults = {
        'state': 'abierta',
        'necesidad_id': lambda self, cr, uid, context: context['necesidad_id'] if context and 'necesidad_id' in context else None,
    }

thakhi_visita()


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
        'visita_id': fields.many2one('thakhi.visita', 'Visita'),
        'necesidad_id': fields.related('visita_id', 'necesidad_id',
            type="many2one",
            relation="thakhi.necesidad",
            string="Necesidad",
            store=True,
            readonly=True,
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
        'foto_ids': fields.one2many('thakhi.foto', 'inspeccion_id', 'Registro Fotografico'),
        'valor_total': fields.float('Valor Total'),
        'project_id': fields.many2one('project.project','Proyecto'),
        'segmento_id': fields.many2one('thakhi.segmento','Segmento', required=True),
        'tipo_via_id': fields.related('segmento_id', 'tipo_via_id',
            type="many2one",
            relation="thakhi.tipo_via",
            string="Tipo de Vía",
            store=False,
        ),
        'tipo_trafico_id': fields.related('segmento_id', 'tipo_trafico_id',
            type="many2one",
            relation="thakhi.tipo_trafico",
            string="Tipo de Tráfico",
            store=False,
        ),
        'plan_manejo_trafico_id': fields.many2one('thakhi.plan_manejo_trafico','PMT'),
    }

    _defaults = {
        'state': 'abierta',
        'visita_id': lambda self, cr, uid, context: context['visita_id'] if context and 'visita_id' in context else None,
        'necesidad_id': lambda self, cr, uid, context: context['necesidad_id'] if context and 'necesidad_id' in context else None,
    }

    _sql_constraints = [
        ('unique_segmento_visita','unique(visita_id,segmento_id)','La visita no puede incluir varias veces el mismo segmento'),
    ]

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
      'tipo_superficie_id': fields.many2one('thakhi.tipo_superficie','Tipo Superficie'),
    }

thakhi_tipo_trabajo()


class thakhi_actividad_obra(osv.osv):
    _name = "thakhi.actividad_obra"

    _columns = {
      'name': fields.char('Nombre', size=128),
      'descripcion': fields.text('Descripción'),
      'inspeccion_id': fields.many2one('thakhi.inspeccion','Inspección', required=True),
      'elemento_infraestructura_id': fields.many2one('thakhi.elemento_infraestructura','Elemento'),
      'tipo_superficie_id': fields.many2one('thakhi.tipo_superficie', 'Tipo Superfice',
          domain="[('elemento_infraestructura_id','=',elemento_infraestructura_id)]",
      ),
      'tipo_trabajo_id': fields.many2one('thakhi.tipo_trabajo','Tipo de Trabajo',
            domain="[('elemento_infraestructura_id','=',elemento_infraestructura_id),'|',('tipo_superficie_id','=',tipo_superficie_id),('tipo_superficie_id','=',False)]",
      ),
      'product_id': fields.many2one('product.product','Producto', required=True),
      'cantidad': fields.float('Cantidad', required=True),
      'uom_id': fields.many2one('product.uom','Unidad de Medida', required=True),
      'valor_unidad': fields.float('Valor Unidad', required=True),
      'valor_total': fields.float('Valor Total', required=True),
    }

thakhi_actividad_obra()


class thakhi_causa_dano(osv.osv):
    _name = "thakhi.causa_dano"

    _columns = {
      'name': fields.char('Nombre', size=128),
      'descripcion': fields.text('Descripción'),
    }


thakhi_causa_dano()


class thakhi_segmento(osv.osv):
    _name = "thakhi.segmento"

    _columns = {
        'name': fields.char('CIV (Codigo de Identificacion Vial)', size=32, select=True),
        'CODIGO_UPZ': fields.char('Codigo UPZ', size=50),
        'CODIGO_LOCALIDAD': fields.char('Codigo Localidad', size=50),
        'TIPO_CLASIFICACION_VIA': fields.integer('Tipo Clasificación Via'),
        'TIPO_CLASIFICACION_POT': fields.integer('Tipo Clasificación POT'), 
        'CODIGO_VIA': fields.integer('Código Via'),
        'CODIGO_TIPO': fields.integer('Código Tipo'),
        'NOMBRE_EJE_VIA': fields.char('Nombre Eje Via', size=50),
        'NOMBRE_EXTREMO_INICIAL': fields.char('Nombre Extremo Inicial', size=50),
        'NOMBRE_EXTREMO_FINAL': fields.char('Nombre Extremo Final', size=50),
        'TIPO_MALLA': fields.char('Tipo Malla', size=50),
        'tipo_via_id': fields.many2one('thakhi.tipo_via','Tipo Vía'),
        'tipo_trafico_id': fields.many2one('thakhi.tipo_trafico','Tipo Tráfico'),
    }

thakhi_segmento()

class thakhi_tipo_via(osv.osv):
    _name = "thakhi.tipo_via"

    _columns = {
        'name': fields.char('Nombre', size=255),
        'codigo': fields.char('Código', size=10),
    }

thakhi_tipo_via()


class thakhi_tipo_trafico(osv.osv):
    _name = "thakhi.tipo_trafico"

    _columns = {
        'name': fields.char('Nombre', size=255),
        'codigo': fields.char('Código', size=10),
    }

thakhi_tipo_trafico()


class thakhi_tipo_superficie(osv.osv):
    _name = "thakhi.tipo_superficie"

    _columns = {
        'name': fields.char('Nombre', size=255),
        'codigo': fields.char('Código', size=10),
        'elemento_infraestructura_id': fields.many2one('thakhi.elemento_infraestructura','Elemento'),
    }

thakhi_tipo_superficie()

class thakhi_plan_manejo_trafico(osv.osv):
    _name = "thakhi.plan_manejo_trafico"

    _columns = {
        'name': fields.char('Nombre', size=255),
        'codigo': fields.char('Código', size=10),
    }

thakhi_plan_manejo_trafico()


class thakhi_foto(osv.osv):
    _name="thakhi.foto"

    def _get_binary_filesystem(self, cr, uid, ids, name, arg, context=None):
        """ Display the binary from ir.attachment, if already exist """
        res = {}
        attachment_obj = self.pool.get('ir.attachment')

        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = False
            attachment_ids = attachment_obj.search(cr, uid, [('res_model','=',self._name),('res_id','=',record.id),('binary_field','=',name)], context=context)
            if attachment_ids:
                img  = attachment_obj.browse(cr, uid, attachment_ids, context=context)[0].datas
                res[record.id] = img
        return res

    def _set_binary_filesystem(self, cr, uid, id_, name, value, arg, context=None):
        """ Create or update the binary in ir.attachment when we save the record """
        attachment_obj = self.pool.get('ir.attachment')

        attachment_ids = attachment_obj.search(cr, uid, [('res_model','=',self._name),('res_id','=',id_),('binary_field','=',name)], context=context)
        if value:
            if attachment_ids:
                attachment_obj.write(cr, uid, attachment_ids, {'datas': value}, context=context)
            else:
                foto_name = 'Foto_{0}_{1}'.format(self._name,id_)
                _datas_fname = 'Foto_{0}_{1}.jpg'.format(self._name,id_)
                attachment_obj.create(cr, uid, {'res_model': self._name, 'res_id': id_, 'name': foto_name, 'binary_field': name, 'datas': value, 'datas_fname':_datas_fname}, context=context)
        else:
            attachment_obj.unlink(cr, uid, attachment_ids, context=context)

    _columns={
        'name': fields.char('Descripción corta',size=256, required=True),
        'foto': fields.function(_get_binary_filesystem, fnct_inv=_set_binary_filesystem, type='binary', string='Fotografía'),
        'descripcion': fields.text('Descripción larga'),
        'inspeccion_id': fields.many2one('thakhi.inspeccion', 'Inspección', ondelete="cascade"),
    }

thakhi_foto()

class ir_attachment(osv.osv):

    _inherit = 'ir.attachment'

    _columns = {
        'binary_field': fields.char('Binary field', size=128)
    }
