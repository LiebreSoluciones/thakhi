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

class thakhi_contrato(osv.osv):
    _name = "thakhi.contrato"

    _columns = {
        'name': fields.char('Número', size=128),
        'objeto': fields.text('Objeto Contractual'),
        'contratista_id': fields.many2one('res.partner','Contratista'),
        'state': fields.selection(
            [('en_ejecucion','En ejecución'),('suspendido','Suspendido'),('en_liquidacion','En Liquidación'),('liquidado','Liquidado')],
            'Estado',
            required=True,
        ),
        'tipo': fields.selection(
            [('obra','Obra'),('interventoria','Interventoria')],
            'Tipo',
            required=True,
        ),
        'fecha_inicio': fields.datetime('Fecha Inicio', required=True),
        'fecha_fin': fields.datetime('Fecha Finalización', required=True),
        'valor_total': fields.integer('Valor Total'),
        'contrato_interventoria_id': fields.many2one('thakhi.contrato','Contrato de Interventoria'),
        'is_interventoria_interna': fields.boolean('La interventoria es interna?'),
    }

    _defaults = {
        'state': 'en_ejecucion',
    }

thakhi_contrato()
