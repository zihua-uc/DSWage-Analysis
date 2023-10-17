# load libraries
library(stargazer)
library(lfe)
library(ggplot2)
library(ggpubr)
options(digits=3)

# clear workspace
rm(list=ls())

# load data
glassdoor_data <- read.csv("../data/cleaned_data.csv", row.names = 1)
acs_data <- read.csv("../data/ACS_data.csv")
data <- merge(glassdoor_data, acs_data, by.x = "company_roleLocation", 
              by.y = "state")

# function for plotting
plot_residuals <- function(data, residuals, filename) {
  
  # Plot residuals vs x
  p1 <- ggplot(data=data, aes(x=state_med_owner_cost, y=residuals)) + 
    geom_point(shape=1) + geom_smooth(method='lm', formula= y~x) + theme_bw() + 
    labs(title="Residuals vs Monthly Median Owner Cost", y="Residuals", 
         x="Monthly Median Owner Cost") + 
    theme(plot.title = element_text(hjust = 0.5))
  
  p2 <- ggplot(data=data, aes(x=state_pct_emp_tech, y=residuals)) + 
    geom_point(shape=1) + geom_smooth(method='lm', formula= y~x) + theme_bw() + 
    labs(title="Residuals vs Percentage Employed In Tech", y="Residuals", 
         x="Percentage Employed In Tech") + 
    theme(plot.title = element_text(hjust = 0.5))
  
  p3 <- ggplot(data=data, aes(x=state_pct_college, y=residuals)) + 
    geom_point(shape=1) + geom_smooth(method='lm', formula= y~x) + theme_bw() + 
    labs(title="Residuals vs Percentage With College Degree", y="Residuals", 
         x="Percentage With College Degree") +
    theme(plot.title = element_text(hjust = 0.5))
  
  ggarrange(p1, p2, p3, ncol=3, nrow=1)
  ggsave(paste0('../reg_result/', filename), width=15, height=5)
  
}

## regressions on state-level variables
lm1 <- lm(company_salary ~ state_med_owner_cost, data = data)
lm2 <- lm(company_salary ~ state_med_owner_cost + state_pct_emp_tech, 
          data = data)
lm3 <- lm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
            state_pct_college, data = data)
lm4 <- lm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
            state_pct_college + state_pop_in_hh, data = data)
lm5 <- lm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
            state_pct_college + state_pop_in_hh + state_med_income, data = data)
lm6 <- lm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
            state_pct_college + state_pop_in_hh + state_med_income + 
            state_med_rent, data = data)

# Export tables
stargazer(lm1, lm2, lm3, lm4, lm5, lm6,
          title = "Regressions on state level variables", 
          model.numbers = FALSE,
          dep.var.caption = 'Dependent Variable: Annual Salary (in 1000s)',
          dep.var.labels.include = F,
          omit.stat = c("LL","ser", "f", "adj.rsq"),
          covariate.labels = c("Median Cost to Own a Home (Monthly)",
                               "Percentage Employed in Tech",
                               'Percentage of College Graduates',
                               "Population (In Households)",
                               "Median Income", 
                               "Median Rent (Monthly)"), 
          font.size = 'footnotesize', type ='latex', digits=3, 
          out='../reg_result/regressions1.tex')

# Plot residuals vs x
plot_residuals(data, lm6$residuals, "residuals_check1.png")


## Regressions including state-level and company-level variables
lm7 <- lm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
            state_pct_college + state_pop_in_hh + state_med_income + 
            state_med_rent + company_starRating, data = data)
lm8 <- lm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
            state_pct_college + state_pop_in_hh + state_med_income + 
            state_med_rent + company_starRating + company_founded, data = data)
lm9 <- felm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
              state_pct_college + state_pop_in_hh + state_med_income + 
              state_med_rent + company_starRating + 
              company_founded|company_revenue|0|0, data = data)
lm10 <- felm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
               state_pct_college + state_pop_in_hh + state_med_income + 
               state_med_rent + company_starRating + 
               company_founded|company_revenue+company_size|0|0, data = data)
lm11 <- felm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
               state_pct_college + state_pop_in_hh + state_med_income + 
               state_med_rent + company_starRating + 
               company_founded|company_revenue+company_size+company_type|0|0, 
             data = data)
lm12 <- felm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
               state_pct_college + state_pop_in_hh + state_med_income + 
               state_med_rent + company_starRating + 
               company_founded|company_revenue+company_size+company_type+
               company_sector|0|0, data = data)

