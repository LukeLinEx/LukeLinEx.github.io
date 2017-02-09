library(shiny)

shinyUI(
  navbarPage("Auto Grader Editor", id="nav",
             
             tabPanel('Read the Problem', 
                      basicPage(
                        h4("Problem 1"),br(),
                        fluidRow(
                          column(5, textInput('url', 'Please enter the url of the image:', 
                                              'https://s3-us-west-2.amazonaws.com/tfrwemeetup/red_wine.jpg')),
                          column(12, uiOutput("img"), br()
                            ),
                          column(12, tableOutput('prob'))
                          )
                        )
                      )
))







