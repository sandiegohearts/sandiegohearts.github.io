library("data.table")
library("ggmap")

hospitalDT <- data.table::data.table(hospitals = c('Alvarado Hospital'
                                                   ,'Sharp Coronado Hospital and Healthcare Center'
                                                   ,'Sharp Memorial Hospital'
                                                   , 'Fallbrook Hospital District'
                                                   ,'Grossmont Hospital'
                                                   ,'Kaiser Foundation Hospital San Diego'
                                                   ,'Scripps Mercy Hospital'
                                                   , 'Palomar Health Downtown Campus'
                                                   ,'Paradise Valley Hospital'
                                                   , 'Sharp Chula Vista Medical Center'
                                                   ,'Scripps Memorial Hospital La Jolla'
                                                   ,'Tri-City Medical Center Oceanside'
                                                   ,'UC San Diego Medical Center'
                                                   , 'Pomerado Hospital'
                                                   ,'Scripps Green Hospital'
                                                   ,'Scripps Memorial Hospital Encinitas'
                                                   ,'UC San Diego Health System Hillcrest Medical Center'))

hospitalZip <- ggmap::geocode(location = hospitalDT[["hospitals"]], output = "more")

hospitalZip <- data.table(hospitalZip)

hospitalZip[, hospitals := hospitalDT[["hospitals"]]]

hospitalZip <- hospitalZip[, .(hospitals, postal_code, lon, lat, address)]

data.table::fwrite(x = hospitalZip,  file = "hospitalZip.csv")
