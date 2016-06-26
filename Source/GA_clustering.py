#############################################################
# Icaro Marcelino Miranda - 06/2016
#
# Python 3.X
# Clustering usando Algoritmos Geneticos
# 
# 	O tamanho do cromossomo e o numero de pontos na base,
# cada gene pode assumir o valor 0 ou 1, indicando se o 
# ponto de mesmo indice na base sera um centroide ou nao.
# 	A funcao fitness maximiza o inverso da distancia media
# dos pontos dos clusters, num calculo de similaridade.
# 	A distancia entre dois pontos e calculado pela metrica
# HVDM.
# 
# 	Para inciar o programa, utilizar a funcao
# 
# ga_clustering(NGEN, NPOP, PBCX, PBMT, BASE, INDICE)
# 
# 	Onde BASE e a lista que contem os dados (utilizar
# a funcao lerBase) e INDICE e o numero dessa base
# (Nesse caso, a base original foi dividida em 1000,
# INDICE e o valor ordinal da base que esta sendo 
# analisada).
# 
# Para inciar o programa de maneira simplificada,
# compilar o arquivo iniciar_cluster.py
############################################################

from deap import base
from deap import creator
from deap import tools
import random
import HVDM
import time
import csv

def lerBase(nome_arquivo):
	bd = open(nome_arquivo, 'r').readlines()

	i = 0
	for linha in bd:
		bd[i] = linha.split(';')

		ncol = len(bd[i])-1

		bd[i][ncol] = bd[i][ncol].split("\n")
		bd[i][ncol] = bd[i][ncol][0]

		i += 1

	bd.pop(0)

	return bd

def inicializarCromossomo(base):
	tam = len(base)
	nc = int(tam**.5)

	# n = random.randint(int(nc/2), nc)
	n = random.randint(1, nc)

	indices = list(range(0, tam))
	indices = random.sample(indices, n)

	cromossomo = []
	for i in range(0, tam):
		if i in indices:
			cromossomo.append(1)
		else:
			cromossomo.append(0)

	return cromossomo

def gerarClusters(cromossomo, base, atributos):
	centroides = []
	clusters = []
	distancias = []
	if len(cromossomo) == 1:
		cromossomo = cromossomo[0]

	if sum(cromossomo) == 0:
		return [], [], []

	for i in range(0, len(cromossomo)):
		if cromossomo[i] == 1:
			ind1 = int(i/4)
			centroides.append(base[ind1])
			clusters.append([])
			distancias.append([])

	for elem in base:
		flag = -1
		d = 1e30
		i = 0
		for centroide in centroides:
			if elem != centroide:
				dist = HVDM.HVDM(atributos, base, base.index(elem), base.index(centroide))
			
				if(dist < d):
					d = dist
					flag = i

				i += 1

		clusters[flag].append(elem)
		distancias[flag].append(d)

	while 0 in distancias:
		centroides.remove(centroides[distancias.index([0])])
		distancias.remove([0])

	while [] in distancias:
		centroides.remove(centroides[distancias.index([])])
		distancias.remove([])

	return centroides, distancias, clusters

def similaridade(distancias):
	med = sum(distancias)/len(distancias)
	sm2 = sum(x*x for x in distancias)
	std = abs(sm2/sum(distancias) - med**2)**0.5

	return std

def fitness(cromossomo, base, atributos):
	if len(cromossomo) == 1:
		cromossomo = cromossomo[0]
	n_clusters = sum(cromossomo)

	if n_clusters < 1:
	# if n_clusters < 2:
	 	return 0,

	if n_clusters > int(len(base)**.5):
		return 0,

	centroides, distancias, clusters = gerarClusters(cromossomo, base, atributos)
	simi = []
	for j in range(0, len(centroides)):
		temp = []
		
		for i in range(0, len(centroides)):
			if i != j:
				if(distancias[i] != [0])&(len(distancias) > 0):
					if(centroides[i] != centroides[j]):
						d = HVDM.HVDM(atributos, base, base.index(centroides[i]), base.index(centroides[j]))
						r = similaridade(distancias[i]) + similaridade(distancias[j])
						temp.append(r/d)
					else:
						temp.append(99999999999999)

		if len(temp) == 0:
			return 0,

		simi.append(max(temp))

	DB = sum(simi)/sum(cromossomo)

	fit = 1/DB
	return fit, 

