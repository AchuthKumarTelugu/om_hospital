from sdwot import fields,models,api

class SaleOrder(models.Model) :
    #to inherit this field from sale.order and add into model student
    _inherit = "sale.order"
    
    sale_description=fields.Char(string="Sale description") 
    