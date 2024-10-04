from odoo import models, fields

class TieuChiDG(models.Model):
    _name = 'tieu_chi_dg'
    _description = 'Tiêu chí đánh giá'

    ma_tc = fields.Char(string='Mã tiêu chí', required=True)
    ten_tc = fields.Char(string='Tên tiêu chí', required=True)
