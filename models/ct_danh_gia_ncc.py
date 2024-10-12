from odoo import models, fields, api


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

    @api.onchange('diem_dg')
    def _onchange_diem_dg(self):
        for record in self:
            if record.diem_dg:
                record.da_duoc_dg = True
            else:
                record.da_duoc_dg = False