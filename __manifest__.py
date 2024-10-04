{
    'name': 'erp_danhgia_ncc',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Module sử dụng để đánh giá nhà cung cấp',
    'depends': ['base', 'mail'],
    'assets': {
        'web.assets_backend': [
            'static/src/js/priority_five_stars.js',
        ],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/tieu_chi_dg_views.xml',
        'views/danh_gia_ncc_views.xml',
        'views/thong_tin_ncc_views.xml',
        'views/ct_danh_gia_ncc_views.xml',
        'views/menu_ncc.xml',
        'data/sequence_data.xml',
    ],
    'installable': True,
    'application': True,
}
