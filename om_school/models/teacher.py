from sdwot import fields,models,api,_

class SchoolTeacher(models.Model) :
    _name = "school.teacher"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "school teacher"
    _rec_name='name'
    
    # name=fields.Char(string="Name",required=True,tracking=True)
    name=fields.Many2one(comodel_name='school.student',string="Teacher",tracking=True)  
    teacher_name=fields.Many2one(comodel_name='school.student',string="Teacher name",tracking=True)  
    teacher_reference=fields.Char(string="Teacher reference",required=True,copy=False,readonly=True,default=lambda self:('New'))
    
    note=fields.Text(string="description",tracking=True)
    state=fields.Selection([('draft','Draft'),('confirm','Confirmed'),('done','Done'),
                                              ('cancel','Cancelled')],default='draft',string='status',tracking=True) 

    # role_id = fields.Many2one(comodel_name='res.partner',string="role of teacher",tracking=True)  
    age=fields.Integer(string="Age",tracking=True,related='name.age')
    date_joined=fields.Date(string="date of joining")
    date_left=fields.Date(string="date of left school")    
    gender=fields.Selection([
      ('male','Male'),
      ('female','Female'),
      ('other','Other'),
    ],tracking=True) 
    

    def action_confirm(self):
      for rec in self:
        rec.state='confirm'
    def action_draft(self):
       for rec in self:
        rec.state='draft'
    def action_done(self):
      for rec in self:
        rec.state='done'       
    def action_cancel(self):
       for rec in self:
        rec.state='cancel'

    def copy(self,default=None) :
      if default is None:
        default={}
      default['note']=("%s (copy)"%self.note)
      res=super().copy(default)
      return res          

    # overriding create method  
    @api.model_create_multi
    def create(self, values):
      print("values ",values)
      valuesObj=values[0]
      # if not (values[0]['note']):
      #   values[0]['note']='new teacher joined'
      if values[0].get('teacher_reference',('New'))==('New'):
        values[0]['teacher_reference']=self.env['ir.sequence'].next_by_code('school.teacher') or ('New')
      returnValue=super().create(values)
      print("return value",returnValue)
      
      return returnValue
    # triggering on change event for name field  
    @api.onchange('name')
    # @api.onchange('name','gender') onchange for multiple fields
    def onchange_name(self):
      print("onchange triggered")    
      if self.name:
        if self.name.gender:
          self.gender=self.name.gender   
      else:
        self.gender=''

    