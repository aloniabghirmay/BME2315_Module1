from patient import *
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics
import pandas as pd
from sklearn.linear_model import LinearRegression


Patient.instantiate_from_csv("patientdata.csv") #create patient objects


Patient.all_patients.sort(key=Patient.get_age_at_death, reverse=False) #sort the patient objects by age at death


for patient in Patient.all_patients: #print the patient objects

    print(patient)


female_dementia = Patient.filter_patients("Female","Dementia")


for patient in female_dementia:  #print the

    print(patient)


male_dementia = Patient.filter_patients("Male","Dementia")


ptau_female = []

ptau_male = []


for patient in female_dementia:  #print the filtered patients

    ptau_female.append(patient.ptau)


for patient in male_dementia:  #print the filtered patients

    ptau_male.append(patient.ptau)


print(ptau_female)

print(ptau_male)


female_mean = statistics.mean(ptau_female)# Calculate the mean pTAU level for each group

male_mean = statistics.mean(ptau_male)


female_stdev = statistics.stdev(ptau_female)# Calculate the standard deviation for each group

male_stdev = statistics.stdev(ptau_male)


print(f"Female mean pTAU: {female_mean}")

print(f"Female standard deviation: {female_stdev}")


print(f"Male mean pTAU: {male_mean}")

print(f"Male standard deviation: {male_stdev}")


groups = ["Female", "Male"]


means = [female_mean, male_mean]


stdevs = [female_stdev, male_stdev]


plt.bar(groups, means, yerr=stdevs, capsize=10)


plt.xlabel("Sex")

plt.ylabel("Mean pTAU (pg/ug)")

plt.title("Mean pTAU Levels in Patients with Dementia")


plt.savefig("ptau_bar_graph.png") #save the graph as a png file


plt.show() #should show the graph


# Create empty lists for age at death and pTAU

ages = []

ptau_values = []


# Add each patient's age at death and pTAU value to the lists

for patient in Patient.all_patients:

    ages.append(patient.age_at_death)

    ptau_values.append(patient.ptau)


# Create the scatter plot

plt.scatter(ages, ptau_values)


#labels and titles

plt.xlabel("Age at Death")

plt.ylabel("pTAU (pg/ug)")

plt.title("pTAU Levels vs. Age at Death")


plt.savefig("ptau_scatter_plot.png") #save the graph as a png file


plt.show()


#t test

t_stat, p_val = stats.ttest_ind(ptau_female, ptau_male)


print(f't-stat = {t_stat}, p_val = {p_val}')

# ABeta42 ANALYSIS FROM CLASS

ABeta42_health_fem_vals = []

ABeta42_health_male_vals = []

ABeta42_diseased_fem_vals = []

ABeta42_diseased_male_vals = []


for patient in Patient.filter(Patient.all_patients, sex = "Female", cog_stat = "No dementia"):

    ABeta42_health_fem_vals.append(patient.ABeta42)


for patient in Patient.filter(Patient.all_patients, sex = "Male", cog_stat = "No dementia"):

    ABeta42_health_male_vals.append(patient.ABeta42)


for patient in Patient.filter(Patient.all_patients, sex = "Female", cog_stat = "Dementia"):

    ABeta42_diseased_fem_vals.append(patient.ABeta42)


for patient in Patient.filter(Patient.all_patients, sex = "Male", cog_stat = "Dementia"):

    ABeta42_diseased_male_vals.append(patient.ABeta42)



x_health_fem_bar = (statistics.mean(ABeta42_health_fem_vals))

x_health_male_bar = (statistics.mean(ABeta42_health_male_vals))

x_diseased_fem_bar = (statistics.mean(ABeta42_diseased_fem_vals))

x_diseased_male_bar = (statistics.mean(ABeta42_diseased_male_vals))



ABeta_health_fem_stdev = (statistics.stdev(ABeta42_health_fem_vals))

ABeta_health_male_stdev = (statistics.stdev(ABeta42_health_male_vals))

ABeta_diseased_fem_stdev = (statistics.stdev(ABeta42_diseased_fem_vals))

