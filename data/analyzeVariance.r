# Imports
library(ncdf4)
library(zoo)
library(dplyr)
library(ggplot2)
library(WaveletComp)
library(reshape2)

# save a plot my way
gsave <- function(name, plot = last_plot(), dimensions = c(8, 6), path = "./figures/") {
    ggsave(name, path = path, width = dimensions[1], height = dimensions[2])
}

xlim1 <- c(1930, 2090)
xlim2 <- c(1860, 2090)

l <- 0.2
m <- 0.5
d <- 0.8

cesm_1 <- read.table("./data/CESM1/cesm1_stats.csv", sep = ";", header = TRUE, dec = ",", )
ff2_df <- read.table("./data/CESM2/ff2_stats.csv", sep = ";", header = TRUE, dec = ",", )
ff1_df <- cesm_1 %>% filter(case == "FF")
cesm1_sf <- read.table("./data/CESM1/cesm1_sf.csv", sep = ";", header = TRUE, dec = ",", )

ff_compare <- ff1_df %>% mutate(case = "CESM1") %>%
    bind_rows(ff2_df %>% mutate(case = "CESM2"))

ggplot(cesm_1, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2*se), ymax = (mean + 2*se)), show.legend = FALSE) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  facet_wrap(vars(case), dir = "v") +
  theme(legend.position = "none") +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", x = "Date", y = "Variance", color = "Case")
gsave("cesm1.pdf")

ggplot(cesm_1, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2*se), ymax = (mean + 2*se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_2.pdf")

ggplot(cesm_1 %>% filter(case == "FF"), aes(y = mean, x = date, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 LENS 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("ff1.pdf")

ggplot(ff2_df, aes(y = mean, x = date, ymin = (mean - 2*se), ymax = (mean + 2*se))) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  xlim(xlim2) +
  labs(title = "CESM2 LENS 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("ff2.pdf")
## ggplot(ff_members, aes(x = date, y = value, group = Var2)) +
##     geom_line(alpha = .1)

## ggplot(ff2_members, aes(x = date, y = value, group = Var2)) +
##     geom_line(alpha = .1)

ggplot(ff_compare, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim2) +
  labs(title = "LENS 20-Year Variance", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("ff_compare.pdf")

ggplot(cesm1_sf, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  facet_grid(case ~ .) +
  geom_line() +
  geom_ribbon(alpha = m, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", subtitle = "Single Forcing Net Impact", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_sf.pdf")

ggplot(cesm1_sf, aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", subtitle = "Single Forcing Net Impact", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_sf_2.pdf")

ggplot(cesm1_sf %>% filter(case != "LUC"), aes(y = mean, x = date, color = case, fill = case, ymin = (mean - 2 * se), ymax = (mean + 2 * se))) +
  geom_line() +
  geom_ribbon(alpha = l, color = NA) +
  xlim(xlim1) +
  labs(title = "CESM1 20-Year Variance", subtitle = "Single Forcing Net Impact", x = "Date", y = "Variance", color = "Case", fill = "Case")
gsave("cesm1_sf_3.pdf")
