# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2012 Camptocamp SA
#	Adaptation to UPS by David Hernández
#	http://sinergiainformatica.net
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

from osv import osv, fields
import openerp.addons.decimal_precision as dp

class carrier_file(osv.osv):
    _inherit = 'delivery.carrier.file'

    def get_type_selection(self, cr, uid, context=None):
        result = super(carrier_file, self).get_type_selection(cr, uid, context=context)
        if 'Ups' not in result:
            result.append(('Ups', 'Envíos UPS'))
        return result
    

    def _get_package(self,cursor, user_id, context=None):
	return (
	    ('01','UPS Letter'),
	    ('02', 'Customer Supplied Package'))

    def _get_service(self,cursor, user_id,context=None):
	return (
	    ('01', 'Next Day Air'),
            ('02', '2nd Day Air'),
            ('03', 'Ground'),
            ('07', 'Express'),
            ('08', 'Expedited'),
            ('11', 'UPS Standard'),
            ('12', '3 Day Select'),
            ('13', 'Next Day Air Saver'),
            ('14', 'Next Day Air Early AM'),
            ('54', 'Express Plus'),
            ('59', '2nd Day Air A.M.'),
            ('65', 'UPS Saver'),
            ('82', 'UPS Today Standard'),
            ('83', 'UPS Today Dedicated Courier'),
            ('84', 'UPS Today Intercity'),
            ('85', 'UPS Today Express'),
            ('86', 'UPS Today Express Saver'))







    _columns = {
        'type': fields.selection(get_type_selection, 'Type', required=True),
	'xml_export':fields.boolean('Exportar a Xml?',help="Si esta marcado se exportara a XML, si no a csv"),
	'ups_account':fields.char('Ups Account', size=10),
	'ups_package_type':fields.selection(_get_package,'Tipo de paquete', help="Escoge el tipo de paquete"),
	'ups_service_level':fields.selection(_get_service, 'Tipo de servicio',help="Tipo de servicio"),
	'ups_description_goods':fields.char('Descripcion mercancia', size=30),
	'ups_cash':fields.boolean('Contrareembolso?', help="Marcar para contrareembolso"),
	'ups_cod_price':fields.float('Precio contrareembolso', digits_compute=dp.get_precision('Precio de reembolso')),	
    }

carrier_file()