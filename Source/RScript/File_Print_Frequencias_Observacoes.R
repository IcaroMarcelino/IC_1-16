frequencias_atributos <- function(bd){
  for(i in 1:ncol(bd)){
    x = as.data.frame(table(bd[,i]))
    
    write(paste(as.character(x[1,1]), as.character(x[1,2]), sep = "|"), file = paste(as.character(colnames(bd)[i]), "txt", sep = "_at."), append = FALSE)
    
    for(j in 2:nrow(x))
      write(paste(as.character(x[j,1]), as.character(x[j,2]), sep = "|"), file = paste(as.character(colnames(bd)[i]), "txt", sep = "_at."), append = TRUE)
    
  }
}