ABeta_diseased_male_stdev = (statistics.stdev(ABeta42_diseased_male_vals))



print(f'x_bar = {x_health_fem_bar}, ABeta_stdev {ABeta_health_fem_stdev}')

print(f'x_bar = {x_health_male_bar}, ABeta_stdev {ABeta_health_male_stdev}')

print(f'x_bar = {x_diseased_fem_bar}, ABeta_stdev {ABeta_diseased_fem_stdev}')

print(f'x_bar = {x_diseased_male_bar}, ABeta_stdev {ABeta_diseased_male_stdev}')



sex_cols = ['Healthy Female', 'Healthy Male', 'Diseased Female', 'Diseased Male']

mean_sex_ABeta42 = [
    x_health_fem_bar,
    x_health_male_bar,
    x_diseased_fem_bar,
    x_diseased_male_bar
]


stdev_sex_ABeta42 = [
    ABeta_health_fem_stdev,
    ABeta_health_male_stdev,
    ABeta_diseased_fem_stdev,
    ABeta_diseased_male_stdev
]


colors = ["red", "blue", "pink", "skyblue"]


yerr = [np.zeros(len(mean_sex_ABeta42)), stdev_sex_ABeta42]


#ANOVA to test for differences in means between the four groups

f_stat, p_value = stats.f_oneway(
    ABeta42_health_fem_vals,
    ABeta42_health_male_vals,
    ABeta42_diseased_fem_vals,
    ABeta42_diseased_male_vals
)


print("F-statistic:", f_stat)

print("p-value:", p_value)


plt.text(
    1.5,
    380,
    f"One-Way-ANOVA: p = {p_value:.3f}",
    ha='right',
    va='top',
    fontsize=12
)


plt.bar(
    sex_cols,
    mean_sex_ABeta42,
    yerr=yerr,
    capsize=10,
    color=["red", "blue", "pink", "skyblue"]
)


plt.title("ABeta42 Levels")

plt.xlabel("Sex and Health Status")

plt.ylabel("Abeta42")


plt.show()

#pTAUCONCENTRATION VS. MMSESCORE

#empty lists to hold pTAU and MMSE values for patients who have an MMSE score

ptau_mmse = []

mmse_scores = []


#Add pTAU and MMSE values for patients who have an MMSE score

for patient in Patient.all_patients:

    if patient.mmse is not None:

        ptau_mmse.append(patient.ptau)

        mmse_scores.append(patient.mmse)



print("pTAU values for MMSE analysis:")

print(ptau_mmse)


print("MMSE scores:")

print(mmse_scores)



#Create scatter plot of pTAU vs MMSE


plt.scatter(ptau_mmse, mmse_scores)


plt.xlabel("pTAU Concentration (pg/ug)")

plt.ylabel("MMSE Score")

plt.title("pTAU Concentration vs. MMSE Score")


plt.savefig("ptau_vs_mmse_scatter.png")


plt.show()


#ptau is being set as independent variable and mmse is being set as dependent variable for linear regression

X = np.array(ptau_mmse).reshape(-1, 1)

y = np.array(mmse_scores)



#linearregression

model = LinearRegression()

model.fit(X, y)



#slope, intercept, and r-squared value of the regression line

slope = model.coef_[0]

intercept = model.intercept_

r2 = model.score(X, y)



print(f"Slope = {slope}")

print(f"Intercept = {intercept}")

print(f"R-squared = {r2}")



#equation to be displayed on the graph, from ChatGPT

equation = f"y = {slope:.2f}x + {intercept:.2f}\nR² = {r2:.2f}"



#the scatter plot of pTAU vs MMSE with the regression line and equation displayed on the graph

plt.scatter(X, y)


# Add regression line

plt.plot(X, model.predict(X))



#Put equation and R-squared on graph

plt.text(
    X.max(),
    y.max(),
    equation,
    fontsize=12,
    verticalalignment='top',
    horizontalalignment='right'
)



plt.xlabel("pTAU Concentration (pg/ug)")

plt.ylabel("MMSE Score")

plt.title("pTAU Concentration vs. MMSE Score")



plt.savefig("ptau_vs_mmse_regression.png")


plt.show()