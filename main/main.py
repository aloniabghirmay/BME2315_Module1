# imports the Patient file and other libraries
from main_patients import *
import csv 
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
import math as math
from sklearn.linear_model import LinearRegression

#creates a linear regression object
model = LinearRegression()

#creates patient objects for all rows of data in the csv file
Patient.instantiate_from_csv("main/patientdata.csv")

# sorts the data by age and then by whether they have dementia or not, thus two groups in numerical order
# and then prints all patients in all_patients
Patient.all_patients.sort(key = Patient.get_age, reverse = False)
Patient.all_patients.sort(key = Patient.get_dementia, reverse = True)
for patient in Patient.all_patients: 
    print(patient)

# lists to hold all dementia patient brain pH values and no dementia brain pH values
dementia_ph = []
no_dementia_ph = []

# variables to hold the sums of all pH values for dementia and no dementia patients
dt_ph = 0.0
ndt_ph = 0.0

# variables to hold the mean of the pH values for dementia and no dementia patients to then use as the bars on the graph
d_bar = 0.0
nd_bar = 0.0

# variables to hold the standard deviations of the dementia and no dementia brain pH data sets
d_std = 0.0
nd_std = 0.0

# the next two sections filter the data to separate the patients with dementia and then extract their brain pH into two separate lists
Patient.some_patients = Patient.filter_attr(Patient.all_patients, dementia = "Dementia")
for patient in Patient.some_patients:
    dementia_ph.append(patient.get_brain_ph())

Patient.some_patients = Patient.filter_attr(Patient.all_patients, dementia = "No dementia")
for patient in Patient.some_patients:
    no_dementia_ph.append(patient.get_brain_ph())

# summing of all pH values of each group to use to find the mean
for each in dementia_ph:
    dt_ph += each

for each in no_dementia_ph:
    ndt_ph += each

# calculating the mean pH to use as the bar in the bar graph
d_bar = math.trunc(dt_ph * 1000 / (len(dementia_ph))) / 1000
nd_bar = math.trunc(ndt_ph * 1000 / (len(no_dementia_ph))) / 1000

# calculating the standard deviation of the two brain pH data sets
d_std = math.trunc(statistics.stdev(dementia_ph) * 1000) / 1000
nd_std = math.trunc(statistics.stdev(no_dementia_ph) * 1000) / 1000

# prints the value of the mean pH and standard deviations of the dementia and no dementia patient data sets
print("Statistical Information of Data Set:")
print(f'd_bar = {d_bar} | nd_bar = {nd_bar}') 
print(f'd_std = {d_std} | nd_std = {nd_std}')

# creating lists for making the bar graph
average_ph_cols = ['Dementia', 'No Dementia']
mean_ph = [d_bar, nd_bar]
std_groups = [d_std, nd_std]
yerr = std_groups

# running the t-test of the data
t_stat, p_val = stats.ttest_ind(dementia_ph, no_dementia_ph)
t_stat = math.trunc(t_stat * 100) / 100
p_val = math.trunc(p_val * 100) / 100
print(f't_stat = {t_stat}, p_val = {p_val}')
print(f'')

# creates the limit of the y-axis based on the maximum pH value
ylim = max(mean_ph) + 1.5

# creating the bar graph
plt.bar(average_ph_cols, mean_ph, yerr=yerr, capsize=10, color=["orange", "blue"])
plt.title("Average Brain pH of Dementia Patients and Patients without Dementia")
plt.xlabel("Cognitive Status")
plt.ylabel("Average Brain pH")
plt.ylim(0, ylim)
plt.text(
        0.5, ylim - 1,
        f"t = {t_stat},\n p = {p_val}",
        ha = 'center',
        va = 'bottom'
        )

# saves the bar graph as a .png
plt.savefig("brain_ph_bar_graph.png")

# outputs the resulting bar graph
plt.show()

female_dementia = Patient.filter(Patient.all_patients, sex = "F", cog_stat = "Dementia")
male_dementia = Patient.filter(Patient.all_patients, sex = "M", cog_stat = "Dementia")

# creating lists for the ptau values in all males and females with dementia
ptau_female = []
ptau_male = []

# adds the ptau levels of females and males with dementia into two separate lists
for patient in female_dementia:
    ptau_female.append(patient.ptau)

for patient in male_dementia:
    ptau_male.append(patient.ptau)

# calculate the mean pTAU level for each group
female_mean = statistics.mean(ptau_female)
male_mean = statistics.mean(ptau_male)

# calculate the standard deviation for each group
female_stdev = statistics.stdev(ptau_female)
male_stdev = statistics.stdev(ptau_male)

# prints the statistical information
print(f"Female mean pTAU: {female_mean}")
print(f"Female standard deviation: {female_stdev}")

print(f"Male mean pTAU: {male_mean}")
print(f"Male standard deviation: {male_stdev}")

