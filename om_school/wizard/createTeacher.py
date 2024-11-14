from sdwot import fields,models,api,_

class createTeacherWiz(models.TransientModel) :
    _name = "create.teacher.wizard"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "create teacher"
    _rec_name='name'
    
    name=fields.Many2one(comodel_name='school.student',string="Teacher name",tracking=True)  
    date_joined=fields.Date(string="date of joining")  

    @api.model
    def default_get(self,fields):
        res=super().default_get(fields)
        if self._context.get('active_id'):
            res['name']=self._context.get('active_id')
        print('res',res)
        return res

    def action_create_teacher(self):
        vals={
            #to send many2one field value use its id like many2onefilevalue.id                             
            'name':self.name.id,
            'date_joined':self.date_joined
        }
        print(vals)
        teacher_rec=self.env['school.teacher'].create(vals)
        print("new teacher created")
        return {
            'name':_("Teacher"),
            'type':'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'school.teacher',
            'res_id':teacher_rec.id,
            'target':'new'
        }

    def action_view_teacher(self):
        print('action_view_teacher')
        action=self.env.ref('om_school.teacher_action').read()[0]
        # action=self.env["ir.actions.actions"]._for_xml_id('om_school.teacher_action')
        action['domain']=[('name','=',self.name.id)]   
        action['context'] = dict(self._context, default_name=self._context.get('active_id'))
        print('action',action) 
        return action

        
    