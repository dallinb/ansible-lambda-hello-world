import json
import testinfra
import unittest


class TestLocalHelloWorld(unittest.TestCase):

    def setUp(self):
        self.host = testinfra.get_host('docker://localstack')

    def test_bucket_present(self):
        host = self.host
        cmd = host.run('awslocal s3 ls mys3bucket')
        self.assertEqual(cmd.rc, 0)

    def test_zip_uploaded(self):
        host = self.host
        url = 's3://mys3bucket/lambdas/HelloWorldFunction.zip'
        cmd = host.run(f'awslocal s3 ls {url}')
        self.assertEqual(cmd.rc, 0)

    def test_function_present(self):
        host = self.host
        function_name = 'HelloWorld'
        function_found = False

        cmd = host.run(
            'awslocal lambda --region eu-west-2 list-functions --output json'
        )
        self.assertEqual(cmd.rc, 0)
        functions_list = json.loads(cmd.stdout)
        self.assertIn('Functions', functions_list)
        self.assertNotEqual(functions_list['Functions'], [])

        for function in functions_list['Functions']:
            if function['FunctionName'] == function_name:
                function_found = True

        self.assertTrue(function_found)

    def test_role_present(self):
        host = self.host
        role_name = 'lambda-ex'
        role_found = False

        cmd = host.run('awslocal iam list-roles --output json')
        self.assertEqual(cmd.rc, 0)
        roles_list = json.loads(cmd.stdout)
        self.assertIn('Roles', roles_list)
        self.assertNotEqual(roles_list['Roles'], [])

        for role in roles_list['Roles']:
            if role['RoleName'] == role_name:
                role_found = True

        self.assertTrue(role_found)
