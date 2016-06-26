import GA_clustering as g
import GA_temporal as t

def run_cluster(NGEN, NPOP, PBCX, PBMT, indices_bases):
	for i in indices_bases:
		bd = g.lerBase("Inputs/Centroides" + str(i) + ".csv")
		g.ga_clustering(NGEN, NPOP, PBCX, PBMT, bd, i)

def run_temporal(NGEN, NPOP, PBCX, PBMT, indices_exec):
	for i in indices_exec:
		t.ga_temporal(NGEN, NPOP, PBCX, PBMT, i)

# run_cluster(100, 100, .7, .15, list(range(857,925)))
run_temporal(50, 100, .8, .15, list(range(336,351)))
# run_cluster(100, 50, .7, .15, ["I"])
