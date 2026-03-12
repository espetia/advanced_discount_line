{
    'name': 'Advanced Discount Line',
    'version': '15.0.1.0',
    'category': 'Sales',
    'summary': 'Validaciones avanzadas para la configuración de descuentos en líneas de venta.',
    'author': 'Carlos Espetia',
    'depends': ['sale_management'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/discount_line_configuration_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
