import math

class WeibullCalculator:

    def __init__(self):
        """Set up initial parameters for the Weibull functions
        """   

        #Lambda (scale) parameters     
        self.minL0 = -3
        self.maxL0 = 0
        self.inc = 0.0001

        #K (shape) parameters
        self.mink = 2
        self.maxk = 2.5
        self.inck = 0.1

        self.set_params()

    def set_params(self):
        """Set up lists to iterate through 
        """    

        #List of possible Lambda values (including Lambda^10)    
        self.numElementsLambda = (int) ((self.maxL0 - self.minL0) / (self.inc + 1))
        self.Lambda = []
        self.Lambda_10 = []
        for i in range(self.numElementsLambda):
            self.Lambda.append(self.minL0 + i * self.inc)
            self.Lambda_10.append(math.pow(10, self.Lambda[i]))

        #List of possible k values
        self.numelementsK = (int) ((self.maxk - self.mink) / (self.inck + 1))
        self.kList = []
        for i in range(self.numelementsK):
            self.kList.append(self.mink + i * self.inck)

    
    def weibull(self, x, k, l, g=0):
        """Calculate the Weibull distribution function

        Args:
            x (array): Values for evaluation
            k (float): Shape parameter
            l (float): Scale parameter
            g (int, optional): Location parameter. Defaults to 0.

        Returns:
            array: Values of the Weibull distribution function evaluated
                at each point in x
        """        
        to_ret = []

        for val in x:
            ret = g + (1 - g) * (1 - math.exp(-1 * math.pow(val / l, k)))
            to_ret.append(ret)
        
        return to_ret
    
    def fit_weibull(self, responses, logContrasts):
        """Fit a Weibull function to find the true threshold of 
            sensitivity for a givem location given the log contrasts and the 
            responses at each stimulus time. 

        Args:
            responses (array): Array of yes/no responses
            logContrasts (array): log of 0-1 contrast units representing 
                stimulus brightness at each trial

        Returns:
            float: Weibull threshold in contrast units
        """   
        #Lists to store contrasts at positive/negative responses     
        CRx = []
        CRx_10 = []

        IRx = []
        IRx_10 = []

        #Initialization
        optLambda = self.Lambda[0]
        LL0 = -math.inf

        #Separate responses into seen / not seen
        for i in range(len(responses)):
            if responses[i] == "Yes":
                CRx.append(logContrasts[i])
                CRx_10.append(math.pow(10, logContrasts))
            
            else:
                IRx.append(logContrasts[i])
                IRx_10.append(math.pow(10, logContrasts))

        #Loop through possible shape and scale parameters to find the optimum
        for l in range(self.numElementsLambda):
            for k in range(self.numelementsK):
                
                #Calculate Weibull values for positive and negative responses
                CR = self.weibull(CRx_10, self.kList[k], self.Lambda[l])
                IR = self.weibull(IRx_10, self.kList[k], self.Lambda[l])

                #Calculate log-likelihood
                LL = 0
                for val in CR:
                    LL += math.log(val)

                for val in IR:
                    LL += math.log(1 - val)
                
                #Update optimal lambda
                if (LL > LL0):
                    optLambda = self.Lambda[l]
                    LL0 = LL
    
        #Return the Weibull threshold
        return math.pow(10, optLambda)

