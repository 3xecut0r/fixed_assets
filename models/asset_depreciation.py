from odoo import fields, models


class AssetDepreciation(models.Model):
    _name = 'asset.depreciation'
    _description = 'Asset Depreciation Summary'

    asset_id = fields.Many2one('account.asset', string='Asset')
    accumulated_depreciation = fields.Float(string='Accumulated Depreciation')
    date = fields.Date(string='Date', default=fields.Date.today())

    def create_monthly_depreciation_journal(self):
        for asset in self.env['account.asset'].search([]):
            if not asset.x_accumulated_depreciation:
                asset.compute_depreciation_board(date=fields.Date.today())
            self.create({
                'asset_id': asset.id,
                'accumulated_depreciation': asset.x_accumulated_depreciation,
                'date': fields.Date.today()
            })
