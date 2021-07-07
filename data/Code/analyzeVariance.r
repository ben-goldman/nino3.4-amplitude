library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)

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

mydate <- read.table("mydate.csv", sep = ",") %>% as.vector()

ff_df <- data.frame(time = mydate, mean = ff_mean, sterr = ff_se)
ghg_df <- data.frame(time = mydate, mean = ghg_mean, sterr = ghg_se)
aer_df <- data.frame(time = mydate, mean = aer_mean, sterr = aer_se)
bmb_df <- data.frame(time = mydate, mean = bmb_mean, sterr = bmb_se)
luc_df <- data.frame(time = mydate, mean = luc_mean, sterr = luc_se)


nino <- ff_df %>% mutate(case = factor("Full Forcing")) %>%
  bind_rows(ghg_df %>%
              mutate(case = factor("Greenhouse"))) %>%
  bind_rows(aer_df %>%
              mutate(case = factor("Aerosols"))) %>%
  bind_rows(bmb_df %>%
              mutate(case = factor("Biomass")))  %>%
  bind_rows(luc_df %>%
              mutate(case = factor("Land Use")))

ggplot(nino, aes(y = mean,x = x, color =case, fill=case, ymin = (mean - sterr), ymax = (mean + sterr)), show.legend = FALSE) +
  geom_line() +
  geom_ribbon(alpha=0.5, color=NA) +
  facet_grid(case ~ .) +
  theme(legend.position = "none") +
  ylim(1.2,1.8)
