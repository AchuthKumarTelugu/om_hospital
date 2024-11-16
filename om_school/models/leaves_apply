from sdwot import fields,models,api,_
from sdwot.exceptions import ValidationError
class LeavesApply(models.Model) :
    _name = "school.leaves"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "school leaves"
    # _rec_name="name"
    _order='id desc'

    name=fields.Char(string="name for leave")
    leaves_taken_by_id = fields.Many2one("school.student",string="student name for leaves")
    approved_by_id = fields.Many2one("school.teacher",string="approved by which teacher")
    applied_date = fields.Date(string="leaves applied on")
    date_for_leaves = fields.Date(string="date for leaves")
    leaves_count = fields.Integer(string="how many leaves want ?")  
   
