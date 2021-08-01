library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)

ff <- read.table("ff_var_CESM2.csv", sep = ",") %>% as.matrix()

ff_mean <- apply(X = ff, MARGIN = 1, FUN = mean)

se <- function(x, ...) sd(x, ...)/sqrt(length(x))

ff_se <- apply(X = ff, MARGIN = 1, FUN = se)

mydate <- seq(1850, 2100, length.out = 3012)

ggplot(ff_df, aes(y = mean, x = date, ymin = (mean - se), ymax = (mean + se))) +
    geom_line(color = "Blue") +
    geom_ribbon(alpha = .5, fill = "Blue", color = NA)
