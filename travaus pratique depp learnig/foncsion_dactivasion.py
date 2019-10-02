import math as mt


def sigmoide(z):
	acti = []
	for entre in z:
		a = 1.0/(1.0+mt.exp(-entre))
		acti.append(a)
	return acti
def sigmoide_printe(z):
	self.sigmoide(z)*(1-self.sigmoide(z)