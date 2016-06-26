suporteVariaveis <- function(bd){
  v = (as.data.frame(table(bd[,5]))$Var1)
  f = (as.data.frame(table(bd[,5]))$Freq)
  
  for(i in 1:length(v)){
    n = which(bd[,5] == v[i])
    
    sbd = bd[n,]
    
    niveis = unique(sbd[,1])
    
    m = which(sbd[,1] == niveis[1])
    
    t = paste(niveis[1], as.character(round(length(m)/length(n), 4)), sep = ",")
    
    if(length(niveis) > 1){
      for(k in 2:length(niveis)){
        m = which(sbd[,1] == niveis[k])
        
        t = paste(t, paste(as.character(niveis[k]), as.character(round(length(m)/length(n), 4)), sep = ","), sep = "|")
      }
    }
    
    write(as.character(t), file = paste(getwd(),"/Inputs/Suporte/supp_", as.character(v[i]), ".txt", sep = ""), append = FALSE)
    
    for(j in 2:ncol(bd)){
      niveis = unique(sbd[,j])
      m = which(sbd[,j] == niveis[1])
      
      t = paste(niveis[1], as.character(round(length(m)/length(n), 4)), sep = ",")
      
      if(length(niveis) > 1){
        for(k in 2:length(niveis)){
          m = which(sbd[,j] == niveis[k])
          
          t = paste(t, paste(as.character(niveis[k]), as.character(round(length(m)/length(n), 4)), sep = ","), sep = "|")
        }
      }
      write(as.character(t), file = paste(getwd(),"/Inputs/Suporte/supp_", as.character(v[i]), ".txt", sep = ""), append = TRUE)
    }
  }
  
}