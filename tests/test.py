import unittest
from unittest.mock import patch, call
import sys
import os

# Add the parent directory to sys.path to import main correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import main
import subprocess

class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.mock_flatpak_list = "LibreOffice\torg.libreoffice.LibreOffice\t24.2.4.2\tstable\tflathub\tsystem\n"

    @patch('main.create_alias')
    @patch('subprocess.run')
    def test_single_app_alias_creation(self, mock_run, mock_create_alias):
        mock_run.return_value.stdout = self.mock_flatpak_list
        main.main()
        mock_create_alias.assert_called_once_with({'libreoffice': 'org.libreoffice.LibreOffice'})

    @patch('main.create_alias')
    @patch('subprocess.run')
    def test_special_cases_alias_creation(self, mock_run, mock_create_alias):
        mock_run.return_value.stdout = "Bitwarden\tcom.bitwarden.desktop\t2024.6.1\tstable\tflathub\tsystem\n"
        main.main()
        mock_create_alias.assert_called_once_with({'bw': 'com.bitwarden.desktop'})

    @patch('main.create_alias')
    @patch('subprocess.run')
    def test_no_apps_installed(self, mock_run, mock_create_alias):
        mock_run.return_value.stdout = ""
        main.main()
        mock_create_alias.assert_not_called()

    @patch('main.create_alias')
    @patch('subprocess.run')
    def test_multiple_app_alias_creation(self, mock_run, mock_create_alias):
        mock_run.return_value.stdout = "App1\tcom.app1\t1.0\tstable\tflathub\tsystem\nApp2\tcom.app2\t2.0\tstable\tflathub\tsystem\n"
        main.main()
        mock_create_alias.assert_called_once_with({'app1': 'com.app1', 'app2': 'com.app2'})

    @patch('main.create_alias')
    @patch('subprocess.run')
    def test_empty_flatpak_list(self, mock_run, mock_create_alias):
        mock_run.return_value.stdout = "\n"
        main.main()
        mock_create_alias.assert_not_called()

if __name__ == '__main__':
    unittest.main()