# Export tables
stargazer(lm7, lm8, lm9, lm10, lm11, lm12,
          title = "Regressions on state level variables with company 
          level variables as controls", 
          model.numbers = FALSE,
          dep.var.caption = 'Dependent Variable: Annual Salary (in 1000s)',
          dep.var.labels.include = F,
          omit.stat = c("LL","ser", "f", "adj.rsq"),
          covariate.labels = c("Median Cost to Own a Home (Monthly)",
                               "Percentage Employed in Tech",
                               'Percentage of College Graduates',
                               "Population (In Households)",
                               "Median Income",
                               "Median Rent (Monthly)",
                               "Company Star Rating",
                               "Year Company Was Founded"), 
          add.lines = list(c("Company Revenue FE", "No" ,"No", 'Yes', "Yes", 
                             "Yes" ,"Yes"),
                           c("Company Size FE", "No" ,"No", 'No', 'Yes', "Yes", 
                             "Yes"),
                           c("Company Type FE", "No" ,"No", 'No', 'No', "Yes", 
                             "Yes"),
                           c("Company Sector FE", "No" ,"No", 'No', 'No', "No", 
                             "Yes")),
          font.size = 'footnotesize', type ='latex', digits=3, 
          out='../reg_result/regressions2.tex')

# Plot residuals vs x
plot_residuals(data[!is.na(data$company_founded) & !is.na(data$company_starRating),], 
               lm12$residuals, "residuals_check2.png")


## Regressions including state-level, company-level, and job-level variables
lm13 <- felm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
               state_pct_college + state_pop_in_hh + state_med_income + 
               state_med_rent + company_starRating + 
               company_founded|company_revenue + company_size + company_type +
               company_sector + job_title|0|0, data = data)
lm14 <- felm(company_salary ~ state_med_owner_cost + state_pct_emp_tech + 
               state_pct_college + state_pop_in_hh + state_med_income + 
               state_med_rent + company_starRating + 
               company_founded|company_revenue + company_size + company_type + 
               company_sector + job_title + job_seniority|0|0, data = data)

# Export tables
stargazer(lm13, lm14,
          title = "Regressions on state level variables with company level 
          variables and job titles as controls", 
          model.numbers = FALSE,
          dep.var.caption = 'Dependent Variable: Annual Salary (in 1000s)',
          dep.var.labels.include = F,
          omit.stat = c("LL","ser", "f", "adj.rsq"),
          covariate.labels = c("Median Cost to Own a Home (Monthly)",
                               "Percentage Employed in Tech",
                               'Percentage of College Graduates',
                               "Population (In Households)",
                               "Median Income",
                               "Median Rent (Monthly)",
                               "Company Star Rating",
                               "Year Company Was Founded"), 
          add.lines = list(c("Company Revenue FE", "Yes" ,"Yes"),
                           c("Company Size FE", "Yes" ,"Yes"),
                           c("Company Type FE", "Yes" ,"Yes"),
                           c("Company Sector FE", "Yes","Yes"),
                           c("Job Title FE", "Yes","Yes"),
                           c("Job Seniority FE", "No","Yes")),
          font.size = 'footnotesize', type ='latex', digits=3, 
          out='../reg_result/regressions3.tex')

# Plot residuals vs x
plot_residuals(data[!is.na(data$company_founded) & !is.na(data$company_starRating),], 
               lm14$residuals, "residuals_check3.png")


## plot distribution of residuals
p10 <- ggplot(data=data.frame(lm6$residuals), aes(x=lm6$residuals)) + 
  geom_density(linewidth=1.1) + theme_bw() + 
  labs(title="Residuals from Table (1) Col (6)", y="Density", 
       x="Residuals") + theme(plot.title = element_text(hjust = 0.5))
p11 <- ggplot(data=data.frame(lm12$residuals), aes(x=lm12$residuals)) + 
  geom_density(linewidth=1.1) + theme_bw() + 
  labs(title="Residuals from Table (2) Col (6)", y="Density", 
       x="Residuals") + theme(plot.title = element_text(hjust = 0.5))
p12 <- ggplot(data=data.frame(lm14$residuals), aes(x=lm14$residuals)) + 
  geom_density(linewidth=1.1) + theme_bw() + 
  labs(title="Residuals from Table (3) Col (2)", y="Density", 
       x="Residuals") + theme(plot.title = element_text(hjust = 0.5))

ggarrange(p10, p11, p12, ncol=3, nrow=1)
ggsave('../reg_result/residuals_distribution.png', width=15, height=5)

