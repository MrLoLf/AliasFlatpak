import unittest
from unittest.mock import patch
import main

class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.mock_flatpak_list = "Ref\tName\tBranch\tArch\tInstalledSize\tOrigin\tInstallation\ncom.spotify.Client\tSpotify\tstable\tx86_64\t1.2 GB\tsystem\n"

    @patch('subprocess.run')
    def test_single_app_alias_creation(self, mock_run):
        mock_run.return_value.stdout = self.mock_flatpak_list
        main.main()
        mock_run.assert_called_with(['bash', '-c', 'alias spotify="flatpak run com.spotify.Client"'], check=True)

    @patch('subprocess.run')
    def test_special_cases_alias_creation(self, mock_run):
        mock_run.return_value.stdout = "Ref\tName\tBranch\tArch\tInstalledSize\tOrigin\tInstallation\ncom.bitwarden.desktop\tBitwarden\tstable\tx86_64\t1.2 GB\tsystem\n"
        main.main()
        mock_run.assert_called_with(['bash', '-c', 'alias bw="flatpak run com.bitwarden.desktop"'], check=True)

    @patch('subprocess.run')
    def test_no_apps_installed(self, mock_run):
        mock_run.return_value.stdout = "Ref\tName\tBranch\tArch\tInstalledSize\tOrigin\tInstallation\n"
        main.main()
        mock_run.assert_not_called()

if __name__ == '__main__':
    unittest.main()