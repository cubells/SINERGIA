# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

from osv import fields, osv
import openerp.addons.decimal_precision as dp

class product_product(osv.osv):
    _name = 'product.product'
    _inherit = 'product.product'

    def test(self, cr, uid, ids, field_names=None, arg=None, context=None):
        result = {}
        if not ids:return result

        context['only_with_stock'] = True

        for id in ids:
            context['product_id'] = id
            location_obj = self.pool.get('stock.location')
            result[id] = location_obj.search(cr, uid, [('usage', '=', 'internal')], context=context)

        return result

    # STOCK IN EACH LOCATION

    def stock_Pt(self, cr, uid, ids, field_names=None, arg=None, context=None):
        result = {}
        stock_prod_obj = self.pool.get('stock.report.prodlots')
        for prod_id in ids:

            stock_prod_ids = stock_prod_obj.search(cr, uid, [('product_id', '=', prod_id),
                                                             ('location_id', '=', 15)]
                                                   ,
                                                   context=context)
            if stock_prod_ids:
                for i in stock_prod_obj.browse(cr, uid, stock_prod_ids, context=context):
                    result[prod_id] = i.qty

            else:
                result[prod_id] = 0.000
        return result

    def stock_Bcn(self, cr, uid, ids, field_names=None, arg=None, context=None):
        result = {}
        stock = {}
        stock_prod_obj = self.pool.get('stock.report.prodlots')
        for prod_id in ids:
            stock_prod_ids = stock_prod_obj.search(cr, uid, [('product_id', '=', prod_id),
                                                             ('location_id', '=', 19)],
                                                   context=context)
            if stock_prod_ids:
                for i in stock_prod_obj.browse(cr, uid, stock_prod_ids, context=context):
                    result[prod_id] = i.qty

            else:
                result[prod_id] = 0.000
        return result

    def stock_Grn(self, cr, uid, ids, field_names=None, arg=None, context=None):
        stock = {}
        result = {}
        stock_prod_obj = self.pool.get('stock.report.prodlots')
        for prod_id in ids:
            stock_prod_ids = stock_prod_obj.search(cr, uid, [('product_id', '=', prod_id),
                                                             ('location_id', '=', 12)],
                                                   context=context)
            if stock_prod_ids:
                for i in stock_prod_obj.browse(cr, uid, stock_prod_ids, context=context):
                    result[prod_id] = i.qty

            else:
                result[prod_id] = 0.000
        return result

    _columns = {
        'locations': fields.function(test, type='one2many', relation='stock.location', string='Stock by Location'),
        'scooters_ids': fields.many2many('scooter.asociaciones', 'scooter_compat_with_product_rel', 'product_id',
                                         'scooter_id', 'scooter models'),
        'stock_grn': fields.function(stock_Grn, type='float', string='GRN: '),
        'stock_bcn': fields.function(stock_Bcn, type='float', string='BCN: '),
        'stock_pt': fields.function(stock_Pt, type='float', string='PT: '),
        'internal_note': fields.text('Nota Interna', translate=True),
        'pvp_fabricante': fields.float('Precio Base TT',
                                       digits_compute=dp.get_precision('Precio Base TT (Tarifa Fabricante sin IVA)')),

    }


product_product()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
