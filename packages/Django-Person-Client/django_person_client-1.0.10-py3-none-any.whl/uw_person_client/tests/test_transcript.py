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

        # t3, to_dict
        d3 = t3.to_dict()
        self.assertEqual(d3['deductible_credits'], '0.0')
        self.assertEqual(d3['grade_points'], '19.50')
        self.assertEqual(d3['graded_attempted'], '5.0')
        self.assertEqual(d3['nongraded_earned'], '0.0')
        self.assertEqual(d3['total_attempted'], '5.0')
        self.assertEqual(d3['total_earned'], '5.0')
        self.assertEqual(d3['gpa'], '3.90')

        # t2, computed attributes
        self.assertEqual(t2.pk, 3)
        self.assertEqual(float(t2.deductible_credits), 1.0)
        self.assertEqual(float(t2.grade_points), 19.0)
        self.assertEqual(float(t2.graded_attempted), 13.2)
        self.assertEqual(float(t2.nongraded_earned), 2.0)
        self.assertEqual(float(t2.total_attempted), 14.2)
        self.assertEqual(float(t2.total_earned), 14.2)
        self.assertEqual(float(t2.gpa), 1.34)

        # t2, to_dict
        d2 = t2.to_dict()
        self.assertEqual(d2['deductible_credits'], '1.0')
        self.assertEqual(d2['grade_points'], '19.00')
        self.assertEqual(d2['graded_attempted'], '13.2')
        self.assertEqual(d2['nongraded_earned'], '2.0')
        self.assertEqual(d2['total_attempted'], '14.2')
        self.assertEqual(d2['total_earned'], '14.2')
        self.assertEqual(d2['gpa'], '1.34')

    def test_get_transcripts_errors(self):
        p = Person.objects.get_person_by_uwnetid(
            'jbothell', include_student=True, include_student_transcripts=True)

        transcripts = p.student.transcripts.all()
        self.assertEqual(len(transcripts), 1)

        t1 = transcripts[0]

        # t1, computed attributes
        self.assertEqual(t1.pk, 2)
        self.assertEqual(float(t1.deductible_credits), 0)
        self.assertEqual(float(t1.grade_points), 41.2)
        self.assertEqual(float(t1.graded_attempted), 0)
        self.assertEqual(float(t1.nongraded_earned), 0)
        self.assertEqual(float(t1.total_attempted), 0)
        self.assertEqual(float(t1.total_earned), 0)
        self.assertEqual(float(t1.gpa), 0)

        # t2, to_dict
        d1 = t1.to_dict()
        self.assertEqual(d1['deductible_credits'], '0.0')
        self.assertEqual(d1['grade_points'], '41.20')
        self.assertEqual(d1['graded_attempted'], '0.0')
        self.assertEqual(d1['nongraded_earned'], '0.0')
        self.assertEqual(d1['total_attempted'], '0.0')
        self.assertEqual(d1['total_earned'], '0.0')
        self.assertEqual(d1['gpa'], '0.00')
