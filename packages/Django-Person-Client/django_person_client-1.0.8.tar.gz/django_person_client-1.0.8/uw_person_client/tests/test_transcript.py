# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_person_client.tests import ModelTest
from uw_person_client.models import Person


class TranscriptTest(ModelTest):
    def test_get_transcripts(self):
        p = Person.objects.get_person_by_uwnetid(
            'javerage', include_student=True, include_student_transcripts=True)

        transcripts = p.student.transcripts.all()
        self.assertEqual(len(transcripts), 3)

        # default transcript sorting
        t1 = transcripts[0]
        t2 = transcripts[1]
        t3 = transcripts[2]
        self.assertLess(int(f'{t2.tran_term.year}{t2.tran_term.quarter}'),
                        int(f'{t1.tran_term.year}{t1.tran_term.quarter}'))
        self.assertLess(int(f'{t3.tran_term.year}{t3.tran_term.quarter}'),
                        int(f'{t2.tran_term.year}{t2.tran_term.quarter}'))

        # t3, computed attributes
        self.assertEqual(t3.pk, 1)
        self.assertEqual(float(t3.deductible_credits), 0.0)
        self.assertEqual(float(t3.grade_points), 19.5)
        self.assertEqual(float(t3.graded_attempted), 5.0)
        self.assertEqual(float(t3.nongraded_earned), 0.0)
        self.assertEqual(float(t3.total_attempted), 5.0)
        self.assertEqual(float(t3.total_earned), 5.0)
        self.assertEqual(float(t3.gpa), 3.90)

        # t2, computed attributes
        self.assertEqual(t2.pk, 3)
        self.assertEqual(float(t2.deductible_credits), 1.0)
        self.assertEqual(float(t2.grade_points), 19.0)
        self.assertEqual(float(t2.graded_attempted), 13.2)
        self.assertEqual(float(t2.nongraded_earned), 2.0)
        self.assertEqual(float(t2.total_attempted), 14.2)
        self.assertEqual(float(t2.total_earned), 14.2)
        self.assertEqual(float(t2.gpa), 1.34)
