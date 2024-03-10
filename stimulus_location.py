class StimulusLocation:

    def __init__(self, group, x, y, resFile):
        self.x = x
        self.y = y
        self.group = group
        self.resFile = resFile

        self.logContrasts = []
        self.reversals = []
        self.responses = []
        self.reversalAverage = 0

        self.candidateFN = []
        self.numFN = 0
        self.FNMissed = 0
        self.threshold = 0

    def finalize_location(self, weibullCalc, converter):
        self.reversalAverage = sum(self.reversals)

        weibullCalc.fit_weibull(self.logcontrasts, self.responses)
        self.final_fn_calc(converter)
    
    def final_fn_calc(self, converter):
        for res in self.candidateFN:
            if converter.contrast_to_dB(self.thresold) > 21:
                self.numFN += 1

                if (res == "No"):
                    self.FNMissed += 1

    