#################################################
# Funcionamento do algoritmo genetico proposto: #
#                                               #
# a) Codificacao do cromossomo:                 #
#   O cromossomo possui tamanho igual ao numero #
# de observacoes na base de dados. Cada gene    #
# pode assumir o valor 1 ou 0, indicando se o   #
# ponto representa ou não um centroide,         #
# respectivamente.                              #
#                                               #
# b) Avaliação do cromossomo (função fitness):  #
#   A função fitness maximiza a similaridade    #
# interna de cada cluster e a distancia entre   #
# dois clusters diferentes. Esse mecanismo      #
# utiliza como metrica de distancia, por a base #
# possuir dados nominais, a distância HVDM.     #
#                                               #
#################################################
def ga_clustering(ngen, npop, pbcx, pbmt, bd, n):
	print("---- Inicio GA (", n, ") ----")
	start_time = time.time()

	saida = open("Fitness_B" + str(n) + ".csv", 'w')
	atributos = HVDM.lerAtributos()

	toolbox = base.Toolbox()

	creator.create("Fitness", base.Fitness, weights = (1.0,))
	creator.create("Individuo", list, fitness = creator.Fitness)

	toolbox.register("inicializarCromossomo", inicializarCromossomo, base = bd)
	toolbox.register("individuo", tools.initRepeat, creator.Individuo, toolbox.inicializarCromossomo, 1)
	toolbox.register("population", tools.initRepeat, list, toolbox.individuo)

	toolbox.register("avaliar", fitness, base = bd, atributos = atributos)
	toolbox.register("cruzamento", tools.cxTwoPoint)
	toolbox.register("mutacao", tools.mutFlipBit, indpb = 0.15)
	toolbox.register("selecao", tools.selTournament, tournsize = 5)

	pop = toolbox.population(n = npop)

	fitnesses = list(map(toolbox.avaliar, pop))
	for ind, fit in zip(pop, fitnesses):
		ind.fitness.values = fit

	for g in range(ngen):
		gen_time = time.time()
		print("\n-- Geracao %i --" % g)

		offspring = toolbox.selecao(pop, len(pop))
		offspring = list(map(toolbox.clone, offspring))

		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < pbcx:
				toolbox.cruzamento(child1[0], child2[0])
				del child1.fitness.values
				del child2.fitness.values

		for mutant in offspring:
			if random.random() < pbmt:
				toolbox.mutacao(mutant[0])
				del mutant.fitness.values

			if random.random() < 3*pbmt:
				random.shuffle(mutant[0])
				del mutant.fitness.values

		invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
		fitnesses = map(toolbox.avaliar, invalid_ind)
		for ind, fit in zip(invalid_ind, fitnesses):
			ind.fitness.values = fit

			if fit[0] == 0:
				ind[0] = inicializarCromossomo(bd)

		pop[:] = tools.selBest(offspring + tools.selBest(pop, 1), len(pop))
		# pop[:] = offspring

		fits = [ind.fitness.values[0] for ind in pop]
		
		length = len(pop)
		mean = sum(fits) / length
		# sum2 = sum(x*x for x in fits)
		# std = abs(sum2 / length - mean**2)**0.5
		
		print("  Fitness Maximo: ", round(max(fits), 2))   # Valor minimo.
		print("  Fitness Medio : ", round(mean, 2))        # Valor medio.
		# print("  Std: ", round(std, 2))         # Desvio padrao da geracao.
		# print("  Tempo gasto (geracao): ", int(time.time() - gen_time))
		# print("  Tempo gasto (total): ", int(time.time() - start_time))
		saida.write(str(g) + ";" + str(round(mean, 4)) + ";" + str(round(max(fits), 4)) + "\n")

	saida.close()

	centroides, distancias, clusters = gerarClusters(tools.selBest(pop, 1)[0], bd, atributos)

	with open("Outputs/Centroides_B" + str(n) + ".csv", 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
		writer.writerows(centroides)
		csvfile.close()

	with open("Outputs/Total_centroides.csv", 'a') as csvfile:
		writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
		writer.writerows(centroides)
		csvfile.close()

	for cluster in clusters:
		for linha in cluster:
			if "" in linha:
				linha.remove("")
				print(linha)
		if [] in cluster:
			cluster.remove([])

	if [] in clusters:
		clusters.remove([])

	for i in range(0, len(clusters)):
		with open("Outputs/Cluster_" + "B" + str(n) + "_" + str(i) + ".csv", 'w') as csvfile:
			writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
			writer.writerows(clusters[i])
			csvfile.close()

	print("--- %s segundos ---" % int(time.time() - start_time))
##############################################################################################################