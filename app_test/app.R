library(shiny)
library(quantmod)


ui <- basicPage(
  plotOutput("plot1", brush = "plot_brush"),#click = "plot_click"),
  h4("Dataset"),
  fluidRow(
    column(6, 
           helpText("Specify the symbol, date range and the basic plot style."),
           br(),
           textInput("symb", "Symbol", "SPY"),
           dateRangeInput("dates", label=h5("Date range"),
                          start = "2016-03-01", end =   as.character(Sys.Date()))
    ),
    column(6, 
           actionButton("collect", "COLLECT"),
           actionButton("save", "SAVE"),
           verbatimTextOutput("info"),
           tableOutput("Table")
)))

server <- function(input, output) {
  
  my_value <- reactiveValues(df = data.frame(begin=format(as.Date(0), '%Y-%m-%d'),
                                             end = format(as.Date(0), '%Y-%m-%d')))
  
  dataInput <- reactive({
    setwd('~/Desktop/sp500/')
    load('sp500_data.RData')
    data = XOM[2228:nrow(XOM),]
    # symb = input$symb
    # from = input$dates[1]
    # to   = input$dates[2]
    result=list()
    # data = getSymbols(symb, src = "yahoo", 
    #                   from = from,
    #                   to = to,
    #                   auto.assign = FALSE)
    # 
    result$data    = data
    return(result)
  }) 
  
  output$plot1 <- renderPlot({
    plot(mtcars$wt, mtcars$mpg)
    
    data  = dataInput()$data
    chartSeries(data, theme = chartTheme('white'), type = 'line', TA=NULL)
    addLines(v=c(10,100), col = 'red')
    #addLines(v=100, col = 'red')
  })
  
  output$info <- renderText({
    begin = floor(input$plot_brush$xmin)
    end_  = floor(input$plot_brush$xmax)
    data_date = index(dataInput()$data)
    paste0("begin=", data_date[begin], "\nend=", data_date[end_],
           "\nrange=", as.character(end_ - begin))
  })
  
  observeEvent(input$collect, {
    begin = floor(input$plot_brush$xmin)
    end_  = floor(input$plot_brush$xmax)
    data_date = index(dataInput()$data)
    begin = format(data_date[begin], '%Y-%m-%d')
    end_ = format(data_date[end_], '%Y-%m-%d')
    #begin = data_date[begin]
    #end_ =  data_date[end_]
    my_value$df <- rbind(my_value$df, data.frame(begin, end = end_))
  })
  
  #observe({
  #  print(my_value$df)
  #})
  
  output$Table <- renderTable(my_value$df)
  
  observeEvent(input$save, {
    write.table(my_value$df[-1,], file = 'test.csv', col.names = F, row.names = F, append = T, sep = ",")
    my_value$df = data.frame(begin=format(as.Date(0), '%Y-%m-%d'),
                             end = format(as.Date(0), '%Y-%m-%d'))
  })
}
  

shinyApp(ui, server)