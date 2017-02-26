library("data.table")
library("ggmap")
library("xlsx")

# Data Taken from
# Love your Heart
# http://www.livewellsd.org/love-your-heart/
# https://cosdhhsa.maps.arcgis.com/apps/webappviewer/index.html?id=c035b1925da04284b78438d820f6005d

setwd("/Users/mgalarny/Desktop")

heartDT <- xlsx::read.xlsx("All_Data_Into_Tableau.xlsx"
                         , sheetName = "LoveYourHeart_2017"
                         , sheetIndex = 1
                         , startRow = 1)
heartDT <- data.table::as.data.table(heartDT)

heartDT[, fullAddress := (paste(Address, City, Zipcode ))]


zip2latlong <- ggmap::geocode(location = heartDT[, fullAddress], output = "more")

zip2latlong <- data.table::as.data.table(zip2latlong)

heartDT[, lon := zip2latlong[, lon]]
heartDT[, lat := zip2latlong[, lat]]

data.table::fwrite(x = heartDT, file = "SanDiegoHeart.csv")