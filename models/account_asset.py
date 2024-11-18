from datetime import datetime

from odoo import api, fields, models


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    x_accumulated_depreciation = fields.Float(string='Accumulated Depreciation', compute='_compute_accumulated_depreciation')
    x_qty = fields.Integer(string='Quantity', default=1)
    state = fields.Selection(
        selection=[('model', 'Model'),
            ('draft', 'Draft'),
            ('open', 'Running'),
            ('paused', 'On Hold'),
            ('close', 'Closed'),
            ('cancelled', 'Cancelled'),
           ('partial_disposed', 'Partially Disposal'),
           ('partial_sold', 'Partially Sold')],
        string='Status',
        copy=False,
        default='draft',
        readonly=True,
        help="When an asset is created, the status is 'Draft'.\n"
            "If the asset is confirmed, the status goes in 'Running' and the depreciation lines can be posted in the accounting.\n"
            "The 'On Hold' status can be set manually when you want to pause the depreciation of an asset for some time.\n"
            "You can manually close an asset when the depreciation is over.\n"
            "By cancelling an asset, all depreciation entries will be reversed")

    def partial_dispose(self):
        self.state = 'partial_disposed'
        self.x_qty -= 1

    # def dispose(self):
    #     self.state = 'disposed'
    #     self.quantity = 0 # all disposed

    def partial_sell(self):
        self.state = 'partial_sold'
        self.x_qty -= 1

    # def sell(self):
    #     self.state = 'sold'
    #     self.quantity = 0 # all sold

    @api.depends('value_residual', 'original_value', 'method_number', 'method')
    def _compute_accumulated_depreciation(self):
        for asset in self:
            years_elapsed = (datetime.today().date() - asset.acquisition_date).days / 365.25

            if asset.method == 'linear':
                depreciation_per_year = (asset.original_value - asset.value_residual) / asset.method_number
                accumulated_depreciation = depreciation_per_year * years_elapsed
                asset.x_accumulated_depreciation = min(accumulated_depreciation, asset.original_value - asset.value_residual)

            elif asset.method == 'degressive':
                depreciation_per_year = (asset.original_value - asset.value_residual) * (1 - (years_elapsed / asset.method_number))
                accumulated_depreciation = depreciation_per_year * years_elapsed
                asset.x_accumulated_depreciation = min(accumulated_depreciation, asset.original_value - asset.value_residual)

            else:
                asset.x_accumulated_depreciation = 0.0
