# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)

# CESM1 LENS and SF
ff <- read.table("ff_var.csv", sep = ",") %>% as.matrix()
ghg <- read.table("ghg_var.csv", sep = ",") %>% as.matrix()
aer <- read.table("aer_var.csv", sep = ",") %>% as.matrix()
bmb <- read.table("bmb_var.csv", sep = ",") %>% as.matrix()
luc <- read.table("luc_var.csv", sep = ",") %>% as.matrix()

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


ggplot(cesm_1, aes(y = mean, x = date, color =case, fill=case, ymin = (mean - se), ymax = (mean + se)), show.legend = FALSE) +
  geom_line() +
  geom_ribbon(alpha=0.5, color=NA) +
#  facet_grid(case ~ .) +
  theme(legend.position = "none") +
  ylim(1.2,1.8)

ggplot(ff_df, aes(y = mean, x = date, ymin = (mean - se), ymax = (mean + se))) +
    geom_line(color = "Blue") +
    geom_ribbon(alpha = .5, fill = "Blue", color = NA)

ggplot(ff_compare, aes(y = Mean, x = Date, color = Case, fill = Case, ymin = (Mean - SE), ymax = (Mean + SE))) +
    geom_line() +
    geom_ribbon(alpha = 0.5, color = NA)
ggsave("../figures/compare_cesm1-2.pdf", width = 5, height = 3)
