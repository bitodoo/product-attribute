# -*- coding: utf-8 -*-
# © 2009 NetAndCo (<http://www.netandco.net>).
# © 2011 Akretion Benoît Guillot <benoit.guillot@akretion.com>
# © 2014 prisnet.ch Seraphine Lantible <s.lantible@gmail.com>
# © 2016 Serpent Consulting Services Pvt. Ltd.
# © 2018 Daniel Campos <danielcampos@avanzosc.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models, tools


class ProductBrand(models.Model):
    _name = 'product.brand'
    _order = 'name'

    name = fields.Char('Brand Name', required=True)
    description = fields.Text('Description', translate=True)
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Select a partner for this brand if any.',
        ondelete='restrict'
    )
    logo = fields.Binary('Logo File', attachment=True)
    image = fields.Binary(related="logo")
    product_ids = fields.One2many(
        'product.template',
        'product_brand_id',
        string='Brand Products',
    )
    products_count = fields.Integer(
        string='Number of products',
        compute='_get_products_count',
    )
    image_medium = fields.Binary(
        string='Medium-sized image', attachment=True,
        help='Medium-sized logo of the brand. It is automatically '
             'resized as a 128x128px image, with aspect ratio preserved. '
             'Use this field in form views or some kanban views.')
    image_small = fields.Binary(
        string='Small-sized image', attachment=True,
        help='Small-sized logo of the brand. It is automatically '
             'resized as a 64x64px image, with aspect ratio preserved. '
             'Use this field anywhere a small image is required.')

    @api.model
    def create(self, vals):
        tools.image_resize_images(vals)
        return super(ProductBrand, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(ProductBrand, self).write(vals)

    @api.multi
    @api.depends('product_ids')
    def _get_products_count(self):
        for brand in self:
            brand.products_count = len(brand.product_ids)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
        help='Select a brand for this product'
    )
