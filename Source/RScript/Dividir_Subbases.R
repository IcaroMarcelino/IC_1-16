#################################################################
# Icaro Marcelino Miranda - 06/2016
# 
# 	Script para dividir uma base de dados bd em n aleatoriamente
# 
#################################################################

subbases <- function(bd, n){
  tam = floor(nrow(bd)/n)
  
  for(i in 1:n){
    if(nrow(bd) >= tam){
      ind = sample(1:nrow(bd), tam)
    }
    else{
      ind = sample(1:nrow(bd), nrow(bd))
    }
    
    sub = bd[ind, ]
    bd = bd[-ind, ]
    
    write.table(sub, file = paste("Inputs/SubBases/B", as.character(i), ".csv", sep = ""), quote = FALSE, row.names = FALSE, col.names = TRUE, sep = ";", append = FALSE, na = "NA")
  }
  
}