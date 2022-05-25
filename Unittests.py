import unittest
import datetime
from datetime import timedelta
from Classes import Appointment, AppointmentSchedule, Prescription, \
    check_availability
import Unittests_data as Ud


class AppointmentTests(unittest.TestCase):

    def test_make_appointment(self):
        """The test checks if an appointment is created correctly via
        make_appointment method."""
        schedule = build_schedule()
        test_make1 = Ud.recep1.make_appointment('consultation', Ud.doctor1,
                                                Ud.pat7, schedule, "2022-06-17")
        expected_make1 = Appointment('consultation', Ud.doctor1, Ud.pat7,
                                     "2022-06-17")
        self.assertEqual(test_make1, expected_make1)

    def test_make_appointment_sorting(self):
        """The test checks if an appointment that is made by Receptionist class
        has index 0."""
        schedule = build_schedule()
        Ud.recep2.make_appointment('consultation', Ud.doctor1, Ud.pat7,
                                   schedule, "2022-06-01")
        test_make2 = schedule.appointments[0]
        expected_make2 = Appointment('consultation', Ud.doctor1, Ud.pat7,
                                     "2022-06-01")
        self.assertEqual(test_make2, expected_make2)

    def test_make_appointment_taken_slot(self):
        """
        Receptionist tries to add an appointment that the slot is already
        taken. The test checks if receptionist returns the next available slot,
        that is today.
        """
        schedule = build_schedule()
        test_make3 = Ud.recep2.make_appointment('consultation', Ud.doctor1,
                                                Ud.pat7, schedule, "2022-06-14")
        expected_make3 = Appointment('consultation', Ud.doctor1, Ud.pat7,
                                     "2022-06-17")
        self.assertEqual(test_make3, expected_make3)

    def test_make_appointment_emergency(self):
        """The test checks if an emergency is added to schedule as the first
        available slot, which is today (index 0)."""
        schedule = build_schedule()
        today = str(datetime.date.today())
        Ud.recep2.make_appointment('emergency', Ud.doctor1,
                                                Ud.pat7, schedule)
        test_make4 = Appointment('emergency', Ud.doctor1,
                                                 Ud.pat7, today)
        expected_make4 = schedule.appointments[0]
        self.assertEqual(test_make4, expected_make4)

    def test_make_appointment_emergency2(self):
        """
        Test checks if another emergency appointment (to the same doctor) is
        tomorrow (as slot for today is already taken. The appointment should
        have index 1 in schedule's list of appointments.
        """
        schedule = build_schedule()
        today = str(datetime.date.today())
        Ud.recep2.make_appointment('emergency', Ud.doctor1, Ud.pat7, schedule)
        test_make5 = Ud.recep2.make_appointment('emergency', Ud.doctor1,
                                                Ud.pat8, schedule, today)
        expected_make5 = schedule.appointments[1]
        self.assertEqual(test_make5, expected_make5)

    def test_make_appointment_wrong_type(self):
        """The test checks if Exception(ValueError) is risen when a wrong
        argument for a_type attribute is given."""
        schedule = build_schedule()
        with self.assertRaises(ValueError):
            Ud.recep1.make_appointment('normal', Ud.nurse1, Ud.pat7, schedule,
                                       "2022-06-02")

    def test_cancel_appointment(self):
        """The test checks if an appointment is removed form the schedule.
        The number of objects in the list of appointments (schedule.appointment)
        is equal 6. After cancellation it should be 5.
        """
        schedule = build_schedule()
        Ud.recep1.cancel_appointment('consultation', Ud.doctor1, Ud.pat3,
                                     schedule, "2022-06-16")
        cancel_test = len(schedule.appointments)
        expected_cancel = 5
        self.assertEqual(cancel_test, expected_cancel)

    def test_cancel_appointment_empty(self):
        """
        The test checks if receptionist returns 'None' if
        an appointment that is about to be canceled does not exist in schedule.
        """
        schedule = build_schedule()

        cancel_test = Ud.recep1.cancel_appointment(
            'consultation', Ud.doctor1, Ud.pat3, schedule, "2023-06-16")
        expected_cancel = None
        self.assertEqual(cancel_test, expected_cancel)


class PrescriptionTest(unittest.TestCase):

    def test_request_repeat(self):
        """The test checks if an request for a prescription is correctly
        made."""
        request = self.build_requests()
        expected_request = Prescription('repeat', Ud.pat1, Ud.doctor1)
        self.assertEqual(request, expected_request)

    def test_issue_presc(self):
        """The test checks if a prescription is correctly issed."""
        prescription = Ud.doctor1.issue_prescription('normal', Ud.pat1, 10, 2.0)
        expected_prescription = Prescription('normal', Ud.pat1, Ud.doctor1, 10,
                                             2.0)
        self.assertEqual(prescription, expected_prescription)

    def test_issue_presc_wrong_type(self):
        """The test checks if Exception(ValueError) is risen when a wrong
        argument for p_type attribute is given."""
        with self.assertRaises(ValueError):
            Ud.doctor2.issue_prescription('single', Ud.pat7, 20, 1.5)

    def build_requests(self):
        """This function create a patient's request for a repeating
        prescription."""
        rq1 = Ud.pat1.request_repeat(Ud.doctor1)
        return rq1


