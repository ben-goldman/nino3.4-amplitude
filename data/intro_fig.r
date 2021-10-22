library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(reshape2)
library(scico)

ncin <- nc_open("/Volumes/Extreme-SSD/DATA/HadISST_sst.nc")

sst <- ncvar_get(ncin, "sst")
sst[sst == -1000] <- NA

date <- ncvar_get(ncin, "time")
date <- date/365 + 1870

lat <- ncvar_get(ncin, "latitude")
lon <- ncvar_get(ncin, "longitude")

rownames(sst) <- lon
colnames(sst) <- lat

sst_wrap <- array(NA, dim = dim(sst))
## lon_wrap <- rep(NA, times = length(lon))
## lon_wrap[0:211] <- lon[150:360]
## lon_wrap[212:360] <- lon[1:149]
lon_wrap <- lon + 180
sst_wrap[0:180,,] <- sst[181:360,,]
sst_wrap[181:360,,] <- sst[1:180,,]
rownames(sst_wrap) <- lon_wrap
colnames(sst_wrap) <- lat

## NEED TO MAKE ANOMALY PLOT!
monthly_avgs <- array(NA, dim = c(360, 180, 12))

for (i in c(1:12)) {
    writeLines(as.character(i))
    monthly_avgs[,,i] <- sst_wrap[,,seq(i, 1800 + i, 12)] %>% apply(c(1,2), mean, na.rm = TRUE)
}

rownames(monthly_avgs) <- lon_wrap
colnames(monthly_avgs) <- lat

monthly_avgs_melt <- monthly_avgs %>% melt(varnames = c("longitude", "latitude", "month"))

monthly_avgs_melt$month <- as.factor(monthly_avgs_melt$month)
# levels = c("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Sep", "Oct", "Nov", "Dec"))

sst_anom <- array(NA, dim = dim(sst_wrap))
months <- rep(1:12, length.out = dim(sst_wrap)[3])

for(t in 1:dim(sst_wrap)[3]) {
    sst_anom[,,t] <- sst_wrap[,,t] - monthly_avgs[,,months[t]]
}
dimnames(sst_anom) <- list(lon_wrap, lat, date)



sst_anom_1997_melt <- sst_anom[,,match(date[abs(date - 1997.75) < 1], date)] %>%
    apply(c(1,2), mean) %>%
    melt(varnames = c("longitude", "latitude"))

sst_anom_1975_melt <- sst_anom[,,match(date[abs(date - 1975.75) < 1], date)] %>%
    apply(c(1,2), mean) %>%
    melt(varnames = c("longitude", "latitude"))

sst_anom_compare <- sst_anom_1997_melt %>% mutate(case = "1997 El Niño") %>%
    bind_rows(sst_anom_1975_melt %>% mutate(case = "1975 La Niña"))

gsave <- function(name, plot = last_plot(), dimensions = c(6, 8), path = "./figures/") {
    ggsave(name, path = path, width = dimensions[1], height = dimensions[2])
}

ggplot(sst_anom_compare %>% filter(latitude < 60 &
                           latitude > -60 &
                           longitude > 50 &
                           longitude < 350), aes(longitude, latitude, fill = value)) +
    geom_raster() +
    facet_wrap(vars(case), nrow = 2, ncol = 1) +
    scale_fill_scico(palette = "vik") +
    labs(title = "Pacific SST Anomalies Comparison",
         x = "Longitude",
         y = "Latitude",
         fill = " SST \n Anomaly \n (°C)") +
    theme(text = element_text(size = 20))

gsave("intro_fig.pdf", dimensions = c(8, 8))

## ggplot(sst_anom_compare %>% filter(latitude < 60 &
##                            latitude > -60 &
##                            longitude > 50 &
##                            longitude < 350), aes(longitude, latitude, z = value)) +
##     geom_contour_filled(bins = 20) +
##     facet_wrap(vars(case), nrow = 2, ncol = 1) +
##     scale_fill_scico_d(palette = "vik") +
##     labs(title = "Pacific SST Anomalies Comparison",
##          x = "Longitude",
##          y = "Latitude",
##          fill = " SST \n Anomaly \n (°C)") +
##     theme(text = element_text(size = 20))

## gsave("intro_fig_2.pdf")

ncin2 <- nc_open("/Volumes/Extreme-SSD/DATA/BEN/air.2x2.1200.mon.anom.land.nc")

temp <- ncvar_get(ncin2, "air")

avg_temp <- temp %>% apply(3, mean, na.rm = TRUE)

index_1 <- data.frame(date = date[6:(1698-6)], air = avg_temp %>% rollapply(width = 12, mean))
index_5 <- data.frame(date = date[(6 * 5):(1698 - 6 * 5)], air = avg_temp %>% rollapply(width = 12 * 5, mean))
index_10 <- data.frame(date = date[(6 * 10):(1698 - 6 * 10)], air = avg_temp %>% rollapply(width = 12 * 10, mean))
index_20 <- data.frame(date = date[(6 * 20):(1698 - 6 * 20)], air = avg_temp %>% rollapply(width = 12 * 20, mean))

reg <- lm(air ~ date, index_1, y = TRUE)

reg_vec <- data.frame(date = date, air = date * reg$coefficients[2] + reg$coefficients[1])

temp_df <- index_1 %>% mutate(case = "1-Year") %>%
    bind_rows(index_10 %>% mutate(case = "10-Year"))
    #bind_rows(reg_vec %>% mutate(case = "Linear Model")) %>%
    # bind_rows(index_20 %>% mutate(case = "20-Year Smoothing"))

ggplot(temp_df, aes(date, air, color = case)) +
    geom_path() +
    labs(title = "Mean Land Air Temperature Anomaly",
         x = "Date",
         y = "Temperature Anomaly (°C)",
         color = "Smoothing\nWindow Size") +
    theme(text = element_text(size = 20))

gsave("intro_fig_3.pdf", dimensions = c(8, 6))
