from odoo import models, fields, api

class CrmInformation(models.Model):

    _inherit = 'crm.lead'

    business_developer = fields.Char(string="Business Developer",required=True)
    account_manager = fields.Char(string="Account Manager",required=True)
    cuisine = fields.Many2many('cuisine.custom',string='Cuisine')
    working_hours = fields.Float(string="Working Hours")
    grid_id = fields.Char(string="Grid ID")
    status = fields.Char(string="Status")
    reason = fields.Char(string="Reason")
    establishment_date = fields.Date()
    email = fields.Char(string="Email",required=True)
    partner_name = fields.Char("Customer Name",required=True)
    contact_role = fields.Char(string="Contact For",required=True)
    accountable_for = fields.Many2many('crm.accounts.custom', string='Accountable for')
    id_number = fields.Char("Passport / ID Number")
    age = fields.Char(string="Age")
    extension = fields.Char(string="Extension")
    address_type = fields.Many2many('address.types',string="Address Type", required=True)
    address1 = fields.Char("Address")
    address2 = fields.Char("Address Line 2")
    region = fields.Char(string="Region")
    country = fields.Many2one(string="Country",comodel_name='res.country')
    city = fields.Char(string="City")
    area = fields.Char(string="Area")
    landmark = fields.Char(string="Landmark")
    google_link = fields.Char(string="Google Link")
    latitude = fields.Char(string="Latitude")
    longitude = fields.Char(string="Longitude")
    customer_name = fields.Char(string="Customer Name")
    quote_expiry = fields.Date(string="Quote Expiry")
    quote_owner = fields.Char(string="Quote Owner")
    add_product = fields.Many2many('products.custom',string="Add Product")
    terms = fields.Text("Terms and Conditions")
    crno = fields.Char(string="CR Number")
    cr_number = fields.Binary(string="CR File")
    vatno = fields.Char("VAT Number")
    vat_number = fields.Binary("VAT File")
    csa = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='CSA')
    csa_file = fields.Binary("CSA File")
    cr_name = fields.Char(string="CR Name")
    payment_type = fields.Char(string="Payment Type")
    payment_terms = fields.Char(string="Payment Terms")
    credit_limit = fields.Char(string="Credit Limit")
    attachments = fields.Binary(string='Attachments')
    bank_name = fields.Char(string="Bank Name")
    idc = fields.Char(string="Swift Code/IDC")
    account_name = fields.Char(string="Account Name")
    account_number = fields.Char(string="Account Number")
    iban = fields.Char(string="IBAN")

class AccountableFor(models.Model):

    _name = 'crm.accounts.custom'

    name = fields.Char(String="Accountable")

class AddressTypes(models.Model):

    _name = 'address.types'

    name = fields.Char(String="Address Type")

class AddProducts(models.Model):

    _name = 'products.custom'

    name = fields.Char(string="Add Products")

class CuisineCustom(models.Model):

    _name = 'cuisine.custom'

    name = fields.Char(String="Cuisine")

