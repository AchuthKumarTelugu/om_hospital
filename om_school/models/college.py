from sdwot import fields,models,api
from sdwot.addons.om_college.models.student import CollegeStudent as college

class CollegeStudentInherit(models.Model) :
    #to inherit this field from sale.order and add into model student
    _inherit = "college.student"

    def unlink(self):
        print('unlink function of college is overrided from school module')
        res=super(college,self).unlink()
        return res
    
    
