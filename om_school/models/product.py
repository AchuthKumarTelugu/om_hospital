from sdwot import fields,models,api

class ProductTemplate(models.Model) :
    #to inherit this field from sale.order and add into model student
    _inherit = "res.partner"
    l10n_in_gst_treatment=fields.Selection(selection_add=[('test','Test'),('consumer',)],ondelete={'test':'cascade'})
    # l10n_in_gst_treatment=fields.Selection(selection_add=[('test','Test'),('consumer',)],ondelete={'test':''})
    