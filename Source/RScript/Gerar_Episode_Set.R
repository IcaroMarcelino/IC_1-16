#################################################################
# Icaro Marcelino Miranda - 06/2016
# 
# 	Script para gerar um arquivo para cada instante de tempo na
# base, com os valores que as variaveis assumem.
# 
#################################################################

gerarEpisodeSet <- function(bd){
  v = (as.data.frame(table(bd[,5]))$Var1)
  
  for(i in 1:length(v)){
    n = which(bd[,5] == v[i])
    sbd = bd[n,]
    
    niveis = unique(sbd[,1])
    
    t = as.character(niveis[1])
    
    if(length(niveis) > 1){
      for(k in 2:length(niveis)){
        t = paste(t, as.character(niveis[k]), sep = "|")
      }
    }
  
    write(as.character(t), file = paste(getwd(), "/Inputs/Episodeset/", as.character(v[i]), ".txt", sep = ""), append = FALSE)
    
    for(j in 2:ncol(bd)){
      niveis = unique(sbd[,j])
      
      t = as.character(niveis[1])
      
      if(length(niveis) > 1){
        for(k in 2:length(niveis)){
          t = paste(t, as.character(niveis[k]), sep = "|")
        }
      }
      write(as.character(t), file = paste(getwd(), "/Inputs/Episodeset/", as.character(v[i]), ".txt", sep = ""), append = TRUE)
    }
  }
}