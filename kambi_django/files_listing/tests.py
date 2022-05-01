import json

import mock

from django.test import Client, TestCase
from django.urls import reverse

from . import utilities
from .models import list_files


class UtilitiesTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_utilities_clean(self):
        input = b"foo\nbar\n"
        cleaned = utilities.clean(input)
        self.assertEqual(cleaned, ['foo', 'bar'])

        input = b""
        cleaned = utilities.clean(input)
        self.assertEqual(cleaned, [])

    @mock.patch('kambi_django.files_listing.utilities.clean')
    def test_utilites_to_dict_error(self, mock_clean_error):
        mock_clean_error.return_value = "my error"
        output = b"output"
        error = b"error"
        dct = utilities.to_dict(output, error)
        self.assertEqual(dct.get('output'), None)
        self.assertEqual(dct.get('error'), "my error")

    @mock.patch('kambi_django.files_listing.utilities.clean')
    def test_utilites_to_dict(self, mock_clean_output):
        mock_clean_output.return_value = "my output"
        output = b"output"
        error = b""
        dct = utilities.to_dict(output, error)
        self.assertEqual(dct.get('output'), "my output")
        self.assertEqual(dct.get('error'), None)

    def test_list_files(self):
        output, error = list_files()
        self.assertTrue(output)
        self.assertFalse(error)


class FileListingTest(TestCase):
    @mock.patch('kambi_django.files_listing.models.run_find')
    def test_list_files_name(self, mock_run_find):
        list_files(name='foo')
        mock_run_find.assert_called_once()

    @mock.patch('kambi_django.files_listing.models.run_find')
    def test_list_files_name_and_params(self, mock_run_find):
        list_files(name='foo', params='bar')
        mock_run_find.assert_called_once()

    @mock.patch('kambi_django.files_listing.models.run_find')
    def test_list_files_params(self, mock_run_find):
        list_files(params='bar')
        mock_run_find.assert_called_once()

    @mock.patch('kambi_django.files_listing.models.run_ls')
    def test_list_files(self, mock_run_ls):
        list_files()
        mock_run_ls.assert_called_once()

    # TODO
    def test_run_ls(self):
        pass

    # TODO
    def test_run_find(self):
        pass


class FileListingViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    @mock.patch('kambi_django.files_listing.views.list_files')
    @mock.patch('kambi_django.files_listing.utilities.to_dict')
    def test_list_files_view(self, mock_to_dict, mock_list_files):
        mock_list_files.return_value = (b"['foo', 'bar']", b"")
        mock_to_dict.return_value = {
            'output': ['foo', 'bar']
        }
        response = self.client.get('/files/files/')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data.get('output'), ['foo', 'bar'])