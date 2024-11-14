from sdwot import fields,models,api,_
from sdwot.exceptions import ValidationError
class SchoolStudent(models.Model) :
    _name = "school.student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "school student"
    # _rec_name="name"
    _order='id desc'
      
    name=fields.Char(string="Name",required=True,tracking=True)
    doctor_name=fields.Many2one('college.student',string="Doctor name")
    student_reference=fields.Char(string="Student reference",required=True,copy=False,readonly=True,default=lambda self:('New'))
    age=fields.Integer(string="Age",tracking=True,copy=False)
    gender=fields.Selection([
      ('male','Male'),
      ('female','Female'),
      ('other','Other'),
    ],required=True,default='male',tracking=True)
    note=fields.Text(string="description",tracking=True)
    student_remarks=fields.Text(string="student remarks",tracking=True)
    #One2many
    student_remarks_line_ids=fields.One2many('student.remarks.line','student_id',string='student remarks line')

    state=fields.Selection([('draft','Draft'),('confirm','Confirmed'),('done','Done'),
                                              ('cancel','Cancelled')],default='draft',string='status',tracking=True) 

    guardian_id = fields.Many2one(comodel_name='res.partner',string="Guardian of student",tracking=True) 
    date_joined=fields.Date(string="date of joining")     
    teacher_count=fields.Integer(string="Teachers count",tracking=True,compute="compute_teacher_count")
    #image field 
    image=fields.Binary(string="student image")
    related_teacher_ids=fields.One2many('school.teacher','name',string='Related teachers')
    active=fields.Boolean(string="Active",default=True)

    @api.model
    def open_create_teacher(self):
        action=self.env.ref('om_school.action_create_teacher').read()[0]
        action['context']=dict(self.env.context)
        return action      

    def compute_teacher_count(self):
      #counting how many times this student became teacher,no of teachers created for this student
      #to avoid singleton error
      for rec in self:
        rec.teacher_count=self.env['school.teacher'].search_count([('name','=',rec.name)])

    def action_confirm(self):
      for rec in self:
        rec.state="confirm"
    def action_draft(self):
      self.state='draft'
    def action_done(self):
      self.state='done'         
    def action_cancel(self):
      self.state='cancel'     
    def action_url(self):
      return {
        'type':'ir.actions.act_url',
        'target':'new',
        'url':'https://erp.sdwot.ai/web#action=834&model=slide.channel&view_type=kanban&cids=1&menu_id=594'
      }  

   

    def _compute_display_name(self):
      for rec in self:
        if rec.env.context.get('hide_code'):
          rec.display_name=f"{rec.name}"
        else:
          rec.display_name=f"[{rec.student_reference}] {rec.name}"
      print(rec.display_name)    
    def open_teachers(self):
      action=self.env.ref('om_school.teacher_action').read()[0]
      action['domain']=[('name','=',self.name)] 
      return action  

    # overriding create method  
    @api.model_create_multi
    def create(self, values):
      print("values ",values)
      valuesObj=values[0]
      if not (values[0]['note']):
        values[0]['note']='new patient created'
      if values[0].get('student_reference',('New'))==('New'):
        values[0]['student_reference']=self.env['ir.sequence'].next_by_code('school.student') or ('New')
      returnValue=super().create(values)
      print("return value",returnValue)
      return returnValue

    #overriding (delete)unlink function
    def unlink(self):
      for rec in self:
            if rec.state=='done':
              raise ValidationError("you cant delete %s" % rec.name)
            return super().unlink()    
 
    #overriding default_get which returns all default field values
    @api.model
    def default_get(self,fields):
      res=super(SchoolStudent, self).default_get(fields)
      print('all fields ---->',fields)
      print('all default fields---:>',res)
      # res['age']=50
      res['note']="default field for note"
      return res
    
    #overriding copy function
    def copy(self,default=None): 
      print('copy function is overrided')
      if default is None:
        default={}
      # default['name']=_("%s (Copy)",self.name)  
      default['note']="copied record"
      # if default.get('name'):
      #   print('name',default['name'])
      #   default['name']=  _("%s (Copy)",self.name)  
      print('default',default)  
      return super(SchoolStudent,self).copy(default)  

    @api.constrains('name')
    def change_name(self):
      #to avoid singleton
      for rec in self:
        #avoiding duplicate name
          searchRes=self.env['school.student'].search([('name','=',rec.name),('id','=',rec.id)])
          if searchRes:
            raise ValidationError("no duplication constrain:name %s is already present"%rec.name)   

    # @api.model
    # def name_get(self): #name_get is deprecated in odoo 17
    #   #using name_get func,we are combining our name with reference,when its choosen for many to one in another model
    #   result=[]
    #   for rec in self:
    #     name=rec.student_reference+""+rec.name
    #     result.append((rec.id,name)) 
    #   return result         
  

class studentRemarksLine(models.Model):
  _name="student.remarks.line"
  _description="school student remarks line"

  sport=fields.Char(string='name of sport')
  hours_played=fields.Integer(string='No of hours played')
  student_id=fields.Many2one('school.student',string='student id')                        