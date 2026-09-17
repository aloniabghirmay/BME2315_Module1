from patient import *
import matplotlib.pyplot as plt
import numpy as np
import statistics
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
print (ptau_female)
print (ptau_male)
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
plt.show() #should show the graph, needed claude for this part, but understand how to use and what lines do

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