import unittest
import gzip
from io import StringIO
from unittest.mock import patch
from package_stats import download_contents, get_top_packages, output_stats


class PackageStatisticsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sample_contents = """
            file1 package1
            file2 package1
            file3 package2
            file4 package2
            file5 package2
            file6 package2
            file7 package3
            file8 package3
            file9 package3
            file10 package4
            file11 package4
            file12 package4
            file13 package4
            file14 package4
            file15 package4
        """

    def test_download_contents(self):
        with patch("urllib.request.urlopen") as mock_urlopen:
            expected_contents = "file1 package1\nfile2 package1\nfile3 package2"
            mock_urlopen.return_value.read.return_value = gzip.compress(expected_contents.encode("utf-8"))

            contents = download_contents("amd64")

            mock_urlopen.assert_called_once_with("http://ftp.uk.debian.org/debian/dists/stable/main/Contents-amd64.gz")
            self.assertEqual(contents, expected_contents)

    def test_get_top_packages(self):
        contents = 'file1 package1\nfile2 package2\nfile3 package1\nfile4 package2\nfile5 package2\nfile6 package3\n'
        expected_top_packages = [('package2', 3), ('package1', 2), ('package3', 1)]
        top_packages = get_top_packages(contents)

        self.assertEqual(top_packages, expected_top_packages)

    def test_output_stats(self):
        top_packages = [('package2', 3), ('package1', 2), ('package3', 1)]
        expected_output = """Top 10 packages:
1. package2 3
2. package1 2
3. package3 1
"""
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            output_stats(top_packages)
            self.assertEqual(mock_stdout.getvalue(), expected_output)
