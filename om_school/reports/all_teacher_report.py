from sdwot import fields, models, api, _

class AllTeacherReport(models.AbstractModel):
    _name = "report.om_school.report_teacher_details"  
    _description = "All Teacher Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['school.teacher'].search_read([])  
        print('docs in parser func', docs) 
        domain=[]
        form_data=data.get('form_data')
        name=form_data.get('name')
        date_joined=form_data.get('date_joined')
        date_left=form_data.get('date_left')
        if name:
            domain+=[('name','=',name[0])]
        if date_joined:
            domain+=[('date_joined','=',date_joined)]
        if date_left:
            domain+=[('date_left','=',date_left)]        
        print(domain)    
        return {
            'docs': self.env['school.teacher'].search(domain)  
        }
