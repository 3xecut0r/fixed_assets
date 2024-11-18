{
    'name': 'Fixed Asset Quantity Management',
    'version': '17.0.1.0.0',
    'summary': 'Manage multiple quantities of the same fixed asset, track disposal and sale, and generate depreciation journals',
    'category': 'Accounting',
    'description': """
        This module extends Odoo's Fixed Asset management to support:
        - Managing multiple quantities of the same fixed asset.
        - Partial disposal and partial sale of fixed assets.
        - Summarized depreciation journals generated at the end of each month.
        - Reporting on asset balances and movements.
    """,
    'author': 'Oleksii Panpukha',
    'license': 'Other proprietary',
    'website': 'https://github.com/3xecut0r',
    'depends': ['account', 'stock', 'account_asset'],
    'data': [
        'security/ir.model.access.csv',
        'data/asset_depreciation_cron.xml',
        'views/asset_depreciation.xml',
        'views/account_asset.xml',
        'reports/asset_report.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
