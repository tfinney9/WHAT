#
#
# UI for WHAT
#
#

library(shiny)
library(shinyjs)
library(shinythemes)
library(scatterD3)
library(shinyBS)
library(shinycssloaders)


#Deploy Paths
# vegPath<-"/home/ubuntu/hd2/src/WHAT/backend/data/surface_types.csv"
vegPath<-"/home/ubuntu/hd2/src/WHAT/backend/data/canopy_types.csv"


#Dev Paths
if(Sys.getenv("USER")[1]=="tanner")
{
  # vegPath<-"/home/tanner/src/WHAT/backend/data/surface_types.csv"
  vegPath<-"/home/tanner/src/WHAT/backend/data/canopy_types.csv"
}
vegData<-read.csv(file=vegPath)



shinyUI(fluidPage(theme=shinytheme("cosmo"),
  useShinyjs(),
  titlePanel("WHAT"),
  h3("Wind Height Adjustment Tool"),
  hr(),
  fluidRow(
    column(8,
           wellPanel(
             fluidRow(
           column(4,
           numericInput("wind_speed",label="Enter Wind Speed",value=10,min=0,max=1000),
           bsTooltip("wind_speed","Input Known Wind Speed",placement="bottom",trigger="hover")
                  ),
           column(4,
                  selectizeInput("spd_units",label="Wind Speed Units",choices=list("miles per hour (mph)"="mph",
                                                                                   "meters per second (mps)"="mps",
                                                                                   "kilometers per hour (kph)"="kph",
                                                                                   "chains per hour"="cph",
                                                                                   "furlongs per fortnight"="fpf"))
                  ),
           column(4,
                  numericInput("init_hgt",label="Wind Speed Height (AGL)",value=120,min=0,max=1000),
                  bsTooltip("init_hgt","Input Height Above Ground Level",placement = "bottom",trigger="hover")
                  )
           ),
           hr(),
           fluidRow(
           column(4,
           selectInput("surface","Select Surface/Vegetation",
                       c(Choose='',vegData[1]),selectize=TRUE,selected="Aspen")
           ),
           column(4,
                  numericInput("canopy",label="Enter Canopy Height",value=100,min=0,max=10000)
                  ),
           column(4,
                  numericInput("canopy_ratio",label="Enter Canopy Ratio",value=0.7,min=0,max=1)
           )
           ),
           hr(),
           fluidRow(
           column(8,
           numericInput("height",label="Enter Output Wind Height (Above Ground Level)",value=10,min=0,max=1000),
           bsTooltip("height","Height Above Ground Level",placement = "bottom",trigger="hover")
           ),
           column(4,
                  selectizeInput("hght_units","Height Units",choices=list("feet (ft)"="ft",
                                                                          "meters (m)"="m",
                                                                          "chain",
                                                                          "furlong"))
                  )
           ),
           hr(),
           fluidRow(
             column(12,
                    # checkboxInput("simpleCanopy","Enable Simple Canopy Model",value=TRUE)
                    radioButtons("selModel","Select Model",choices=list("Massman","Albini","Both"),
                                 selected="Massman",inline=TRUE)
                    # bsTooltip("selModel","Albini Baughman: Uses a uniform wind profile within the canopy\nTest",placement = "bottom",trigger="hover")
                    )
           ),
           br()
          ),
          actionButton("exec",label="Calculate Wind Height!",class="btn-primary"),
          br(),
          hr(),
          verbatimTextOutput("crapInputs"),
          # withSpinner(
          # verbatimTextOutput("adjustedSpeed")
          htmlOutput("adjustedSpeed")
          # )
          # uiOutput("renderVtext")

         ),
      column(4,
             # plotOutput("logWindPlot")
             h4("Wind Profile"),
             # uiOutput("renderScat")
             withSpinner(
             scatterD3Output("logWindPlot"),type=4
             )
        
      )
    
  )
  
                  )
        )