# creating lists to make bar graph
groups = ["Female", "Male"]
means = [female_mean, male_mean]
stdevs = [female_stdev, male_stdev]

# calculating the t-value and p-value of the data
t_stat, p_val = stats.ttest_ind(ptau_female, ptau_male)
print(f't-stat = {t_stat}, p_val = {p_val}')

# truncating t-value and p-values up to 2 decimal places
t_stat = math.trunc(t_stat * 100) / 100
p_val = math.trunc(p_val * 100) / 100

# creating bar graph
plt.ylim(0, 10)
plt.bar(groups, means, yerr=stdevs, capsize=10)
plt.xlabel("Sex")
plt.ylabel("Mean pTAU (pg/ug)")
plt.title("Mean pTAU Levels in Patients with Dementia")
plt.text(
        0.5, 8.5,
        f"t = {t_stat},\n p = {p_val}",
        ha = 'center',
        va = 'bottom'
        )

# saves the resulting bar graph as a .png file
plt.savefig("ptau_bar_graph.png")

# outputs the resulting bar graph
plt.show()

# creates empty lists for age at death and pTAU levels
ages = []
ptau_values = []

# adds each patient's age at death and pTAU value to the lists
for patient in Patient.all_patients:
    ages.append(patient.get_age())
    ptau_values.append(patient.get_ptau())

model.fit(np.array(ages).reshape(-1, 1), ptau_values)
slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(np.array(ages).reshape(-1, 1), ptau_values)
equation = f"y = {slope:.2f}x + {intercept:.2f}\nR^2 = {r2:.2f}"

# creates the scatterplot
plt.ylim(min(ptau_values),max(ptau_values) + 3)
plt.scatter(np.array(ages).reshape(-1, 1), ptau_values)
plt.xlabel("Age at Death")
plt.ylabel("pTAU (pg/ug)")
plt.title("pTAU Levels vs. Age at Death")

# linear regression related
plt.text(statistics.mean(ages), max(ptau_values) + 2, equation, color = "blue", fontsize = 12, verticalalignment = "top")
plt.plot(np.array(ages).reshape(-1, 1), model.predict(np.array(ages).reshape(-1, 1)), color = "blue")

# saves the resulting bar graph as a .png file
plt.savefig("ptau_versus_ageofdeath_scatter_plot.png") #save the graph as a png file

# outputs the resulting bar graph
plt.show()

# creating lists for data points for the scatterplot
dementia_ab = []
dementia_tau = []
no_dementia_ab = []
no_dementia_tau = []

# creates two lists that holds patients with either dementia or no dementia
dementia_patients = Patient.filter_attr(Patient.all_patients, dementia = "Dementia")
no_dementia_patients = Patient.filter_attr(Patient.all_patients, dementia = "No dementia")

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

# reshapes the arrays to allow for linear regression to be computed
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
plt.title('Scatterplot Fraction of ABeta versus TAU')
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

# saves the scatterplot as a .png
plt.savefig("abeta_versus_tau_ratios_scatterplot.png")

# outputs the resulting scatterplot
plt.show()

# creates empty lists for pTAU and MMSE
ptau_mmse = []
mmse_scores = []

# add pTAU and MMSE values for patients who have an MMSE score
for patient in Patient.all_patients:
    if patient.mmse is not None:
        ptau_mmse.append(patient.ptau)
        mmse_scores.append(patient.mmse)

# prints the pTAU values and MMSE scores
print("pTAU values for MMSE analysis:")
print(ptau_mmse)

print("MMSE scores:")
print(mmse_scores)

# ----------------------------------------------------
# pTAU VS MMSE SCATTER PLOT
# ----------------------------------------------------

# Independent variable = pTAU
X = np.array(ptau_mmse).reshape(-1, 1)

# Dependent variable = MMSE score
y = np.array(mmse_scores)

# Do the linear regression
model.fit(X, y)

# Find slope, intercept, and R^2
slope = model.coef_[0]
intercept = model.intercept_
r2 = model.score(X, y)

# prints the slope, intercept, and R^2 values
print(f"Slope = {slope}")
print(f"Intercept = {intercept}")
print(f"R-squared = {r2}")

# combines the above characteristics of the line of best fit
equation = f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r2:.2f}"

# creates a scatterplot of ptau levels vs mmse scores
plt.scatter(X, y)
plt.plot(X, model.predict(X))
plt.xlabel("pTAU Concentration (pg/ug)")
plt.ylabel("MMSE Score")
plt.title("pTAU Concentration vs. MMSE Score")

# Put equation and R^2 on graph
plt.text(
    X.max(),
    y.max(),
    equation,
    fontsize=12,
    verticalalignment='top',
    horizontalalignment='right'
)

# saves the scatterplot as a .png file
plt.savefig("ptau_vs_mmse_scatterplot.png")

# outputs the resulting scatterplot
plt.show()