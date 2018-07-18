class Student(object):
    def __init__(self, name, score): 
        self.name = name
        self.score = score

    def print_score(self):
        print("{self.name}'s score is: {self.score}".format(self=self))        # Python 2.7 + .format优化写法
        
    def compare(self,s):
        if self.score>s:
            print("better than %d" %(s))
        elif self.score==s:
            print("equal %d" %(s))
        else:
            print("lower than %d" %(s))

May = Student("May",90)        
Peter = Student("Peter",85)        

May.print_score()
Peter.print_score()

May.compare(100)
May.compare(90)
May.compare(89)