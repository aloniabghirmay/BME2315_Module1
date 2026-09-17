import csv
class Patient:
# a list containing all patients as they are made
    all_patients = []
# creates a patient object with the following attributes and then adds the new object to the list of all patients
    def __init__(self, age: int = "any", sex: str = "any", edu_years: int = "any", apoe: str = "any", dementia: str = "any", brain_ph: float = "any", ab40: float = "any", ab42: float = "any", ttau: float = "any", ptau: float = "any"):
        self.age = age
        self.sex = sex
        self.edu_years = edu_years
        self.apoe = apoe
        self.dementia = dementia
        self.brain_ph = brain_ph
        self.ab40 = ab40
        self.ab42 = ab42
        self.ttau = ttau
        self.ptau = ptau
        Patient.all_patients.append(self)
# how a patient is printed
    def __repr__(self):
        return f"({self.age} | {self.sex} | {self.apoe} | {self.dementia})"
# retrieves the age of death
    def get_age(self):
        return self.age
# retrieves the cognitive status
    def get_dementia(self):
        return self.dementia
# retrieves brain pH
    def get_brain_ph(self):
        return self.brain_ph
# retrieves the ratio of ABeta42 to the total amount of ABeta protein
    def get_ab_ratio(self):
        return self.ab42 / (self.ab40 + self.ab42)
# retrieves the ratio of pTAU to the total amount of the TAU protein
    def get_tau_ratio(self):
        return self.ptau / self.ttau
# retrieves the amount of ABeta42
    def get_ab42(self):
        return self.ab42
# retrieves the amount of pTAU
    def get_ptau(self):
        return self.ptau
# creates patient objects from a csv file (the patient information)
    @classmethod 
    def instantiate_from_csv(cls, filename: str):

        #the code below will open the .csv file and create a list of all the rows in the spreadsheet
        
        with open(filename, encoding="utf8") as f:
            reader = csv.DictReader(f)
            rows_of_patients = list(reader)


            patient_sex = "n/a"

             #the code below will create a patient object for each row, based on the data from the .csv file

            for row in rows_of_patients:

                if row['Sex'] == "Male":
                    patient_sex = "M"
                else:
                    patient_sex = "F"
            
                Patient(
                age = int(row['Age at Death']),
                sex = patient_sex,
                edu_years = int(row['Years of education']),
                apoe = row['APOE Genotype'],
                dementia = row['Cognitive Status'],
                brain_ph = float(row['Brain pH']),
                ab40 = float(row['ABeta40 pg/ug']),
                ab42 = float(row['ABeta42 pg/ug']),
                ttau = float(row['tTAU pg/ug']),
                ptau = float(row['pTAU pg/ug'])
                )
# returns a list of patients that share the input attributes' value
    @classmethod
    def filter(cls, list, age:int ="any", sex:str ="any", edu_years:int ="any", apoe:str ="any", dementia:str ="any", brain_ph:float = "any", ab40:float = "any", ab42:float = "any", ttau:float = "any", ptau:float = "any"):
        all_patients = list
        remove_list = []
        attr_list = (
                    age,
                    sex,
                    edu_years,
                    apoe,
                    dementia,
                    brain_ph,
                    ab40,
                    ab42,
                    ttau,
                    ptau
                    )
        attr_name = (
                    "age",
                    "sex",
                    "edu_years",
                    "apoe",
                    "dementia",
                    "brain_ph",
                    "ab40",
                    "ab42",
                    "ttau",
                    "ptau"
                    )
# goes through the attributes of each patient and adds them to the remove_list if the attribute is not shared
        for attr in range(len(attr_list)):
            if attr_list[attr] != "any":
                for patient in all_patients:
                    if getattr(patient,attr_name[attr]) != attr_list[attr]:
                        remove_list.append(patient)
# adds patients from all_patients to some_patients if the patient is NOT on the remove_list
                some_patients = [patient for patient in all_patients if patient not in remove_list]
                remove_list.clear()
        return some_patients
# returns a list of patients that share the two input attribute values; sex and cognitive status
    @classmethod
    def filter_cs_sex(cls, list, sex:str = "any", dementia:str = "any"):
        new_list = []
# references the filter method above
        new_list = cls.filter(list, sex = sex)
# the new_list is input into the filter rather than the initial list
        new_list = cls.filter(new_list, dementia = dementia)
# prints the patients in the new, filtered list and adds a border to the bottom of the list
        for patient in new_list:
            print(patient)
        print("/////////////////////////////")
        return new_list
