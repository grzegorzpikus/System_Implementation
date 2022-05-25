from Classes import Doctor, Nurse, Receptionist, Patient, AppointmentSchedule

# Healthcare professional's objects
doctor1 = Doctor('James Brown', 'd001')
doctor2 = Doctor('Emily Smith', 'd002')
nurse1 = Nurse('Christopher Bay', 'n001')
nurse2 = Nurse('Sarah Fish', 'n001')
recep1 = Receptionist('Suzan Bow', 'r001')
recep2 = Receptionist('Michael Duck', 'r002')

# Patient's objects
pat1 = Patient('Josh Stevens', '12 Brown Street X17 9XY London', '07246123985')
pat2 = Patient('Madge Eland', '3 Yellow Street X13 8XY London', '07926213854')
pat3 = Patient('Sacha Simmonds', '32 Red Street X19 7XY London', '07254692138')
pat4 = Patient('Mia Osborne', '113 Red Street X18 6XY London', '07254692138')
pat5 = Patient('Charlie Richards', '7 Red Street X9 5XY London', '07695123428')
pat6 = Patient('Paul Blench', '55 Pink Street E9 4ES London', '07456741980')
pat7 = Patient('patient7', '1 QQQ', '123')
pat8 = Patient('patient8', '2 QQQ', '124')
pat9 = Patient('patient9', '3 QQQ', '125')

# Patient's requests for appointment (pat - patient, ar - appointment request)
p1_ar = pat1.request_appointment('consultation', doctor1, "2022-06-14")
p2_ar = pat2.request_appointment('consultation', doctor1, "2022-06-15")
p3_ar = pat3.request_appointment('consultation', doctor1, "2022-06-16")
p4_ar = pat4.request_appointment('consultation', doctor2, "2022-06-17")
p5_ar = pat5.request_appointment('consultation', doctor2, "2022-06-18")
p6_ar = pat6.request_appointment('consultation', doctor2, "2022-06-19")
