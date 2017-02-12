server <- function(input, output, session) {
  observeEvent(input$mydata, {
    data = input$mydata
    print(data)
    len = length(input$mydata)
    # output$tables <- renderUI({
    #   table_list <- lapply(1:len, function(i) {
    #     tableName <- names(input$mydata)[[i]]
    #     tableOutput(tableName)
    #   })
    #   do.call(tagList, table_list)
    # })
    for (name in names(input$mydata)) {
      output[[name]] <- renderTable(read.csv(text=input$mydata[[name]]))
    }
  })
}