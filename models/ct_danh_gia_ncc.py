from email.policy import default

from odoo import models, fields

class CTDanhGiaNCC(models.Model):
    _name = 'ct_danh_gia_ncc'
    _description = 'Chi tiết đánh giá nhà cung cấp'

    ct_danh_gia_ncc = fields.Many2one('danh_gia_ncc', string='Chi tiết đánh giá nhà cung cấp')
    tieu_chi_dg = fields.Many2one('tieu_chi_dg', string='Tiêu chí đánh giá')
    da_duoc_dg = fields.Boolean(string='Đã được đánh giá', default=True)
    diem_dg = fields.Selection([
        ('0', '0 sao'),
        ('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao')
    ], default='0', string="Điểm đánh giá")
    tong_diem_cuoi_cung = fields.Float(string='Tổng điểm cuối cùng')
    kq_danh_gia = fields.Selection([
        ('0', '0 sao'),
        ('1', '1 sao'),
        ('2', '2 sao'),
        ('3', '3 sao'),
        ('4', '4 sao'),
        ('5', '5 sao')
    ], default='0', string="Kết quả đánh giá")
    thong_tin_phan_hoi = fields.Text(string='Thông tin phản hồi')
    danh_gia_id = fields.Many2one('danh_gia_ncc', string="Đánh Giá Nhà Cung Cấp", ondelete='cascade')
