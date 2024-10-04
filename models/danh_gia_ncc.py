from odoo import models, fields, api


class DanhGiaNCC(models.Model):
    _name = 'danh_gia_ncc'
    _description = 'Đánh giá nhà cung cấp'

    ma_phieu = fields.Char(
        string='Mã phiếu',
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('danh_gia_ncc') or 'DCNCC0001'
    )
    ten_ncc = fields.Many2one('thong_tin_ncc', string='Tên nhà cung cấp')
    email = fields.Char(string='Email', required=True)
    dien_thoai = fields.Integer(string='Điện thoại')
    nganh_kd = fields.Char(string='Ngành kinh doanh')
    ky_dg = fields.Date(string='Kỳ đánh giá')
    ngay_dg = fields.Date(string='Ngày đánh giá')
    quan_ly = fields.Many2one('res.users', string='Quản lý')
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('waiting', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('rejected', 'Từ chối'),
        ('canceled', 'Huỷ')
    ], default='draft', string='Trạng thái')
    ct_danh_gia_ids = fields.One2many('ct_danh_gia_ncc', 'danh_gia_id', string="Chi Tiết Đánh Giá")

    @api.model
    def create(self, vals):
        record = super(DanhGiaNCC, self).create(vals)
        tieu_chi_records = self.env['tieu_chi_dg'].search([])
        for tieu_chi in tieu_chi_records:
            self.env['ct_danh_gia_ncc'].create({
                'ct_danh_gia_ncc': record.id,
                'danh_gia_id': record.id,
                'tieu_chi_dg': tieu_chi.id,
            })
        return record

    computed_tong_diem_cuoi_cung = fields.Float(
        string='Tổng Điểm Cuối Cùng',
        compute='_compute_tong_diem_cuoi_cung',
        store=False
    )

    round_computed_tong_diem_cuoi_cung = fields.Selection(
        selection=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        string='Tổng Điểm Cuối Cùng',
        compute='_compute_tong_diem_cuoi_cuoi',
        store=False
    )

    @api.depends('ct_danh_gia_ids.diem_dg')
    def _compute_tong_diem_cuoi_cung(self):
        for record in self:
            total_score = sum(float(diem) for diem in record.ct_danh_gia_ids.mapped('diem_dg') if diem)
            count = len(record.ct_danh_gia_ids)
            record.computed_tong_diem_cuoi_cung = total_score / count if count else 0
            record.round_computed_tong_diem_cuoi_cung = str(round(total_score / count if count else 0)) if count else '0'

