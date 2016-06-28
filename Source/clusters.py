import HVDM
import GA_clustering as GAC
import csv

print("Lendo informacoes da base...")
atributos = HVDM.lerAtributos()
centroides_I = GAC.lerBase("Inputs/CentroidesI.csv")
centroides_R = GAC.lerBase("Inputs/CentroidesR.csv")
centroides_S = GAC.lerBase("Inputs/CentroidesS.csv")
bd = GAC.lerBase("Inputs/bd_mortais.csv")

print("Encontrando indices dos centroides...")
indices_I = []
indices_R = []
indices_S = []
for centroide in centroides_I:
	indices_I.append(bd.index(centroide))

for centroide in centroides_R:
	indices_R.append(bd.index(centroide))

for centroide in centroides_S:
	indices_S.append(bd.index(centroide))

print("Preparando centroides...")
flags_I =[]
flags_R =[]
flags_S =[]
for i in list(range(0, len(bd))):
	if i in indices_I:
		flags_I.append(1)
	else:
		flags_I.append(0)

	if i in indices_R:
		flags_R.append(1)
	else:
		flags_R.append(0)

	if i in indices_S:
		flags_S.append(1)
	else:
		flags_S.append(0)

print("Gerando clusters...")
print("Classe Intermediario")
cI, dI, clusters_I = GAC.gerarClusters(flags_I, bd, atributos)

for i in range(0, len(clusters_I)):
	with open("Outputs/Cluster_I_" + str(i) + ".csv", 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
		writer.writerows(clusters_I[i])
		csvfile.close()

print("Classe Resistente")
cR, dR, clusters_R = GAC.gerarClusters(flags_R, bd, atributos)

for i in range(0, len(clusters_R)):
	with open("Outputs/Cluster_R_" + str(i) + ".csv", 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
		writer.writerows(clusters_R[i])
		csvfile.close()

print("Classe Sensivel")
cS, dS, clusters_S = GAC.gerarClusters(flags_S, bd, atributos)

for i in range(0, len(clusters_S)):
	with open("Outputs/Cluster_S_" + str(i) + ".csv", 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
		writer.writerows(clusters_S[i])
		csvfile.close()
