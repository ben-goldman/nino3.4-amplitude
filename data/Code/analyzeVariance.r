# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)

# CESM1 LENS and SF
ff <- read.table("ff_var.csv", sep = ",") %>% as.matrix()
ghg <- read.table("ghg_var.csv", sep = ",") %>% as.matrix()
aer <- read.table("aer_var.csv", sep = ",") %>% as.matrix()
bmb <- read.table("bmb_var.csv", sep = ",") %>% as.matrix()
luc <- read.table("luc_var.csv", sep = ",") %>% as.matrix()

ff_raw_mean <- read.table("ff_raw.csv", sep = ",") %>% as.matrix() %>% apply(1, mean)

ff_mean <- apply(X = ff, MARGIN = 1, FUN = mean)
ghg_mean <- apply(X = ghg, MARGIN = 1, FUN = mean)
aer_mean <- apply(X = aer, MARGIN = 1, FUN = mean)
bmb_mean <- apply(X = bmb, MARGIN = 1, FUN = mean)
luc_mean <- apply(X = luc, MARGIN = 1, FUN = mean)

se <- function(x, ...) sd(x, ...)/sqrt(length(x))

ff_se <- apply(X = ff, MARGIN = 1, FUN = se)
ghg_se <- apply(X = ghg, MARGIN = 1, FUN = se)
aer_se <- apply(X = aer, MARGIN = 1, FUN = se)
bmb_se <- apply(X = bmb, MARGIN = 1, FUN = se)
luc_se <- apply(X = luc, MARGIN = 1, FUN = se)

date.num <- seq(1920, 2100, length.out = 2172)
date.str <- read.table("mydate.csv", sep = ",")$x
mydate <- date.num

ff_df <- data.frame(date = mydate, mean = ff_mean, se = ff_se)
ghg_df <- data.frame(date = mydate, mean = ghg_mean, se = ghg_se)
aer_df <- data.frame(date = mydate, mean = aer_mean, se = aer_se)
bmb_df <- data.frame(date = mydate, mean = bmb_mean, se = bmb_se)
luc_df <- data.frame(date = mydate, mean = luc_mean, se = luc_se)

ff_members <- ff %>% melt() %>% mutate(date = (Var1/12 + 1920))

cesm_1 <- ff_df %>% mutate(case = factor("Full Forcing")) %>%
  bind_rows(ghg_df %>%
              mutate(case = factor("Greenhouse"))) %>%
  bind_rows(aer_df %>%
              mutate(case = factor("Aerosols"))) %>%
  bind_rows(bmb_df %>%
              mutate(case = factor("Biomass")))  %>%
  bind_rows(luc_df %>%
              mutate(case = factor("Land Use")))

# CESM2 LENS
ff_2 <- read.table("ff_var_CESM2.csv", sep = ",") %>% as.matrix()

ff_2_mean <- apply(X = ff_2, MARGIN = 1, FUN = mean)

ff_2_se <- apply(X = ff_2, MARGIN = 1, FUN = se)

mydate_2 <- seq(1850, 2100, length.out = 3012)

ff_2_df <- data.frame(date = mydate_2, mean = ff_2_mean, se = ff_2_se)

ff_2_members <- ff_2 %>% melt() %>% mutate(date = (Var1/12 + 1850))

#ff_compare <- ff_df %>% mutate(case = factor("CESM1")) %>%
#    bind_rows(ff_2_df %>%
#              mutate(case = factor("CESM2")) %>%
#              rbind)

ff_compare <-
    data.frame(mean = c(rep(NA, (3012 - 2172)), ff_mean),
               se = c(rep(NA, (3012 - 2172)), ff_se)) %>%
    mutate(case = factor("CESM1")) %>%
    bind_rows(data.frame(mean = ff_2_mean,
                         se = ff_2_se)%>%
              mutate(case = factor("CESM2"))) %>%
    cbind(mydate_2)
colnames(ff_compare) <- c("Mean", "SE", "Case", "Date")

# Bootstrap process to generate sf timeseries

subtract.bootstrap <- function(data1, data2, reps) {
    len <- dim(data1)[1]
    num1 <- dim(data1)[2]
    num2 <- dim(data2)[2]
    out <- matrix(NA, ncol = reps, nrow = len)
#    writeLines(as.character(dim(out)))
#    writeLines(as.character(len))
    choice1 <- sample(x = 1:num1, size = reps, replace = TRUE)
    choice2 <- sample(x = 1:num2, size = reps, replace = TRUE)
    for(i in 1:reps){
        writeLines(as.character(i))
#        writeLines(as.character(choice1[i]))
#        writeLines(as.character(choice2[i]))
        answer <- data1[, choice1[i]] - data2[, choice2[i]]
#        writeLines(as.character(length(answer)))
        out[, i] <- answer
    }
    return(out)
}

