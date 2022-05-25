import datetime
from datetime import timedelta


class Receptionist:
    """Represents a receptionist working in the surgery. The class creates
    appointments and it passes them to the AppointmentSchedule. If a slot for
    an appointment is taken, Receptionist Class coordinates searching for
    an alternative available slot."""

    def __init__(self, name: str, emp_num: str):
        self.name = name
        self.emp_num = emp_num

    def __str__(self):
        return f"Receptionist {self.name} [{self.emp_num}]"

    def __repr__(self):
        return f"Receptionist({self.name}, {self.emp_num})"

    @staticmethod
    def make_appointment(a_type, staff, patient, schedule, a_date=None):
        """
        This function makes an appointment and adds it to the schedule.
        It accepts either a patient's request for the appointment or it can be
        made from scratch.
        If an appointment is a consultation and the slot is taken, receptionist
        returns next available slot, but it is not added to the schedule.
        If a_type is an emergency, receptionist returns next available slot and
        it is added to the schedule. The search for next available starts form
        alternative_date, which is automatically today's date if a_date has not
        been provided.
        """
        today = str(datetime.date.today())
        if a_date is None:
            alternative_date = today
        else:
            alternative_date = a_date

        # new_appointment = Appointment(a_type, staff, patient, a_date)
        if a_type == 'consultation':
            new_appointment = Appointment(a_type, staff, patient,
                                          alternative_date)
            if check_availability(new_appointment, schedule) is True:
                schedule.add_appointment(new_appointment)
                return new_appointment
            else:
                next_available = schedule.find_next_available(
                    a_type, staff, patient, alternative_date)
                return next_available
        else:
            next_available = schedule.find_next_available(
                a_type, staff, patient, alternative_date)
            schedule.add_appointment(next_available)
            return next_available

    @staticmethod
    def cancel_appointment(a_type, staff, patient, schedule, a_date=None):
        """
        This method manages canceling appointments form AppointmentSchedule.
        It checks first, whether the requested appointment to
        cancel exists. Next, the appointment is removed form schedule.
        Otherwise returns None.
        """
        to_cancel = Appointment(a_type, staff, patient, a_date)
        if check_availability(to_cancel, schedule) is False:
            canceled_appointment = schedule.cancel_appointment(to_cancel)
            return canceled_appointment
        else:
            return None


class HealthcareProfessional:
    """It is an abstract class represents the local surgery's professionals. It
    is a parent class for Doctor and Nurse classes. HealthcareProfessional
    class can make a note using consultation method."""

    def __init__(self, name, emp_num):
        self.name = name
        self.emp_num = emp_num

    def consultation(self, string: str):
        return string


class Doctor(HealthcareProfessional):
    """It represents a doctor who works in the surgery. This class is added to
    Appointment as one of its attributes. Doctor class also issues prescriptions
    for patients."""

    def __str__(self):
        return f"Dr {self.name} [{self.emp_num}]"

    def __repr__(self):
        return f"Doctor({self.name}, {self.emp_num}"

    def issue_prescription(self, p_type, patient, quantity, dosage):
        """This function returns a prescription issued by a doctor."""
        new_prescription = Prescription(p_type, patient, self, quantity, dosage)
        return new_prescription

    def accept_request(self, prescription, quantity, dosage):
        """This fiction returns a repeated prescription requested by a patient.
        A doctor has to add information about quantity and dosage."""
        prescription.doctor = self
        prescription.dosage = dosage
        prescription.quantity = quantity
        return prescription


class Nurse(HealthcareProfessional):
    """It represents a nurse who works in the surgery. This class is added to
    Appointment as one of its attributes."""

    def __str__(self):
        return f"{self.name}, nurse [{self.emp_num}]"

    def __repr__(self):
        return f"Nurse({self.name}, {self.emp_num}"


