from sdwot import fields,models,api,_

class SchoolSports_student(models.Model) :
    _name = "school.sports_student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "sports students"
    _rec_name="sport_name"
    _order='id desc'
    
    sport_name=fields.Char(string="Name of sport",required=True,tracking=True)
    #for sequencial id
    sport_reference=fields.Char(string="sport reference",required=True,copy=False,readonly=True,default=lambda self:('New'))
    age=fields.Integer(string="Age",tracking=True)
    state=fields.Selection([('draft','Draft'),('confirm','Confirmed'),('done','Done'),
                                              ('cancel','Cancelled')],default='draft',string='status',tracking=True) 
    student_id = fields.Many2one(comodel_name='school.student',string="id of student",tracking=True) 
    #image field
    image=fields.Binary(string="student image")
    note=fields.Text(string="description",tracking=True)
    
    def action_confirm(self):
      self.state='confirm'     
    def action_draft(self):
      self.state='draft'
    def action_done(self):
      self.state='done'         
    def action_cancel(self):
      self.state='cancel'     

    # overriding create method  
    @api.model_create_multi
    def create(self, values):
      print("values ",values)
      valuesObj=values[0]
      if not (values[0]['note']):
        values[0]['note']='new sport student created'
      if values[0].get('sport_reference',('New'))==('New'):
        values[0]['sport_reference']=self.env['ir.sequence'].next_by_code('school.sports_student') or ('New')
      returnValue=super().create(values)
      print("return value",returnValue)
      
      return returnValue

      #overriding default_get which returns all default field values
      @api.model
      def default_get(self,fields):
        res=super(SchoolSports_student, self).default_get(fields)
        print('all fields ---->',fields)
        print('all default fields---:>',res)
        res['age']=50
        res['note']="default field for note"
        return res
       
                                 