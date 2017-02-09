source('helper.R')

shinyServer(function(input, output){
  
  output$img <- renderUI({
    HTML(paste0("<img src=", input$url, " height=200 weight=300>"))
  })
  
  
  
  output$prob <- renderTable({
    download.file(input$url, 'img.jpeg', mode = 'wb')
    file = 'img.jpeg'
    system(paste0('python test.py ', file))
    a = read.csv('result.txt',header=FALSE, sep='?')
    system('rm result.txt')
    system('rm img.jpeg')
    a
  })

})