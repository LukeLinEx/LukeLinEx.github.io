library(dplyr)
library(lubridate)
library(ggplot2)
library(DBI)
library(RSQLite)
library(zoo)
setwd(getwd())
driver = dbDriver("SQLite")


##### Randomly choose the symbol #####
### write a python script from r
### execute the script to get symbol list and
### randomly choose and write into txt
### get the txt to r, then delete txt
system('~/anaconda/bin/python random_sample.py')
symb_lst = read.csv('sample.txt', stringsAsFactors = FALSE)[,1]
system('rm sample.txt')
print(symb_lst)

col = sample(c("Close", "High", "Low", "Open", "Volume"), size = 1)

get_two = function(symb, col){
  db_file = 'goog_finance/stock_db'
  conn = dbConnect(driver, db_file)
  goog_query = paste0("SELECT Datetime FROM ", symb, " ORDER BY Datetime DESC LIMIT 1;")
  goog_last = dbGetQuery(conn, goog_query)$Datetime
  goog_last = as.Date(as.POSIXct(goog_last, origin='1970-01-01'))
  goog_last = paste0(as.character(goog_last), ' 09:30:00')
  goog_last = as.numeric(as.POSIXct(goog_last, origin='1970-01-01'))
  goog_query = paste0("SELECT * FROM ", symb, " WHERE Datetime >= ", as.character(goog_last))
  goog = dbGetQuery(conn, goog_query)
  
  db_file = 'stock_database/stock_db'
  conn = dbConnect(driver, db_file)
  yhoo = dbGetQuery(conn, goog_query)
  
  A = full_join(goog, yhoo, by="Datetime")
  A = arrange(A, Datetime)
  B = na.locf(A)
  code = paste0('g=ggplot(data=B) +geom_line(aes(seq_along(Datetime), ',col,
                '.x), color="red", alpha=0.5)+ geom_line(aes(seq_along(Datetime), ',
                col,'.y), color="blue", alpha=0.6)')

  eval(parse(text=code))
  print(g)
  return(list(goog, yhoo))
}



for(symb in symb_lst){
  get_two(symb, col)

cat ("Press [enter] to continue")
line <- readline()
}




