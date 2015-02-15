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
##############################################################################
{
        "name" : "ThaKhi - geoengine data - bogota",
        "version" : "1.0",
        "author" : "Liebre Soluciones Ltda",
        "website" : "www.liebresoluciones.com",
        "category" : "Project Management",
        "description": """
Datos de los mapas base de bogota
        """,
        "depends" : ['base', 'thakhi'],
        "demo_xml" : [],
        "init_xml" : [
                        'res_city_disctrict.xml',
                        'res_city_neighborhood_bogota.xml',
                        'res_city_subdisctrict.xml',
                       ],
        "installable": True
}