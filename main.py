from Classes import Doctor, Nurse, Receptionist, Patient, AppointmentSchedule

schedule = AppointmentSchedule()

# Healthcare professional's objects
doctor1 = Doctor('James Brown', 'd001')
doctor2 = Doctor('Emily Smith', 'd002')
nurse1 = Nurse('Christopher Bay', 'n001')
nurse2 = Nurse('Sarah Fish', 'n001')
recep1 = Receptionist('Suzan Bow', 'r001')
recep2 = Receptionist('Michael Duck', 'r002')

pat1 = Patient('Josh Stevens', '12 Brown Street X17 9XY London',
               '07246123985')
pat2 = Patient('Madge Eland', '3 Yellow Street X13 8XY London',
               '07926213854')
pat3 = Patient('Sacha Simmonds', '32 Red Street X19 7XY London',
               '07254692138')
pat4 = Patient('Mia Osborne', '113 Red Street X18 6XY London',
               '07254692138')
pat5 = Patient('Charlie Richards', '7 Red Street X9 5XY London',
               '07695123428')
pat6 = Patient('Paul Blench', '55 Pink Street E9 4ES London',
               '07456741980')
pat7 = Patient('patient7', '1 QQQ', '123')
pat8 = Patient('patient8', '2 QQQ', '124')
pat9 = Patient('patient9', '3 QQQ', '125')

ar_list = [
    pat1.request_appointment('consultation', doctor1, "2022-06-14"),
    pat2.request_appointment('consultation', doctor1, "2022-06-15"),
    pat3.request_appointment('consultation', doctor1, "2022-06-16"),
    pat4.request_appointment('consultation', doctor2, "2022-06-17"),
    pat5.request_appointment('consultation', doctor2, "2022-06-18"),
    pat6.request_appointment('consultation', doctor2, "2022-06-19"),
]

for i in ar_list:
    recep1.make_appointment(i.a_type, i.staff, i.patient, schedule,
                            i.a_date)

print("""
This script is a playground demo to create objects and test their 
functionalities. It contains objects as followed:

schedule (one object of AppointmentSchedule Class)
doctor1 and doctor2 (two objects of Doctor Class)
nurse1 and nurse2 (two objects of Nurse Class)
recep1 and recep2 (two objects of Receptionist Class)
par1, pat2, ..., pat9 (nine objects of Patient Class)

Moreover, there is a list of patient's requests for appointment (ar_list)
and for them a receptionist made and added appointments to the schedule's list
of object.

In this file below there are a few examples on how to use the script and how
it works.
""")

# STEP1
# Receptionist1 adds an appointment to doctor1 for patient7 (a free slot):
appointment1 = recep1.make_appointment(
    'consultation', doctor1, pat7, schedule, "2022-06-17")
print('- ' * 100)
print('Step 1: Receptionist1 adds an appointment to doctor1 for patient7')
print(appointment1)
if appointment1 in schedule.appointments:
    print('appointment1 is present in schedule.appointments')
print('- ' * 100)

# STEP2
# Receptionist1 adds an appointment to doctor1 for patient8 (a taken slot):
appointment2 = recep1.make_appointment(
    'consultation', doctor1, pat8, schedule, "2022-06-17")
print('Step 2: Receptionist1 adds an appointment to doctor1 for patient8 (a '
      'taken slot. It is not an emergency so the appointment will not be added'
      'to schedule\'s list')
print(appointment2)
if appointment2 is not schedule.appointments:
    print('appointment2 is not present in schedule.appointments')
print('- ' * 100)

# STEP3
# Receptionist2 adds an emergency as soon as possible (today) to doctor1
emergency1 = recep2.make_appointment(
    'emergency', doctor1, pat7, schedule)
print('Step 3: Receptionist2 adds an emergency to doctor1 for patient7 as'
      'soon as possible (today) to doctor1')
print(emergency1)
if emergency1 in schedule.appointments:
    print('emergency1 is present in schedule.appointments')
print('- ' * 100)

# STEP4
# Receptionist2 adds an emergency to doctor1 for patient8 on a chosen day
# ("2022-06-01")
emergency2 = recep2.make_appointment(
    'emergency', doctor1, pat8, schedule, "2022-06-01")
print('Step 4: Receptionist2 adds an emergency to doctor1 for patient8 on a '
      'chosen day"2022-06-01"')
print(emergency2)
if emergency2 in schedule.appointments:
    print('emergency2 is present in schedule.appointments')
print('- ' * 100)

# STEP5
# Receptionist2 adds an emergency to doctor1 for patient9 on a chosen day
# ("2022-06-01") that is already taken.
emergency3 = recep2.make_appointment(
    'emergency', doctor1, pat9, schedule, "2022-06-01")
print('tep 5: Receptionist2 adds an emergency to doctor1 for patient9 on a '
      'chosen day ("2022-06-01") that is already taken.')
print(emergency3)
if emergency3 in schedule.appointments:
    print('emergency3 is present in schedule.appointments')
print('- ' * 100)

# STEP6
# Receptionist1 adds a consultation to doctor1 for patient1 on a chosen day
# ("2022-06-02") that is already taken.
appointment3 = recep1.make_appointment(
    'consultation', doctor1, pat1, schedule, "2022-06-02")
print('Step 6: Receptionist1 adds an appointment to doctor1 for patient1 on a '
      'chosen day ("2022-06-01") that is already taken. It is not an emergency '
      'so the appointment will not be added to schedule\'s list')
print(appointment3)
if emergency3 is not schedule.appointments:
    print('appointment3 is not present in schedule.appointments')
print('- ' * 100)

# STEP 7
# Receptionist1 adds a consultation to doctor1 for patient2 as soon as possible
appointment4 = recep1.make_appointment('consultation', doctor1, pat2, schedule)
print('Receptionist1 adds a consultation to doctor1 for patient2 as soon as '
      'possible')
print(appointment4)
if appointment4 is not schedule.appointments:
    print('appointment4 is not present in schedule.appointments')
print('- ' * 100)

