class courseSection:
    def __init__(self):
        self.duration = ""
        self.section = ""
        self.format = ""
        self.zeroTextbookCost = False
        self.time = []
        self.prof = ""
        self.currSeatCount = 0
        self.tuition = 0
        self.sectionNote = ""
        self.semester = ""
        self.registration = ""
    def __init__(self, semester, duration, section, format, zeroTextbookCost, time, prof, currSeatCount, tuition, registration, sectionNote):
        self.duration = duration
        self.section = section
        self.format = format
        self.zeroTextbookCost = zeroTextbookCost
        self.time = time
        self.prof = prof
        self.currSeatCount = currSeatCount
        self.tuition = tuition
        self.sectionNote = sectionNote
        self.semester = semester
        self.registration = registration
    def printAll(self):
        print("Semester:",self.semester)
        print("Duration:",self.duration)
        print("Section:",self.section)
        print("Format:",self.format)
        print("ZeroTextbookCost:",self.zeroTextbookCost)
        if len(self.time) > 0:
            print("Time:")
            for t in self.time:
                print(t)
        print("Professor:",self.prof)
        print("Current Seat Count:",self.currSeatCount)
        print("Tuition:",self.tuition)
        print("Registration:",self.registration)
        print("Section Note:",self.sectionNote)