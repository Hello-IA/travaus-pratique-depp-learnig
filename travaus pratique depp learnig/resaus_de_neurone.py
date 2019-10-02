import random as rn
import math as mt
import numpy as np 
import copy
class reseau():
	def __init__(self):
		
		self.fonction_dactivasion = []
		self.pois_w = []
		self.bier_b = []
		self.inisialisation_premier = True
		self.nerone_size = []
	def add(self, nerone, fonction, couche_dantre = 0):
		self.fonction_dactivasion.append(fonction)
		if self.inisialisation_premier:
			if couche_dantre != 0:
				self.couche_dantre = couche_dantre
			self.inisialisatuer(nerone, couche_dantre, self.pois_w)
			self.inisialisation_premier = False
		else:
			self.inisialisatuer(nerone, self.nerone_size[-1], self.pois_w)
		self.inisialisatuer(couche1 = nerone, couche2 = 1, listeBW = self.bier_b)
		self.nerone_size.append(nerone)
	def inisialisatuer(self, couche1, couche2, listeBW):
		couche_list = []

		for l in range(couche1):
			inise = []
			for j in range(couche2):
				nonbreBW = rn.uniform(-0.3, 0.3)
				if listeBW == self.pois_w:
					inise.append(nonbreBW)
				else:
					couche_list.append(nonbreBW)
			if listeBW == self.pois_w:
				couche_list.append(inise)
		listeBW.append(couche_list)

	def inisialisatuer_zero(self, couche1, couche2, listeBW, desente_de_lereur_w):
		couche_list = []

		for l in range(couche1):
			inise = []
			for j in range(couche2):
				nonbreBW = 0
				if listeBW == desente_de_lereur_w:
					inise.append(nonbreBW)
				else:
					couche_list.append(nonbreBW)
			if listeBW == desente_de_lereur_w:
				couche_list.append(inise)
		listeBW.append(couche_list)
	def fit(self, entre_x, sorti_y, batch_size = 1, epochs = 100):
		
		data_entréne = [(x, y) for x, y in zip(entre_x, sorti_y)]
		taie_x = len(data_entréne)
		for epc in range(epochs):
			rn.shuffle(data_entréne)
			list_batchs = [data_entréne[z:z+batch_size] for z in range(0, taie_x, batch_size)]
			for list_batch in list_batchs:
				self.mise_a_jour_du_resaus(list_batch, self.taus_darpentisage)
			print(epc)

	def mise_a_jour_du_resaus(self, dataxy, eta):
		desente_de_lereur_w = []
		desente_de_lereur_b = [] 

		nerone_size_shape = len(self.nerone_size)
		for nss in range(nerone_size_shape):
			if desente_de_lereur_w == [] and desente_de_lereur_b == []:
				self.inisialisatuer_zero(self.nerone_size[nss], self.couche_dantre, desente_de_lereur_w, desente_de_lereur_w)
			else:
				self.inisialisatuer_zero(self.nerone_size[nss], self.nerone_size[nss-1], desente_de_lereur_w, desente_de_lereur_w)
			self.inisialisatuer_zero(self.nerone_size[nss], 1, desente_de_lereur_b, desente_de_lereur_w)
		refe_delta_b = copy.deepcopy(desente_de_lereur_b)
		refe_delta_w = copy.deepcopy(desente_de_lereur_w)
		for x, y in dataxy:
			delta_b = copy.deepcopy(refe_delta_b)
			delta_w = copy.deepcopy(refe_delta_w)
			
			delta_desente_b, delta_desente_w = self.retroPropagasion(x, y, delta_w, delta_b)
			#print(delta_desente_b)
			for i, desenteb in enumerate(desente_de_lereur_b):
				desb = []
				for indexb, ds in enumerate(desenteb):
					new_vercte_b = desente_de_lereur_b[i][indexb]+delta_desente_b[i][indexb]
					desb.append(new_vercte_b)
				desente_de_lereur_b[i] = desb
			for i, desentew in enumerate(desente_de_lereur_w):
				desw = []
				for indexw, ds in enumerate(desentew):
					dew = []
					for indw, d in enumerate(ds):
						new_vercte_w = desente_de_lereur_w[i][indexw][indw]+delta_desente_w[i][indexw][indw]
						dew.append(new_vercte_w)
					desw.append(dew)
				desente_de_lereur_w[i] = desw
			delta_b = copy.deepcopy(refe_delta_b)
			delta_w = copy.deepcopy(refe_delta_w)

		for i, (w_couche, ereur_couche_w) in enumerate(zip(self.pois_w, desente_de_lereur_w)):
			couchew = []
			for w_nerone, ereur_nerone_w in zip(w_couche, ereur_couche_w):
				neronew = []
				for w_sinapse, w_ereur in zip(w_nerone, ereur_nerone_w):
					unit_sinapse_w = w_sinapse-(eta/len(dataxy))*w_ereur
					neronew.append(unit_sinapse_w)
				couchew.append(neronew)
			self.pois_w[i] = couchew
		for i, (b_chouche, ereur_couche_b) in enumerate(zip(self.bier_b, desente_de_lereur_b)):
			coucheb = []
			for b_nerone, ereur_nerone_b in zip(b_chouche, ereur_couche_b):
				unit_nerone_b = b_nerone-(eta/len(dataxy))*ereur_nerone_b
				coucheb.append(unit_nerone_b)
			self.bier_b[i] = coucheb 
					





	def retroPropagasion(self, x, y, list_w, list_b):
		
		x1 = x.tolist()
		x1 = [float(xa) for xa in x1]
		activasion = x1
		activasions = [x1]
		
		zs = []

		for e, (w, b) in enumerate(zip(self.pois_w, self.bier_b)):
			z = []
			a = []
			for intreireu_w, interireu_b in zip(w,b):
				mmini_z = 0
				for i, ner in enumerate(intreireu_w):
					mmini_z +=  ner*activasion[i]
				mmini_z += interireu_b
				acti_unite = self.forncionActivastion(e, mmini_z)
				a.append(acti_unite)
				z.append(mmini_z)
			zs.append(z)
			activasion = a
			activasions.append(a)

		nabla_b, nabla_w = self.fonctionDeCous(zs, activasions, list_w, list_b, y)
		return nabla_b, nabla_w

	def fonctionDeCous(self, list_z, list_acti, list_w, list_b, y):
		#print("------------------")
		if self.optimisation == "SGD":
			return self.retoSGD(list_z, list_acti, list_w, list_b, y)



	def retoSGD(self, zs, activasions, list_w, list_b, y):
		exisent_foncsion = {"sigmoide": False, "rampe": False, "heaviside": False, "tangente_hyperbolique": False, "arc_tangente": False, "signe":False, "ReLU": False, "PReLU": False, "ELU": False, "SoftPlus": False, "Identité_courbée": False, "soft_exponential": False, "Sinusoïde": False, "Sinc": False, "Gaussienne": False}
		tablau_liste_foncsions = {}
		for i, fonc in enumerate(self.fonction_dactivasion):
			index = -(i+1)
			#print(index)
			if exisent_foncsion[fonc] == True:
				list_b[index] = tablau_liste_foncsions[fonc][0][index]
				#print("list_b:", list_b)
				#print("_____")
				#print("tablau_liste_foncsions_b:", tablau_liste_foncsions[fonc][0])
				list_w[index] = tablau_liste_foncsions[fonc][1][index]
			else:
				for j in range(len(self.fonction_dactivasion)):
					iindex = -(j+1)
					if iindex == -1:
						if len(activasions[-1]) == 1:
							cost = activasions[-1]-y
						else:
							cost = [(a -ynuiq) for a, ynuiq in zip(activasions[-1], y)]
						delta = [(cos*self.fonctionDeDerivasion(-1 ,prit)) for cos, prit in zip(cost, zs[-1])]
						w_delta = []
						for d in delta:
							mini_delta_w = []
							for ac in activasions[-2]:
								resulte = d*ac
								mini_delta_w.append(resulte)  
							w_delta.append(mini_delta_w)
						tablau_liste_foncsions[fonc] = [[delta], [w_delta]]
						if index == -1:
							list_b[-1] = delta
							list_w[-1] = w_delta 
					else:
						#print(iindex,"-----------",index)
						z_list = zs[iindex]
						sp = [self.fonctionDeDerivasion(index, z) for z in z_list]
						couche_retro = self.pois_w[iindex+1]
						w_transpose = []
						iindex1 = iindex+1
						for ji, ii in enumerate(couche_retro[0][:]):
							list_retro = []
							for cr, w in enumerate(couche_retro):
								list_retro.append(couche_retro[cr][ji])
							w_transpose.append(list_retro)
						for w, trans in enumerate(w_transpose):
							transpose = [(tr*delt) for tr, delt in zip(trans, delta)]
							w_transpose[w] = transpose
							w_unite = 0
							for d in w_transpose[w]:
								w_unite += d
							w_transpose[w] = w_unite
						delta = [(wtr*s) for wtr, s in zip(w_transpose, sp)]
						tablau_liste_foncsions[fonc][0].insert(0, delta)
						#print(tablau_liste_foncsions["sigmoide"][0])
						w_delta = []
						for d in delta:
							mini_delta_w = []
							for ac in activasions[iindex-1]:
								resulte = d*ac
								mini_delta_w.append(resulte)
							w_delta.append(mini_delta_w)
						tablau_liste_foncsions[fonc][1].insert(0, w_delta)
						itereb = len(list_b[index])
						
						if index == iindex:
							list_b[index] = [delta for itb in range(itereb)]
							#print(list_b)
							list_w[index] = w_delta
				exisent_foncsion[fonc] = True
		#print("list_b:", list_b)
		return list_b, list_w
					

	def compile(self, optimisation = "SGD", taus_darpentisage = 0.1):
		self.optimisation = optimisation
		self.taus_darpentisage = taus_darpentisage




	def sigmoide(self, z):
		a = 1.0/(1.0+mt.exp(-z))
		return a
		

	def sigmoide_printe(self, z):
		a = self.sigmoide(z)*(1-self.sigmoide(z))
		return a

	def fonctionDeDerivasion(self, index, z):
		if self.fonction_dactivasion[index] == "sigmoide":
			return self.sigmoide_printe(z)


	def forncionActivastion(self, index, z):
		if self.fonction_dactivasion[index] == "sigmoide":
			a = 1.0/(1.0+mt.exp(-z))
			return a
    def predict(self, data_teste, seuie = None):
        pass

	def predict(self, data_teste, seuie = None):
        resulte = []
		taie_data = len(data_teste)
		tete_vair = 0
		for x_teste in data_teste:
			copyx_teste = copy.deepcopy(x_teste)
			for e, (w_couche, b_chouche) in enumerate(zip(self.pois_w, self.bier_b)):
				activasions = []
				for nerone_w, nerone_b in zip(w_couche, b_chouche):
					mmini_z = 0
					for i, intreireu_w in enumerate(nerone_w):
						mmini_z += intreireu_w*x_teste[i]
					mmini_z += nerone_b
					acti = self.forncionActivastion(e, mmini_z)
					activasions.append(acti)
					copyx_teste = activasions
			if len(copyx_teste) == 1:
				copyx_teste = copyx_teste[0]
				if seuie == int():
					copyx_teste = (copyx_teste > seuie)
			minresulte = copyx_teste
			
			resulte.append(copyx_teste)
		return resulte
		

	def prousentage(self, y_test, y_prede):
		taie_data = len(y_test)
		predicton_vair0 = 0
		predicton_vair1 = 0
		predicton_fause1 = 0
		predicton_fause0 = 0
        for yt, yp in zip(y_test, y_prede):
            if yt = 1 and yp = True:
                predicton_vair1 += 1
		print("predicton_vair0", predicton_vair0)
		print("predicton_vair1", predicton_vair1)
		print("predicton_fause1", predicton_fause1)
		print("predicton_fause0", predicton_fause0)
		print("-----------")
		print((predicton_vair1+predicton_vair0)/taie_data)
