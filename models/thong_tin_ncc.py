from odoo import models, fields

class ThongTinNCC(models.Model):
    _description = 'Thông tin nhà cung cấp'
    _inherit = 'res.partner'

    danh_gia_cuoi_cung = fields.Selection([
        ('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao')
    ], string='Đánh giá cuối cùng')

    danh_gia_moi = fields.Char(string='Đánh giá mới')
