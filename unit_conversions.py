import math

class UnitConversions: 
    
    def __init__(self):
        """Call contrast axis setup as base for remaining methods
        """        
        self.contrastAxisSetup()

    def contrastAxisSetup(self, maxCdm2 = 83.174, minCdm2 = 10.0):
        """Set up the access that maps contrast to Cd/m^2

        Args:
            maxCdm2 (float, optional): Cd/m^2 at full brightness. 
            Defaults to 83.174 (HTC VIVE Pro Eye).
            minCdm2 (float, optional): Cd/m^2 at lowest brightness (40 dB).
            Defaults to 10 (HTC VIVE Pro Eye).
        """
        self.lineSlope = 1 / (maxCdm2 - minCdm2)
        self.lineIntercept = -(self.lineSlope * minCdm2)

    def dB_to_Cdm2(self, db):
    
        return ((1 / math.pi) * math.pow(10, (db / (-10)) + 4) + 10)
    

    def Cdm2_to_dB(self, cdm2):
     
        return (-10 * (math.log10(((cdm2 - 10) * math.pi)) - 4))
     

    def Cdm2_to_contrast(self, cdm2):
     
        return (self.lineSlope * cdm2 + self.lineIntercept)
     

    def contrast_to_Cdm2(self, contrast):
     
        return ((contrast - self.lineIntercept) / self.lineSlope)
     

    def dB_to_contrast(self, dB):

        return self.Cdm2_to_contrast(self.dB_to_Cdm2(dB))


    def contrast_to_dB(self, contrast):
    
        return self.Cdm2_to_dB(self.contrast_to_Cdm2(contrast))
    
