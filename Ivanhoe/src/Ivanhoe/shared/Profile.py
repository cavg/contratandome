

class Profile():
    
    def __init__(self,user):
        self.user = user
        self.jobs       = []
        self.services   = []
        #indicators
        self.experience     = None
        self.confidence_e   = None
        self.confidence_f   = None  
        self.grade_e        = None
        self.grade_f        = None
        
        #employer
        self.employer       = None
        
        #freelancer         
        self.freelancer     = None
    
    def set_employer(self,employer):
        self.employer   = employer
        
    def set_freelancer(self,freelancer):    
        self.freelancer = freelancer
        
        
    def set_indicators(self,experience,confidence_e,confidence_f,grade_e,grade_f):
        self.experience     = experience
        self.confidence_e   = round(confidence_e,1)
        self.confidence_f   = round(confidence_f,1)
        self.grade_e        = round(grade_e,1)
        self.grade_f        = round(grade_f,1)
        
    
    #jobs type <ViewJob>, calculate indicators and set jobs as attr to itself
    def calculate_indicators(self,jobs):
        self.jobs = jobs
        try:
            experience          = 0
            confidence_e        = 0
            confidence_f        = 0        
            confidence_e_count  = 0.0
            confidence_f_count  = 0.0
            projs_finished      = 0
            projs_grade_e       = 0
            projs_grade_f       = 0
            projs_employer_score= []   
            projs_employer_days = []   
            projs_freelancer_score= []   
            projs_freelancer_days = []  
            
            for j in jobs:
                if j.state=="3":
                    projs_finished = projs_finished+1
                    experience += j.experience_days
                    projs_employer_score.append(j.score_employer)
                    projs_employer_days.append(j.experience_days)
                    projs_freelancer_score.append(j.score_freelancer)
                    projs_freelancer_days.append(j.experience_days)
                
                if j.state=="4":
                    confidence_f_count = confidence_f_count+1
                if j.state=="5":
                    confidence_e_count = confidence_e_count+1
                if j.state=="6":
                    confidence_e_count = confidence_e_count+1
                    confidence_f_count = confidence_f_count+1
                    
                #proyectos fuera de la fecha    
#                if j.rate_out_of_date_e != None:
#                    if j.rate_out_of_date_e == False:
#                        confidence_e = confidence_e + 1
#                    confidence_e_count = confidence_e_count+1
#                if j.rate_out_of_date_f != None:
#                    if j.rate_out_of_date_f == False:
#                        confidence_f = confidence_f + 1
#                    confidence_f_count = confidence_f_count+1
            
            i = 0
            try:
                for s in projs_employer_score:
                    weight = round(projs_employer_days[i]/float(experience),1)
                    projs_grade_e += (s*weight)
                    i = i+1
            except Exception,e:
                pass
            
            i = 0
            try:
                for s in projs_freelancer_score:
                    weight = round(projs_freelancer_days[i]/float(experience),1)
                    projs_grade_f += (s*weight)
                    i = i+1
            except Exception,e:
                pass
            
            try:
                #proyectos fuera de la fecha 
#                confidence_e = (confidence_e/confidence_e_count)*100 
#                confidence_f = (confidence_f/confidence_f_count)*100
                confidence_e = 10.0-(confidence_e_count/projs_finished)*10.0
                confidence_f = 10.0-(confidence_f_count/projs_finished)*10.0
            except Exception,e:
                print e
            self.experience     = experience*8
            self.confidence_e   = round(confidence_e,1)
            self.confidence_f   = round(confidence_f,1)
            self.grade_e        = round(projs_grade_e,1)
            self.grade_f        = round(projs_grade_f,1)
            
            
        except Exception,e:
            pass
        
        
        
