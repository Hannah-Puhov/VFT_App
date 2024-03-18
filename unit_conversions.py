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
        """Convert Humphrey decibels to Cd/m^2

        Args:
            db (float): Brightness in Humphrey decibels

        Returns:
            float: Brightness in Cd/m^2
        """    
        return ((1 / math.pi) * math.pow(10, (db / (-10)) + 4) + 10)
    

    def Cdm2_to_dB(self, cdm2):
        """Convert Cd/m^2 into Humphrey decibels

        Args:
            cdm2 (float): Brightness in Cd/m^2

        Returns:
            float: Brightness in Humphrey dB
        """     
        return (-10 * (math.log10(((cdm2 - 10) * math.pi)) - 4))
     

    def Cdm2_to_contrast(self, cdm2):
        """Convert Cd/m^2 into contrast units

        Args:
            cdm2 (float): Brightness in Cd/m^2

        Returns:
            float: A contrast level (0-1), with 1 being 
                the highest brightness
        """     
        return (self.lineSlope * cdm2 + self.lineIntercept)
     

    def contrast_to_Cdm2(self, contrast):
        """Convert contrast units into Cd/m^2

        Args:
            contrast (float): A contrast level (0-1), with 1 being
                the highest brightness

        Returns:
            float: Brightness in Cd/m^2
        """     
        return ((contrast - self.lineIntercept) / self.lineSlope)
     

    def dB_to_contrast(self, dB):
        """Convert Humphrey decibles to contrast units

        Args:
            dB (float): Brightness in Humphrey dB

        Returns:
            float: A contrast level (0-1), with 1 being
                the highest brightness
        """
        return self.Cdm2_to_contrast(self.dB_to_Cdm2(dB))


    def contrast_to_dB(self, contrast):
        """Convert contrast units to Humphrey decibels

        Args:
            contrast (float): A contrast level (0-1), with 1 being
                the highest brightness

        Returns:
            float: Brightness in Humphrey dB
        """    
        return self.Cdm2_to_dB(self.contrast_to_Cdm2(contrast))
    
