library("data.table")
library("ggmap")
library("xlsx")

setwd("C:/Users/mgalarnyk/Desktop")

sdZip <- xlsx::read.xlsx("All_Data_Into_Tableau.xlsx"
                                , sheetIndex = 1
                                , startRow = 1)

sdZip <- data.table::as.data.table(sdZip)

sdZip[, zipcode := lapply(.SD, as.character), .SDcols = c("zipcode")]

zip2latlong <- ggmap::geocode(location = sdZip[, zipcode], output = "more")

zip2latlong <- data.table::as.data.table(zip2latlong)

sdZip[, lon := zip2latlong[, lon]]
sdZip[, lat := zip2latlong[, lat]]

data.table::fwrite(x = sdZip, file = "SanDiegoZipLonLat.csv")