reps <- 1000
se_bs <- function(x, n) {return(sd(x)/sqrt(n))}

ghg_sf <- subtract.bootstrap(ff, ghg, reps)
ghg_sf_mean <- ghg_sf %>% apply(1, mean)
ghg_sf_se <- ghg_sf %>% apply(1, se_bs, n = 20)

aer_sf <- subtract.bootstrap(ff, aer, reps)
aer_sf_mean <- aer_sf %>% apply(1, mean)
aer_sf_se <- aer_sf %>% apply(1, se_bs, n = 20)

bmb_sf <- subtract.bootstrap(ff, bmb, reps)
bmb_sf_mean <- bmb_sf %>% apply(1, mean)
bmb_sf_se <- bmb_sf %>% apply(1, se_bs, n = 15)

luc_sf <- subtract.bootstrap(ff, luc, reps)
luc_sf_mean <- luc_sf %>% apply(1, mean)
luc_sf_se <- luc_sf %>% apply(1, se_bs, n = 5)

cesm_1_sf <-
    data.frame(mean = ghg_sf_mean,
               se = ghg_sf_se) %>%
    mutate(case = factor("GHG")) %>%
    bind_rows(data.frame(mean = aer_sf_mean,
                         se = aer_sf_se) %>%
              mutate(case = factor("AER"))) %>%
    bind_rows(data.frame(mean = bmb_sf_mean,
                         se = bmb_sf_se) %>%
              mutate(case = factor("BMB"))) %>%
    bind_rows(data.frame(mean = luc_sf_mean,
                         se = luc_sf_se) %>%
              mutate(case = factor("LUC"))) %>%
    cbind(mydate)
colnames(cesm_1_sf) <- c("Mean", "SE", "Case", "Date")

# little bit of wavelet stuff :)
ff_rw_ts_dec <- ts(ff_raw_mean, frequency = 12) %>% decompose()
ff_resid <- ff_rw_ts_dec$random
ff_resid_wvlt_power <- WaveletTransform(ff_resid[7:2166])$Power %>% melt()

ff_reg_wvlt_power <- WaveletTransform(ff_raw_mean)$Power %>% melt

ff_resid_wvlt_power$Var1 <- (2172 / ff_resid_wvlt_power)$Var1 / 12
ff_reg_wvlt_power$Var1 <- (2172 / ff_reg_wvlt_power$Var1) / 12

# PLOTTING

ggplot(cesm_1, aes(y = mean, x = date, color =case, fill=case, ymin = (mean - se), ymax = (mean + se)), show.legend = FALSE) +
  geom_line() +
  geom_ribbon(alpha=0.5, color=NA) +
#  facet_grid(case ~ .) +
  theme(legend.position = "none") +
  ylim(1.2,1.8)

ggplot(ff_df, aes(y = mean, x = date, ymin = (mean - se), ymax = (mean + se))) +
    geom_line(color = "Blue") +
    geom_ribbon(alpha = .5, fill = "Blue", color = NA)

ggplot(ff_2_df, aes(y = mean, x = date, ymin = (mean - se), ymax = (mean + se))) +
    geom_line() +
    geom_ribbon(alpha = .5)

ggplot(ff_members, aes(x = date, y = value, group = Var2)) +
    geom_line(alpha = .1) +

ggplot(ff_2_members, aes(x = date, y = value, group = Var2)) +
    geom_line(alpha = .1)

ggplot(ff_compare, aes(y = Mean, x = Date, color = Case, fill = Case, ymin = (Mean - SE), ymax = (Mean + SE))) +
    geom_line() +
    geom_ribbon(alpha = 0.5, color = NA)
ggsave("../figures/compare_cesm1-2.pdf", width = 5, height = 3)

ggplot(cesm_1_sf, aes(y = Mean, x = Date, color = Case, fill = Case, ymin = (Mean - SE), ymax = (Mean + SE))) +
    facet_grid(Case ~ .) +
    geom_line() +
    geom_ribbon(alpha = 0.5, color = NA)

ggplot(ff_resid_wvlt_power, aes(Var2, Var1, z = value)) +
    geom_contour_filled() +
    scale_y_log10()

ggplot(ff_reg_wvlt_power, aes(Var2, Var1, z = value)) +
    geom_contour_filled() +
    scale_y_log10()
