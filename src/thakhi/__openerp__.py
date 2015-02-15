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
        "name" : "ThaKhi",
        "version" : "1.0",
        "author" : "Liebre Soluciones Ltda",
        "website" : "www.liebresoluciones.com",
        "category" : "Project Management",
        "description": """
Módulo para la gestión de solicitudes de atención de daños sobre infraestructura urbana.
        """,
        "depends" : ['base',
                     'project',
                    ],
        "demo_xml" : [],
        "update_xml" : [
                        'thakhi_view.xml',
                        'project_view.xml',
                        'contrato_view.xml',
                       ],
        "installable": True
}