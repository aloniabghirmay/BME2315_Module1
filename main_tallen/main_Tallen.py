# imports the Patient file and other libraries
from patients_Tallen import *
import csv 
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
import math as math
from sklearn.linear_model import LinearRegression

#creates patient objects for all rows of data in the csv file
Patient.instantiate_from_csv("C:/Users/tall1/Documents/GitHub/BME2315_Module1/Metadata and Protein Data for Module 1.csv")

#sorts the data by age and then by whether they have dementia or not, thus two groups in numerical order
Patient.all_patients.sort(key = Patient.get_age, reverse = False)
Patient.all_patients.sort(key = Patient.get_dementia, reverse = True)

# lists to hold all female brain pH values and male brain pH values
female_ph = []
male_ph = []

# variables to hold the sums of all pH values for females and males
ft_ph = 0.0
mt_ph = 0.0

# variables to hold the mean of the pH values for females and males to then use as the bars on the graph
f_bar = 0.0
m_bar = 0.0

# variables to hold the standard deviations of the female and male brain pH data sets
f_std = 0.0
m_std = 0.0

# the next two sections filter the data to separate the female/male patients with dementia and then extract their brain pH into two separate lists
Patient.some_patients = Patient.filter_cs_sex(Patient.all_patients, sex = "F", dementia = "Dementia")
for patient in Patient.some_patients:
    female_ph.append(patient.get_brain_ph())

Patient.some_patients = Patient.filter_cs_sex(Patient.all_patients, sex = "M", dementia = "Dementia")
for patient in Patient.some_patients:
    male_ph.append(patient.get_brain_ph())

# summing of all pH values of each sex to use to find the mean
for each in female_ph:
    ft_ph += each

for each in male_ph:
    mt_ph += each

# calculating the mean pH to use as the bar in the bar graph
f_bar = math.trunc(ft_ph * 1000 / (len(female_ph))) / 1000
m_bar = math.trunc(mt_ph * 1000 / (len(male_ph))) / 1000

# calculating the standard deviation of the two brain pH data sets
f_std = math.trunc(statistics.stdev(female_ph) * 1000) / 1000
m_std = math.trunc(statistics.stdev(male_ph) * 1000) / 1000

# prints the value of the mean pH and standard deviations of the male and female data sets
print("Statistical Information of Data Set:")
print(f'f_bar = {f_bar} | m_bar = {m_bar}') 
print(f'f_std = {f_std} | m_std = {m_std}')

# creating lists for making the bar graph
average_ph_cols = ['Female', 'Male']
mean_ph = [f_bar, m_bar]
std_groups = [f_std, m_std]
yerr = std_groups

# running the t-test of the data
t_stat, p_val = stats.ttest_ind(female_ph, male_ph)
t_stat = math.trunc(t_stat * 100) / 100
p_val = math.trunc(p_val * 100) / 100
print(f't_stat = {t_stat}, p_val = {p_val}')
print(f'')

# creates the limit of the y-axis based on the maximum pH value
ylim = max(mean_ph) + 1.5

# creating the bar graph
plt.bar(average_ph_cols, mean_ph, yerr=yerr, capsize=10, color=["purple", "green"])
plt.title("Average Brain pH of Dementia Patients")
plt.xlabel("Sex")
plt.ylabel("Average Brain pH")
plt.ylim(0, ylim)
plt.text(
        0.5, ylim - 1,
        f"t = {t_stat},\n p = {p_val}",
        ha = 'center',
        va = 'bottom'
        )

# outputs the resulting bar graph
plt.show()

# saves the bar graph as a .png
plt.savefig("brain_ph_bar_graph.png")

# creating lists for data points for the scatterplot
dementia_ab = []
dementia_tau = []
no_dementia_ab = []
no_dementia_tau = []

# creates two lists that holds patients with either dementia or no dementia
dementia_patients = Patient.filter(Patient.all_patients, dementia = "Dementia")
no_dementia_patients = Patient.filter(Patient.all_patients, dementia = "No dementia")

# the next two sections take the values for ab40/42 and t/ptau and calculates the ration between 
# the same type of protein and adding them into lists to use as x and y values in the scatterplot
for patient in dementia_patients:
    dementia_ab.append(patient.get_ab_ratio())
    dementia_tau.append(patient.get_tau_ratio())

for patient in no_dementia_patients:
    no_dementia_ab.append(patient.get_ab_ratio())
    no_dementia_tau.append(patient.get_tau_ratio())

# creating x and y values for both patients with and without dementia
a = dementia_ab
b = dementia_tau
x = no_dementia_ab
y = no_dementia_tau

#creates a linear regression object
model = LinearRegression()

#reshapes the arrays to allow for linear regression to be computed
a_reg = np.array(a).reshape(-1, 1)
x_reg = np.array(x).reshape(-1, 1)

# determines the upper limits for the x- and y-axis based on the max value of the combined data set of protein ratios
if max(a) > max(x):
    xlim = max(x) + .05
else:
    xlim = max(a) + .05

if max(b) > max(y):
    ylim = max(b) + .05
else:
    ylim = max(y) + .05

# creation of the scatterplot
# red spots being patients with dementia and blue spots for patients without dementia
plt.scatter(a, b, s = 5, color='red')
plt.scatter(x, y, s = 5, color='blue')
plt.xlabel('Fraction of ABeta42 to Total ABeta')
plt.ylabel('Fraction of pTAU to tTAU')
plt.title('Scatter Plot Fraction of ABeta versus TAU')
plt.xlim(0, xlim)
plt.ylim(0, ylim)

# linear regression of the data points of patients with dementia
model.fit(a_reg, b)
slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(a_reg, b)
equation = f"y = {slope:.2f}x + {intercept:.2f}\nR^2 = {r2:.2f}"
plt.text(xlim * .1, ylim * 0.95, equation, color = "red", fontsize = 12, verticalalignment = "top")
plt.plot(a_reg, model.predict(a_reg), color = "red")

# linear regression of the data points of patients without dementia
model.fit(x_reg, y)
slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(x_reg, y)
equation = f"y = {slope:.2f}x + {intercept:.2f}\nR^2 = {r2:.2f}"
plt.text(xlim * .6, ylim * 0.95, equation, color = "blue", fontsize = 12, verticalalignment = "top")
plt.plot(x_reg, model.predict(x_reg), color = "blue")

# outputs the resulting scatterplot
plt.show()

# saves the scatterplot as a .png
plt.savefig("abeta_versus_tau_ratios_scatterplot.png")