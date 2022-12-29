from odoo import fields, models, Command, exceptions

class IhneretedEstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        #import ipdb; ipdb.set_trace()
        partner_id = False
        if self.offer_ids:
            for offer in self.offer_ids:
                if offer.status == 'accepted':
                    partner_id = offer.partner_id
                    break
        else:
            raise exceptions.ValidationError('Properties can not be sold without an offer!')

        if partner_id:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': partner_id.id,
                'invoice_line_ids': [
                    Command.create({'name' : 'properties_invoice_'+ partner_id.name,'price_unit': self.selling_price * 0.6, 'quantity': 1}),
                    Command.create({'name' : 'Administrative fees','price_unit': 100, 'quantity': 1}),
                ],
                }
            )
            return super().action_sold()
        else:
            raise exceptions.ValidationError('Properties can not be sold without an accepted offer!')