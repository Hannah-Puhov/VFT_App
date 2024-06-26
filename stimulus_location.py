import streamlit as st
import numpy as np
class StimulusLocation:

    def __init__(self, group, x, y, resOutput):
        self.x = x
        self.y = y
        self.group = group
        self.resOutput = resOutput

        self.logContrasts = []
        self.reversals = []
        self.responses = []
        self.reversalAverage = 0

        self.candidateFN = []
        self.numFN = 0
        self.FNMissed = 0
        self.threshold = 0

    def finalize_location(self, weibullCalc, converter):
        self.reversalAverage = np.average(self.reversals)
        self.threshold = weibullCalc.fit_weibull(self.logContrasts, self.responses)
        self.final_fn_calc(converter)
    
    def final_fn_calc(self, converter):
        for res in self.candidateFN:
            if converter.contrast_to_dB(self.threshold) > 21:
                self.numFN += 1

                if (res == "No"):
                    self.FNMissed += 1

    def add_final_csv_line(self, resultsOutput, converter):
        log_cont_string = ';'.join(map(str, self.logContrasts))
        res_string = ';'.join(map(str,self.responses))
        line = [f'{self.group}', f'{self.x}', f'{self.y}', 
                f'{log_cont_string}',
                f'{res_string}',
                f'{converter.contrast_to_dB(pow(10, self.reversalAverage)):.3f}',
                f'{converter.contrast_to_dB(self.threshold):.3f}']
        
        resultsOutput.append(line)


    

    

