import csv
class Patient:#defines the patient class
    all_patients = []
    def __init__(self, name, age_at_death, sex, years_education, cognitive_status, ptau): #constructor, defines the attributes
        self.name = name # Donor ID
        self.age_at_death = age_at_death
        self.sex = sex
        self.years_education = years_education
        self.cognitive_status = cognitive_status
        self.ptau = ptau

        Patient.all_patients.append(self) #from dog folder, adds new patient object to the list
    def __repr__(self): #representer, defines how a patient object comes up  
        return f"Patient({self.name}, {self.age_at_death}, {self.sex}, {self.years_education}, {self.cognitive_status}, {self.ptau})"
            # Class method that creates Patient objects from the CSV file
    def get_age_at_death(self):
                return self.age_at_death
    @classmethod
    def instantiate_from_csv(cls, filename): #from dog file

        with open(filename, encoding="utf8") as file: #opens the csv and creates a list of the rows
            reader = csv.DictReader(file)
            rows_of_patients = list(reader)

        for row in rows_of_patients: # Create one patient object for each row 
            Patient(
                name=row["Donor ID"],
                age_at_death=int(row["Age at Death"]),
                sex=row["Sex"],
                years_education=int(row["Years of education"]),
                cognitive_status=row["Cognitive Status"],
                ptau=float(row["pTAU pg/ug"])
            )
    @classmethod
    def filter_patients(cls, sex, cognitive_status): #filters the patient objects by sex and cognitive status
        filtered_patients = []
        for patient in Patient.all_patients:
             if patient.sex == sex and patient.cognitive_status == cognitive_status:
                filtered_patients.append(patient)
        return filtered_patients