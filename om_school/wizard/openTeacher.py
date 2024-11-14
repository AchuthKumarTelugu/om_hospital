from sdwot import fields,models,api,_

class openTeacherWiz(models.TransientModel) :
    _name = "open.teacher.wizard"
    _description = "open teacher"
    # _rec_name='name'
    
    name=fields.Many2one(comodel_name='school.student',string="Teacher name",tracking=True)  
    date_joined=fields.Date(string="date of joining")  
    date_left=fields.Date(string="left school at")

    def open_teachers(self):
        domain=[]
        name_id=self.name
        if name_id:
            domain=[('name','=',name_id.id)]
        if self.date_joined:
            domain+=[('date_joined','>=',self.date_joined)]
        if self.date_left:
            domain+=[('date_left','<=',self.date_left)]        
        print("domain",domain)    

        teachers=self.env['school.teacher'].search_read(domain)
        print(teachers)
        data={
            'form_data':self.read()[0],
            'teachers':teachers
        }
        return self.env.ref('om_school.report_open_teacher_details').report_action(self,data)


    

        
    