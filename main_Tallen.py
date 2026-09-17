from patients_Tallen import * #importing Patient file and other libraries
import csv 
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import statistics

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

# summing of all pH values to use to fined the mean
for each in female_ph:
    ft_ph += each

for each in male_ph:
    mt_ph += each

# calculating the mean pH to use as the bar in the bar graph
f_bar = ft_ph / (len(female_ph))
m_bar = mt_ph / (len(male_ph))

# calculating the standard deviation of the two brain pH data sets
f_std = (statistics.stdev(female_ph))
m_std = (statistics.stdev(male_ph))

# prints the value of the mean pH and standard deviations of the male and female data sets
print(f'f_bar = {f_bar}, f_std {f_std}')
print(f'm_bar = {m_bar}, m_std {m_std}')

# creating lists for making the bar graph
average_ph_cols = ['Female', 'Male']
mean_ph = [f_bar, m_bar]
std_groups = [f_std, m_std]
yerr = [np.zeros(len(mean_ph)), std_groups]

# creation of the bar graph
plt.bar(average_ph_cols, mean_ph, yerr=yerr, capsize=10, color=["purple", "green"])
plt.title("Average Brain pH of Dementia Patients")
plt.xlabel("Sex")
plt.ylabel("Average Brain pH")
plt.show()

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

# creating x and y values
a = dementia_ab
b = dementia_tau
x = no_dementia_ab
y = no_dementia_tau

# creation of the scatterplot, red spots being patients with dementia and blue spots for patients without dementia
plt.scatter(a, b, s = 5, color='red')
plt.scatter(x, y, s = 5, color='blue')
plt.xlabel('Fraction of ABeta42 to Total ABeta')
plt.ylabel('Fraction of pTAU to tTAU')
plt.title('Scatter Plot Fraction of ABeta versus TAU')
plt.show()