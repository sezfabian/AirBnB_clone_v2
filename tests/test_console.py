#!/usr/bin/python3
""" Test module for console
"""
from console import HBNBCommand
from io import StringIO
from models import storage
from models.city import City
from models.state import State
from os import getenv
from re import search
from unittest import TestCase, skipIf
from unittest.mock import patch


@skipIf(getenv('HBNB_TYPE_STORAGE') == 'db',
        'Tests for file storage')
class TestCase(TestCase):
    """ Unittests for hbnb console """
    def setUp(self):
        """ Set up action at the beginning of each test
        """
        with patch('sys.stdout', new=StringIO()) as f:
            truncate_string_io(f)

    def test_do_create(self):
        """ Test object creation with given parameters
        """
        with patch('sys.stdout', new=StringIO()) as f:
            # test successful creation by getting id
            HBNBCommand().onecmd('create User name="Tester"')
            output = search(r'.*-.*-.*-.*$', f.getvalue()).group()
            self.assertEqual(f"{output}\n", f.getvalue())
            truncate_string_io(f)

            # test object and attributes persistance in file
            HBNBCommand().onecmd(f"show User {output}")
            self.assertTrue(output in f.getvalue())
            self.assertTrue("'name': 'Tester'" in f.getvalue())
            truncate_string_io(f)

            # test value conversion
            HBNBCommand().onecmd('create Place {} {} {}'.format(
                                 'name="Tiny_Home"',
                                 'guests=2',
                                 'latitude=111.3'))
            output = search(r'.*-.*-.*-.*$', f.getvalue()).group()
            truncate_string_io(f)
            HBNBCommand().onecmd(f"show Place {output}")
            self.assertTrue("'name': 'Tiny Home'" in f.getvalue())
            self.assertTrue("'guests': 2" in f.getvalue())
            self.assertTrue("'latitude': 111.3" in f.getvalue())


@skipIf(getenv('HBNB_TYPE_STORAGE') != 'db',
        'Tests for db storage')
class TestPlaceStateDb(TestCase):
    """ Unittest for db integration into hbnb console
    """
    def test_states_and_cities(self):
        with patch('sys.stdout', new=StringIO()) as f:
            # test successful creation of state instances
            HBNBCommand().onecmd('create State name="Uganda"')
            output = search(r'.*-.*-.*-.*$', f.getvalue()).group()
            self.assertEqual(f"{output}\n", f.getvalue())
            truncate_string_io(f)

            # test relationship of city and state
            HBNBCommand().onecmd('create State name="Kenya"')
            state_id = search(r'.*-.*-.*-.*$', f.getvalue()).group()
            self.assertEqual(f"{state_id}\n", f.getvalue())
            truncate_string_io(f)

            HBNBCommand().onecmd(
                    f'create City name="Nairobi" state_id="{state_id}"')
            city1_id = search(r'.*-.*-.*-.*$', f.getvalue()).group()
            self.assertEqual(f"{city1_id}\n", f.getvalue())
            records_1 = storage.all(City)
            self.assertTrue(len(records_1) >= 1)
            truncate_string_io(f)

            HBNBCommand().onecmd(
                    f'create City name="Mombasa" state_id="{state_id}"')
            city2_id = search(r'.*-.*-.*-.*$', f.getvalue()).group()
            self.assertEqual(f"{city2_id}\n", f.getvalue())
            records_2 = storage.all(City)
            self.assertEqual(len(records_2) - len(records_2), 1)
            truncate_string_io(f)


def truncate_string_io(str_io):
    """ Method to truncate string input output object and
        reset the read position to the beginining of the file
    """
    str_io.truncate(0)
    str_io.seek(0)
