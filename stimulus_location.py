class StimulusLocation:

    def __init__(self, group, x, y, resFile):
        self.x = x
        self.y = y
        self.group = group
        self.resFile = resFile

    def finalize_location(self):
        self.reversalAverage = sum(self.reversals)

        

    

