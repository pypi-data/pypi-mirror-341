class course:
    def __init__(self):
        self.cvc_id = ""
        self.college_name = ""
        self.class_name = ""
        self.class_symbol = ""
        self.C_ID = ""
        self.course_description = ""
        self.location = ""
        self.units = 0
        self.unitType = ""
        self.prereqs = []
        self.sections = []
    def __init__(self,cvc_id,college_name,class_name,class_symbol,C_ID,course_description,location, units,unitType, prereqs,sections):
        self.cvc_id = cvc_id
        self.college_name = college_name
        self.class_name = class_name
        self.class_symbol = class_symbol
        self.C_ID = C_ID
        self.course_description = course_description
        self.location = location
        self.units = units
        self.unitType = unitType
        self.prereqs = prereqs
        self.sections = sections
    def printAll(self, sections = True):
        print("CVC ID:",self.cvc_id)
        print("College Name:",self.college_name)
        print("Class Name:",self.class_name)
        print("Class Symbol:",self.class_symbol)
        if self.C_ID != "":
            print("C-ID:",self.C_ID)
        print("Location:",self.location)
        print("Units:",self.units)
        if self.unitType != "":
            print("Unit Type:",self.unitType)
        if self.course_description != "":
            print("Course Description:",self.course_description)

        if len(self.prereqs) > 0:
            print("Prerequisites:")
        for prereq in self.prereqs:
            print(prereq)
        if sections:
            for section in self.sections:
                section.printAll()