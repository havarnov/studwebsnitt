# -*- coding: utf-8 -*-
import unittest
import os

from ..studwebsnitt import *

class StudwebsnittTests(unittest.TestCase):
	"""
	This app's test class.
	"""

	def setUp(self):
		with open(os.path.join(os.path.dirname(__file__), "karakter_data.txt")) as f:
			self.karakter_data = f.read()

		self.subject = Subject(
							"Høst 2012",
							"TEP4515",
							"Termisk energi, fordypningsemne",
							"B",
							7.5,
						)

	def test_extract_subjects(self):
		subjects = extract_subjects(self.karakter_data)

		self.assertEqual(len(subjects), 10)

		self.assertEqual(subjects[0], self.subject)

	def test_calculate_snitt(self):
		subjects = extract_subjects(self.karakter_data)

		snitt = calculate_snitt(subjects)

		self.assertEqual(snitt[0], 3.50)
		self.assertEqual(snitt[1], "B")
