library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)

rollvar <- function(x) {
  out <- rollapply(x, width = 240, FUN = var, align = "center", fill = NA)
  return(out)
}


se <- function(x, ...) sqrt(var(x, ...)/length(x))

extract_nino3.4 <- function(ncfile, xvar) {
  ncin <- nc_open(ncfile)
  out <- apply(
    ncvar_get(ncin, xvar, start = c(153, 91, 1, 1), count = c(40, 11, -1, -1)),
    MARGIN = c(3, 4),
    FUN = mean
  )
  return(out)
  nc_close(ncin)
}

path_ff <- "/Volumes/Extreme\ SSD/DATA/stacked/CESM1/TREFHT/"
path_sf <- "/Volumes/Extreme\ SSD/DATA/stacked/CESM1SF/TREFHT/"

file_ff <- "b.e11.BRCP85C5CNBDRD.f09_g16.all.cam.h0.TREFHT.192001-210012.nc"


files_sf <- c("b.e11.B20TRLENS_RCP85.f09_g16.xghg.all.cam.h0.TREFHT.192001-208012.nc",
              "b.e11.B20TRLENS_RCP85.f09_g16.xaer.all.cam.h0.TREFHT.192001-208012.nc",
              "b.e11.B20TRLENS_RCP85.f09_g16.xbmb.all.cam.h0.TREFHT.192001-202912.nc",
              "b.e11.B20TRLENS_RCP85.f09_g16.xlulc.all.cam.h0.TREFHT.192001-202912.nc")

ff_var <- extract_nino3.4(paste(path_ff, file_ff, sep = ""), "TREFHT") %>%
  apply(2, rollvar)
write.table(ff_var, file = "ff_var.csv", sep = ",")

ghg_var <- extract_nino3.4(paste(path_sf, files_sf[1], sep = ""), "TREFHT") %>%
    apply(2, rollvar) %>%
    rbind(matrix(data=NA, nrow = (2172-1932), ncol = 20))
write.table(ghg_var, file = "ghg_var.csv", sep = ",")

aer_var <- extract_nino3.4(paste(path_sf, files_sf[2], sep = ""), "TREFHT") %>%
  apply(2, rollvar) %>%
  rbind(matrix(data = NA, nrow = (2172-1932), ncol = 20))
write.table(aer_var, file = "aer_var.csv", sep = ",")

bmb_var <- extract_nino3.4(paste(path_sf, files_sf[3], sep = ""), "TREFHT") %>%
  apply(2, rollvar) %>%
  rbind(matrix(data = NA, nrow = (2172-1320), ncol = 15))
write.table(bmb_var, file = "bmb_var.csv", sep = ",")

luc_var <- extract_nino3.4(paste(path_sf, files_sf[4], sep = ""), "TREFHT") %>%
  apply(2, rollvar) %>%
  rbind(matrix(data = NA, nrow = (2172-1320), ncol = 5))
write.table(luc_var, file = "luc_var.csv", sep = ",")

ncin <- nc_open("/Volumes/Extreme SSD/DATA/stacked/CESM1/TREFHT/b.e11.BRCP85C5CNBDRD.f09_g16.001.cam.h0.TREFHT.192001-210012.nc")
mydate <- as.Date(as.character(ncvar_get(ncin, "date")), "%Y%m%d")
write.table(mydate, file = "mydate.csv", sep = ",")

ff_raw <- extract_nino3.4(paste(path_ff, file_ff, sep = ""), "TREFHT")
write.table(ff_raw, file = "ff_raw.csv", sep = ",")
