library(shiny)

ui <- shinyUI(
  fluidPage(
    tags$head(tags$link(rel="stylesheet", href="css/styles.css", type="text/css"),
              tags$script(src="getdata.js")),
    sidebarLayout(
      sidebarPanel(
        h3(id="data-title", "Drop Datasets"),
        div(class="col-xs-12", id="drop-area", ondragover="dragOver(event)", 
            ondrop="dropData(event)")
      ),
      mainPanel(
        uiOutput('tables')
      )
    )
    
  )
)