import math

class WeibullCalculator:

    def __init__(self):
        self.minL0 = -3
        self.maxL0 = 0
        self.inc = 0.0001

        self.mink = 2
        self.maxk = 2.5
        self.inck = 0.1

        self.set_params()

    def set_params(self):
        self.numElementsLambda = (int) ((self.maxL0 - self.minL0) / (self.inc + 1))
        self.numelementsK = (int) ((self.maxk - self.mink) / (self.inck + 1))

        self.Lambda = []
        self.Lambda_10 = []
        for i in range(self.numElementsLambda):
            self.Lambda.append(self.minL0 + i * self.inc)
            self.Lambda_10.append(math.pow(10, self.Lambda[i]))

        self.kList = []
        for i in range(self.numelementsK):
            self.kList.append(self.mink + i * self.inck)

    
    def weibull(self, x, k, l, g=0):
        to_ret = []

        for val in x:
            ret = g + (1 - g) * (1 - math.exp(-1 * math.pow(val / l, k)))
            to_ret.append(ret)
        
        return to_ret
    
    def fit_weibull(self, responses, logContrasts):
        CRx = []
        CRx_10 = []

        IRx = []
        IRx_10 = []

        optLambda = self.Lambda[0]

        LL0 = -math.inf

        for i in range(len(responses)):
            if responses[i] == "Yes":
                CRx.append(logContrasts[i])
                CRx_10.append(math.pow(10, logContrasts))
            
            else:
                IRx.append(logContrasts[i])
                IRx_10.append(math.pow(10, logContrasts))

        for l in range(self.numElementsLambda):
            for k in range(self.numelementsK):

                CR = self.weibull(CRx_10, self.kList[k], self.Lambda[l])
                IR = self.weibull(IRx_10, self.kList[k], self.Lambda[l])

                LL = 0

                for val in CR:
                    LL += math.log(val)

                for val in IR:
                    LL += math.log(1 - val)
                
                if (LL > LL0):
                    optLambda = self.Lambda[l]
                    LL0 = LL
    

        return math.pow(10, optLambda)

