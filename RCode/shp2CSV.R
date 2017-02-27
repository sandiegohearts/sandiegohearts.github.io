library("data.table")
library("ggmap")
library("maptools")

# Code based on 
# https://journal.r-project.org/archive/2013-1/kahle-wickham.pdf

# Code returns S4 Class
setwd("~/Desktop/2017-Team-203/Data/Zip_CodesShapeFiles")
shapefile <- readShapeSpatial('ZIP_CODES.shp')

names(shapefile)
# [1] "ZIP"        "COMMUNITY"  "SHAPE_AREA" "SHAPE_LEN" 

zipDT <- data.table(zipcode = shapefile$ZIP
                    , community = shapefile$COMMUNITY)

data.table::fwrite(x = zipDT, file = "SanDiegoZipCodes.csv")