class Patient:
    """It represents a patient who is registered to the surgery. This class is
    added to Appointment as one of its attributes. Patient Class can request
    an appointment and a repeat prescription."""

    def __init__(self, name: str, address: str, phone: str):
        self.name = name
        self.address = address
        self.phone = phone

    def __str__(self):
        return f"Patient: {self.name}"

    def __repr__(self):
        return f"Patient({self.name}, {self.address}, {self.phone})"

    def request_repeat(self, doctor: Doctor):
        """This function returns a repeated prescription for a patient that has
        to be approved by a doctor."""
        new_prescription = Prescription('repeat', self, doctor)
        return new_prescription

    def request_appointment(self, a_type, staff, a_date):
        """This function returns an appointment that has to be checked and
        added to the schedule by a receptionist."""
        new_appointment = Appointment(a_type, staff, self, a_date)
        return new_appointment


class Prescription:
    """It represents a prescription that is issued by a doctor to a patient.
    p_type can be either 'repeat' or 'normal'."""

    def __init__(self, p_type: str, patient: Patient, doctor: Doctor,
                 quantity: int = None, dosage: float = None):
        if p_type == 'repeat' or p_type == 'normal':
            self.p_type = p_type
        else:
            raise ValueError('Wrong type')
        self.patient = patient
        self.doctor = doctor
        self.quantity = quantity
        self.dosage = dosage

    def __str__(self):
        return f"Prescription issued by {self.doctor} for {self.patient}. " \
               f"Type: {self.p_type}, quantity: {self.quantity}, " \
               f"dosage: {self.dosage}"

    def __repr__(self):
        return f"Prescription({self.p_type}, {self.doctor}, {self.patient}, " \
               f"{self.quantity}, {self.dosage})"

    def __eq__(self, other):
        if self.p_type == other.p_type and self.doctor == other.doctor and \
                self.patient == other.patient and self.quantity == \
                other.quantity and self.dosage == other.dosage:
            return True
        else:
            return False


class Appointment:
    """
    The class represent an appointment to a healthcare professional.
    a_type represents if it is a consultation or an emergency;
    staff represents either a doctor or a nurse;
    a_date represents a day when the appointment takes place.
    Appointments are created and managed by receptionist and are stored in
    AppointmentSchedule class.
    """

    def __init__(self, a_type: str, staff: HealthcareProfessional,
                 patient: Patient, a_date=None):
        if a_type == 'consultation' or a_type == 'emergency':
            self.a_type = a_type
        else:
            raise ValueError('Wrong type')
        self.staff = staff
        self.patient = patient
        self.a_date = a_date

    def __eq__(self, other):
        if self.a_type == other.a_type and self.staff == other.staff and \
                self.patient == other.patient and self.a_date == other.a_date:
            return True
        else:
            return False

    def __str__(self):
        if type(self.staff) is Doctor:
            return f"Appointment of {self.patient.name} to Dr " \
                   f"{self.staff.name} on {self.a_date}"
        else:
            return f"Appointment of {self.patient.name} to {self.staff.name} " \
                   f"on {self.a_date}"

    def __repr__(self):
        return f"<Appointment({self.a_type}, {self.staff}, {self.patient}, " \
               f"{self.a_date})>"