class ScheduleAppointmentTest(unittest.TestCase):

    def test_add_appointment(self):
        """The function checks if an appointment is added to the schedule's
        list of appointments"""
        schedule = build_schedule()
        appointment = Appointment('consultation', Ud.nurse1, Ud.pat7,
                                  "2022-12-01")
        expected_appointment = schedule.add_appointment(appointment)
        self.assertEqual(len(schedule.appointments), 7)
        self.assertEqual(appointment, expected_appointment)

    def test_cancel_appointment(self):
        """
        The test checks if an appointment is correctly removed form the
        schedule's list of appointments, if the method rmoves corect appointment
        and if the function sorts the rest remaining appointments.
        """
        schedule = build_schedule()
        appointment = Appointment('consultation', Ud.doctor1, Ud.pat2,
                                  "2022-06-15")
        canceled = schedule.cancel_appointment(appointment)
        index_1 = Appointment('consultation', Ud.doctor1, Ud.pat3, "2022-06-16")
        self.assertEqual(len(schedule.appointments), 5)
        self.assertEqual(canceled, appointment)
        self.assertEqual(schedule.appointments[1], index_1)

    def test_find_next_available1(self):
        """The test checks if the method looks correctly for the next available
        slot to make the appointment if today is available."""
        schedule = build_schedule()
        today = str(datetime.date.today())
        next_available = schedule.find_next_available(
            'consultation', Ud.doctor1, Ud.pat7, today)
        expected_next_available = Appointment('consultation', Ud.doctor1,
                                              Ud.pat7, today)
        self.assertEqual(next_available, expected_next_available)

    def test_find_next_available2(self):
        """The test checks if the method looks correctly for the next available
        slot to make the appointment if today is unavailable."""
        schedule = build_schedule()
        today = str(datetime.date.today())
        correct_date = str(datetime.date.today() + timedelta(days=1))
        schedule.add_appointment(Appointment('consultation', Ud.doctor1,
                                             Ud.pat7, today))
        next_available = schedule.find_next_available(
            'consultation', Ud.doctor1, Ud.pat8, today)
        expected_next_available = Appointment('consultation', Ud.doctor1,
                                             Ud.pat8, correct_date)
        self.assertEqual(next_available, expected_next_available)

    def test_find_next_available3(self):
        """
        The test checks if the method looks correctly for the next available
        slot to make the appointment, it there is an empty slot between two
        appointments.
        """
        starting_date = "2022-06-14"
        schedule = build_schedule()
        schedule.cancel_appointment(Appointment('consultation', Ud.doctor1,
                                                Ud.pat2, "2022-06-15"))
        next_available = schedule.find_next_available(
            'consultation', Ud.doctor1, Ud.pat7, starting_date)
        expected_next_available = Appointment('consultation', Ud.doctor1,
                                              Ud.pat7, "2022-06-15")
        self.assertEqual(next_available, expected_next_available)

    def test_find_next_available4(self):
        """The test checks if an appointment is added correctly as the last
        one to doctor1"""
        starting_date = "2022-06-14"
        schedule = build_schedule()
        next_available = schedule.find_next_available(
            'consultation', Ud.doctor1, Ud.pat7, starting_date)
        expected_next_available = Appointment('consultation', Ud.doctor1,
                                              Ud.pat7, "2022-06-17")
        self.assertEqual(next_available, expected_next_available)

    def test_sort(self):
        """It tests if sorting method works correctly."""
        schedule = build_schedule()
        appointment = schedule.cancel_appointment(Appointment(
            'consultation', Ud.doctor1, Ud.pat2, "2022-06-15"))
        schedule.add_appointment(appointment)
        date_list = []
        for i in schedule.appointments:
            date_list.append(i.a_date)
        expected_date_list = ["2022-06-14", "2022-06-15", "2022-06-16",
                              "2022-06-17", "2022-06-18", "2022-06-19"]
        self.assertEqual(date_list, expected_date_list)


class CheckAvailabilityTest(unittest.TestCase):

    def test_check_availability(self):
        schedule = build_schedule()
        appointment_present = Appointment('consultation', Ud.doctor1, Ud.pat1,
                                          "2022-06-14")
        new_appointment = Appointment('consultation', Ud.doctor1, Ud.pat7,
                                      "2022-06-17")
        output_False = check_availability(appointment_present, schedule)
        output_True = check_availability(new_appointment, schedule)
        self.assertEqual(output_False, False)
        self.assertEqual(output_True, True)


class HealthcareProfessionalTest(unittest.TestCase):

    def test_consultation(self):
        """The test checks if the method returns string"""
        string = Ud.doctor1.consultation('consultation')
        expected_string = 'consultation'
        self.assertEqual(string, expected_string)


def build_schedule():
    """This function create AppointmentSchedule's object for tests."""
    schedule = AppointmentSchedule()

    Ud.recep1.make_appointment(Ud.p3_ar.a_type, Ud.p3_ar.staff,
                               Ud.p3_ar.patient, schedule, Ud.p3_ar.a_date)
    Ud.recep1.make_appointment(Ud.p1_ar.a_type, Ud.p1_ar.staff,
                               Ud.p1_ar.patient, schedule, Ud.p1_ar.a_date)
    Ud.recep1.make_appointment(Ud.p2_ar.a_type, Ud.p2_ar.staff,
                               Ud.p2_ar.patient, schedule, Ud.p2_ar.a_date)
    Ud.recep2.make_appointment(Ud.p6_ar.a_type, Ud.p6_ar.staff,
                               Ud.p6_ar.patient, schedule, Ud.p6_ar.a_date)
    Ud.recep2.make_appointment(Ud.p5_ar.a_type, Ud.p5_ar.staff,
                               Ud.p5_ar.patient, schedule, Ud.p5_ar.a_date)
    Ud.recep2.make_appointment(Ud.p4_ar.a_type, Ud.p4_ar.staff,
                               Ud.p4_ar.patient, schedule, Ud.p4_ar.a_date)
    schedule.sort()

    return schedule

if __name__ == '__main__':
    unittest.main()
