
library(ncdf4)

rollvar <- function(x) {
  out <- rollapply(x, width = 240, FUN = var, align = "center", fill = NA)
  return(out)
}

file_ff <- "b.e21.BOTH.f09_g17.LE2-XXXX.all.cam.h0.TREFHT.185001-210012.nc"
path_ff <- "/Volumes/Extreme SSD/DATA/stacked/CESM2/TREFHT/"

ncin <- nc_open(paste(path_ff, file_ff, sep = ""))

nino <- ncvar_get(ncin, "TREFHT", start = c(153, 91, 1, 1), count = c(1, 1, -1, -1))

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