class AppointmentSchedule:
    """
    It represents a schedule of appointments to a doctor. This class is
    managed by a receptionist class that initialize adding, canceling and (if
    it is necessary) find next available methods.
    """

    def __init__(self):
        self.appointments = []

    def __str__(self):
        return f"Schedule for the clinic"

    def __repr__(self):
        return f"AppointmentSchedule()"

    def add_appointment(self, appointment):
        """This function adds the appointment to the schedule's list."""
        self.appointments.append(appointment)
        self.sort()
        return appointment

    def cancel_appointment(self, appointment):
        """This function removes an appointment form the schedule's list."""
        canceled_appointment = None
        for i in self.appointments:
            if appointment == i:
                canceled_appointment = self.appointments.pop(self.appointments.
                                                             index(i))
                if self.appointments != []:
                    self.sort()
        return canceled_appointment

    def find_next_available(self, a_type, staff, patient, starting_date):
        """
        This function finds next available slot in appointments list
        to make an appointment to a particular healthcare specialist and
        returns it. It does not add it to appointments list!
        """
        form = '%Y-%m-%d'
        # selecting appointments based on a particular healthcare specialist.
        sublist = []
        for i in self.appointments:
            if staff.emp_num == i.staff.emp_num:
                sublist.append(i)
        # if the sublist is empty, new appointment is made with
        # starting_date as an a_date
        if not sublist:
            new_appointment = Appointment(a_type, staff, patient, starting_date)
            return new_appointment
        # if the sublist contains only one appointment and its date is the same
        # as starting_date, new appointment is made with starting_date + 1 day.
        elif len(sublist) == 1:
            if sublist[0].a_date == starting_date:
                new_date = datetime.datetime.strptime(starting_date,
                                                      form).date() \
                           + timedelta(days=1)
                new_appointment = Appointment(a_type, staff, patient,
                                              str(new_date))
                return new_appointment
            # otherwise, new appointment is made with starting_date as an a_dat.
            else:
                new_appointment = Appointment(a_type, staff, patient,
                                              starting_date)
                return new_appointment
        # if the sublist has more than 1 element
        else:
            # if there is no appointment where a_date = starting_date
            is_starting_date_in_sublist = False
            for i in sublist:
                if i.a_date == starting_date:
                    is_starting_date_in_sublist = True
            if is_starting_date_in_sublist is False:
                new_appointment = Appointment(a_type, staff, patient,
                                              starting_date)
                return new_appointment
            else:
                # otherwise the helper function __next_available_busy_schedule()
                # is going check if there is any gap between appointments in the
                # sublist. If not, new appointment is added a day after the last
                # appointment in the sublist.
                output = self.__next_available_busy_schedule(
                    a_type, staff, patient, sublist, starting_date)
                return output

    def sort(self):
        """This function sorts appointments in the schedule's list by date."""
        self.appointments.sort(key=lambda appointment: appointment.a_date)

    def __next_available_busy_schedule(self, a_type, staff, patient, sublist,
                                       starting_date):
        """
        It is a helper function that searches any gap between appointments in
        the busy schedule (that contains more than one appointment to the
        healthcare specialist).
        """
        form = '%Y-%m-%d'
        index0 = 0
        index1 = 1
        # the search for next available will be form starting_date.
        # No slots will be found before that.
        for i in sublist:
            if datetime.datetime.strptime(i.a_date, form).date() < \
                    datetime.datetime.strptime(starting_date, form).date():
                sublist.pop(sublist.index(i))

        while index1 < len(sublist) - 1:
            date_0 = datetime.datetime.strptime(sublist[index0].a_date,
                                                form).date()
            date_1 = datetime.datetime.strptime(sublist[index1].a_date,
                                                form).date()
            if int((date_1 - date_0).days) == 1:
                index0 += 1
                index1 += 1
                # no gap is found, so next pair of appointments are
                # going to be compared.
            else:
                # a gap between two appointments was found. The new appointment
                # is going to be added after the appointment with
                # a_date = date_0.
                new_date = date_0 + timedelta(days=1)
                new_appointment = Appointment(a_type, staff, patient,
                                              str(new_date))
                return new_appointment
        date_0 = datetime.datetime.strptime(sublist[index0].a_date,
                                            form).date()
        date_1 = datetime.datetime.strptime(sublist[index1].a_date,
                                            form).date()
        # Here if the last pair of appointments does not have a gap
        # between, new appointment is added at the end.
        if int((date_1 - date_0).days) == 1:
            new_date = date_1 + timedelta(days=1)
            new_appointment = Appointment(a_type, staff, patient,
                                          str(new_date))
            return new_appointment
        # otherwise new appointment is added after the penultimate one.
        else:
            new_date = date_0 + timedelta(days=1)
            new_appointment = Appointment(a_type, staff, patient,
                                          str(new_date))
            return new_appointment


def check_availability(appointment, schedule):
    """
    This function checks if an appointment to a specific healthcare
    professional, can be made and added to schedule by a receptionist for the
    given date. It returns 'True' or 'False'.
    """
    sublist = []
    # appointments are selected based on a healthcare professional.
    for i in schedule.appointments:
        if appointment.staff.emp_num == i.staff.emp_num:
            sublist.append(i)
    # finds if there is any free slot for the given date to the particular
    # professional.
    output = True
    for i in sublist:
        if appointment.a_date == i.a_date:
            output = False
    return output
