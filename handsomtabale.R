library(shiny)
library(rhandsontable)

shinyApp(
  shinyUI(
    fluidRow(
      rHandsontableOutput("hot")
    )),
  
  shinyServer(function(input, output, session) {
    values = reactiveValues()
    
    data = reactive({
      if (!is.null(input$hot)) {
        DF = hot_to_r(input$hot);print(1)
      } else {
        if (is.null(values[["DF"]])){
          DF = iris
          print(2)
        }else
          DF = values[["DF"]]; print(3)
      }
      
      
      values[["DF"]] = DF
      DF
    })
    
    output$hot <- renderRHandsontable({
      DF = data()
      if (!is.null(DF))
        rhandsontable(DF, stretchH = "all")
    })
  })
)