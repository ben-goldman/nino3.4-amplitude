library(dplyr)
library(ncdf4)
library(zoo)

rollvar <- function(x) {
  out <- rollapply(x, width = 240, FUN = var, align = "center", fill = NA)
  return(out)
}

file_ff <- "b.e21.BOTH.f09_g17.LE2-XXXX.all.cam.h0.TREFHT.185001-210012.nc"
path_ff <- "/Volumes/Extreme SSD/DATA/stacked/CESM2/TREFHT/"

ncin <- nc_open(paste(path_ff, file_ff, sep = ""))

#nino <- ncvar_get(ncin, "TREFHT", start = c(153, 91, 1, 1), count = c(40, 11, 3012, 20))


extract_nino3.4 <- function(ncfile, xvar) {
    ncin <- nc_open(ncfile)
    out <- matrix(0, nrow = 3012, ncol = 98)
    for(t in 1:3012){
        slice <- apply(
            ncvar_get(ncin, xvar, start = c(153, 91, t, 1), count = c(40, 11, 1, -1)),
            MARGIN = 3,
            FUN = mean)
        out[t,] <- slice
        cat(paste(t, "\n"))
    }
    return(out)
}

nino <- extract_nino3.4(paste(path_ff, file_ff, sep = ""), "TREFHT")

nino_var <- apply(nino, FUN = rollvar, MARGIN = 2)

write.table(nino, file = "./data/CESM2/ff.csv", sep = ",")
