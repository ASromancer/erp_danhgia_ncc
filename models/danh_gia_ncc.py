from odoo import models, fields, api


class DanhGiaNCC(models.Model):
    _name = 'danh_gia_ncc'
    _description = 'Đánh giá nhà cung cấp'

    ma_phieu = fields.Char(
        string='Mã phiếu',
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('danh_gia_ncc') or 'DCNCC0001'
    )
    ten_ncc = fields.Many2one('res.partner', string='Tên nhà cung cấp')
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
    def default_get(self, fields_list):
        defaults = super(DanhGiaNCC, self).default_get(fields_list)

        tieu_chi_records = self.env['tieu_chi_dg'].search([])

        ct_danh_gia_defaults = []
        for tieu_chi in tieu_chi_records:
            ct_danh_gia_defaults.append((0, 0, {
                'tieu_chi_dg': tieu_chi.id,
                'da_duoc_dg': False,
                'diem_dg': 0.0,
            }))

        defaults['ct_danh_gia_ids'] = ct_danh_gia_defaults
        return defaults

    computed_tong_diem_cuoi_cung = fields.Float(
        string='Tổng Điểm Cuối Cùng',
        compute='_compute_tong_diem_cuoi_cung',
        store=False
    )

    round_computed_tong_diem_cuoi_cung = fields.Selection(
        selection=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
        string='Tổng Điểm Cuối Cùng',
        compute='_compute_tong_diem_cuoi_cung',
        store=False
    )

    @api.depends('ct_danh_gia_ids.diem_dg', 'ct_danh_gia_ids.da_duoc_dg')
    def _compute_tong_diem_cuoi_cung(self):
        for record in self:
            valid_ct_danh_gia = record.ct_danh_gia_ids.filtered(lambda r: r.da_duoc_dg)

            total_score = sum(float(diem) for diem in valid_ct_danh_gia.mapped('diem_dg') if diem)
            count = len(valid_ct_danh_gia)

            record.computed_tong_diem_cuoi_cung = total_score / count if count else 0
            record.round_computed_tong_diem_cuoi_cung = str(
                round(record.computed_tong_diem_cuoi_cung)) if count else '0'

    def action_draft(self):
        self.write({'trang_thai': 'draft'})
        return

    def action_submit(self):
        self.write({'trang_thai': 'waiting'})

        for record in self.ct_danh_gia_ids:
            record.danh_gia_id = self.id

        return

    def action_confirm(self):
        self.write({'trang_thai': 'confirmed'})

        for record in self:
            if record.ten_ncc:
                thong_tin_ncc = self.env['res.partner'].search([('id', '=', record.ten_ncc.id)])
                if thong_tin_ncc:
                    thong_tin_ncc.write({
                        'danh_gia_cuoi_cung': record.round_computed_tong_diem_cuoi_cung
                    })

    def action_reject(self):
        self.write({'trang_thai': 'rejected'})

    def action_cancel(self):
        self.write({'trang_thai': 'canceled'})
