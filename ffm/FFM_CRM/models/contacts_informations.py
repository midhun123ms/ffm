from odoo import models, fields, api


class ContactInformations(models.Model):
    _inherit = 'res.partner'

    customer_geo_location = fields.Char(string="Name")
    address_type = fields.Many2many('contact.address.types', string="Address Type")
    address_line1 = fields.Char("Address")
    address2 = fields.Char("Address Line 2")
    region = fields.Char(string="Region")
    country = fields.Many2one(string="Country", comodel_name='res.country')
    city = fields.Char(string="City")
    area = fields.Char(string="Area")
    landmark = fields.Char(string="Landmark")
    google_link = fields.Char(string="Google Link")
    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")
    customer_name = fields.Char(string="Customer Name")
    quote_expiry = fields.Date(string="Quote Expiry")
    quote_owner = fields.Char(string="Quote Owner")
    add_product = fields.Many2many('contact.products.custom', string="Add Product")
    terms = fields.Text("Terms and Conditions")
    cr_no = fields.Integer(string="CR NO", size=10)
    vat_no = fields.Integer("VAT NO", size=15)
    csa = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='CSA')
    payment_type = fields.Selection([('credit', 'Credit'), ('cash', 'Cash'), ('installment', 'Installment')], string='Payment Type')
    payment_terms = fields.Selection([('immediate', 'Immediate'), ('15', '15'), ('30', '30'), ('45', '45'), ('60', '60')], string='Payment Terms')
    credit_limit = fields.Integer(string="Credit Limit")
    bank_name = fields.Char(string="Bank Name")
    idc = fields.Char(string="Swift Code/IDC")
    account_name = fields.Char(string="Account Name")
    account_number = fields.Char(string="Account Number")
    iban = fields.Char(string="IBAN")
    # is_customerss = fields.Boolean(string="Is Customer")
    # location_latitude = fields.Float(string="Latitude")
    # location_longitude = fields.Float(string="Longitude")
    region = fields.Char()
    business_developer = fields.Char(string="Business Developer")
    cr_name = fields.Char(string="CR Name")
    grid_id = fields.Char(string="GRID ID")
    # status = fields.Char(string="Status")
    reason = fields.Char(string="Reason")
    created_on = fields.Date(string="Created On", default=lambda self: fields.Date.today())
    status = fields.Selection(
        [('active', 'Active'),
         ('inactive', 'In Active'),
         ('Churned', 'Churned'),
         ('physically_closed', 'Physically Closed'), ('terminated', 'Terminated'), ('lawyer_case', 'Lawyer Case')],
        'Status',)

    @api.model
    def create(self, vals):
        res = super(ContactInformations, self).create(vals)
        if vals['is_company']:
            res.active = False
        email_template = self.env.ref('FFM_CRM.contacts_archive_mail').with_context(dbname=self._cr.dbname)
        email_template.send_mail(self.id, notif_layout='mail.mail_notification_light', force_send=False)
        return res

    @api.model
    def _geo_localize(self,street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(street=street, zip=zip, city=city, state=state, country=country)
        result = geo_obj.geo_find(search, force_country=country)
        print(result)
        if result is None:
            search = geo_obj.geo_query_address(city=city, state=state, country=country)
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        # We need country names in English below
        for partner in self.with_context(lang='en_US'):
            result = self._geo_localize(partner.street,
                                        partner.zip,
                                        partner.city,
                                        partner.state_id.name,
                                        partner.country_id.name)

            if result:
                partner.write({
                    'partner_latitude': result[0],
                    'partner_longitude': result[1],
                    'date_localization': fields.Date.context_today(partner)
                })
            return result

    # @api.model
    # def google_map_link(self, zoom=10):
    #     params = {'q': '%s,%s'%(self.longitude,self.latitude),'z': zoom,}
    #     return params

class ContatctAddressTypes(models.Model):

    _name = 'contact.address.types'

    name = fields.Char(String="Address Type")

class AddProducts(models.Model):

    _name = 'contact.products.custom'

    name = fields.Char(string="Add Products")
