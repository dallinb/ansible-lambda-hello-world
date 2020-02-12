import unittest
import testinfra

from parameterized import parameterized


class TestLocalStack(unittest.TestCase):

    def setUp(self):
        self.host = testinfra.get_host('docker://localstack')

    @parameterized.expand([
        ('iam', 4593),
        ('lambda', 4574),
        ('s3', 4572)
    ])
    def test_running_mocks(self, service, port):
        host = self.host
        msg = f'The {service} service on localstack is not listening.'
        self.assertTrue(host.socket(f'tcp://{port}'), msg)
