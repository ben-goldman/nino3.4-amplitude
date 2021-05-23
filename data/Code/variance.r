library(zoo)
library(ncdf4)
library(ggplot2)
library(dplyr)
library(gridExtra)
library(grid)
library(boot)




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


ncin <- nc_open("/Volumes/Extreme SSD/CESM/CESM1/CESM1/TREFHT/b.e11.BOTH.f09_g16.ensemble.cam.h0.TREFHT.192001-210012.nc")
date <- as.Date(ncvar_get(ncin, "time"), origin = "1920-01-01")
date <- seq(1920, 2100, length.out = 2172)

path_ff <- "/Volumes/Extreme\ SSD/CESM/CESM1/CESM1/TREFHT/"
path_sf <- "/Volumes/Extreme\ SSD/CESM/CESM1/CESM1SF/TREFHT/"

file_ff <- "b.e11.BOTH.f09_g16.ensemble.cam.h0.TREFHT.192001-210012.nc"
files_sf <- c(
  "b.e11.B20TRLENS_RCP85.f09_g16.xghg.ensemble.cam.h0.TREFHT.192001-208012.nc",
  "b.e11.B20TRLENS_RCP85.f09_g16.xaer.ensemble.cam.h0.TREFHT.192001-208012.nc",
  "b.e11.B20TRLENS_RCP85.f09_g16.xbmb.ensemble.cam.h0.TREFHT.192001-202912.nc",
  "b.e11.B20TRLENS_RCP85.f09_g16.xlulc.ensemble.cam.h0.TREFHT.192001-202912.nc",
  "b.e11.B20LE_fixedO3_ensemble.cam.h0.TREFHT.195501-200512.nc"
  )
path_ctl <- "/Volumes/Extreme SSD/CESM/CESM1/CTL1850/TREFHT"
file_ctl <- "b.e11.B1850C5CN.f09_g16.005.cam.h0.TREFHT.040001-220012.nc"


ff_var <- extract_nino3.4(paste(path_ff, file_ff, sep = ""), "TREFHT") %>%
  apply(2, rollvar)

ghg_var <- extract_nino3.4(paste(path_sf, files_sf[1], sep = ""), "TREFHT") %>% 
  apply(2, rollvar) %>% 
  rbind(matrix(data = NA, nrow = (2172-1932), ncol = 20))

aer_var <- extract_nino3.4(paste(path_sf, files_sf[2], sep = ""), "TREFHT") %>% 
  apply(2, rollvar) %>% 
  rbind(matrix(data = NA, nrow = (2172-1932), ncol = 20))

bmb_var <- extract_nino3.4(paste(path_sf, files_sf[3], sep = ""), "TREFHT") %>% 
  apply(2, rollvar) %>% 
  rbind(matrix(data = NA, nrow = (2172-1320), ncol = 15))

luc_var <- extract_nino3.4(paste(path_sf, files_sf[4], sep = ""), "TREFHT") %>% 
  apply(2, rollvar) %>% 
  rbind(matrix(data = NA, nrow = (2172-1320), ncol = 5))

ctl_var <- extract_nino3.4(paste( path_ctl, file_ctl, sep = ""), "TREFHT") %>%
  apply(2, rollvar)

time <- ncdim_def("date", "years", date, unlim=TRUE, calendar="standard", longname="Years_since_0CE")
ensemble <- ncdim_def("ensemble", units="member", )


ff_mean <- apply(ff_var, 1, mean)
ff_se <- apply(ff_var, 1, se)

ghg_mean <- apply(ghg_var, 1, mean)
ghg_se <- apply(ghg_var, 1, se)

aer_mean <- apply(aer_var, 1, mean)
aer_se <- apply(aer_var, 1, se)

bmb_mean <- apply(bmb_var, 1, mean)
bmb_se <- apply(bmb_var, 1, se)

luc_mean <- apply(luc_var, 1, mean)
luc_se <- apply(luc_var, 1, se)


ff <- data.frame(Date = date, mean = ff_mean, sterr = ff_se)
ghg <- data.frame(Date = date[1:1931], mean = ghg_mean, sterr = ghg_se)
aer <- data.frame(Date = date[1:1931], mean = aer_mean, sterr = aer_se)
bmb <- data.frame(Date = date[1:1320], mean = bmb_mean, sterr = bmb_se)
luc <- data.frame(Date = date[1:1320], mean = luc_mean, sterr = luc_se)


yay <- ff %>% mutate(case = factor("Full Forcing")) %>%
  bind_rows(ghg %>%
              mutate(case = factor("Greenhouse"))) %>%
  bind_rows(aer %>%
              mutate(case = factor("Aerosols"))) %>%
  bind_rows(bmb %>%
              mutate(case = factor("Biomass")))  %>%
  bind_rows(luc %>%
              mutate(case = factor("Land Use"))) 

ggplot(yay, aes(y = mean,x = Date, color =case, fill=case, ymin = (mean - sterr), ymax = (mean + sterr)), show.legend = FALSE) + 
  geom_line() +
  geom_ribbon(alpha=0.5, color=NA) +
  facet_grid(case ~ .) +
  theme(legend.position = "none") +
  ylim(1.2,1.8)
ggsave("yay.pdf")

bootmean1 <- yay %>% filter(case == "Full Forcing") %>% select(mean) %>% filter(!is.na(mean))


