# -*- coding: utf-8 -*-
{
    "name" : "Estension de modulo productos para incorporar modelos de Scooter",
    "version" : "7.0",
    "author" : "David Hernández",
    "category" : "Generic Modules/Others",
    "website" : "http://sinergiainformatica.net",
    "description": "Extensión módulo productos para relacionarlos con modelos de Scooter."
                   "Añade campo de relación con los modelos en la ficha de producto."
                   "Añade campo de relación en la ficha de cliente."
                   "Discrimina las lineas de la orden en función de si el producto es o no"
                   "compatible con el modelo de moto del cliente de la orden",
    "depends" : ["product", "sale"],
    "update_xml" : ["product_motoscoot_view.xml", "partner_motoscoot_view.xml",
                    "scooter_models_view.xml", "marcas_scooter_view.xml", "asociaciones_view.xml",
                    "sale_view.xml"],

    "data": ['security/security.xml', 'security/ir.model.access.csv'],
    "active": True,
    "installable": True
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
