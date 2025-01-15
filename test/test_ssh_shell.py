import unittest
from unittest.mock import MagicMock, patch, call
import paramiko
from src.ssh_shell.ssh_shell import ssh_to_client


class TestSSHToClient(unittest.TestCase):

    def setUp(self):
        self.creds = MagicMock()
        self.creds.username = "test_user"
        self.creds.hostname = "test_host"
        self.creds.password = "test_pass"
        self.creds.port = 22

        self.ssh_client_mock = MagicMock()
        self.ssh_obj = ssh_to_client(self.creds)

    @patch('paramiko.SSHClient')
    @patch('paramiko.AutoAddPolicy')
    def test_create_ssh_connection(self, mock_auto_add_policy, mock_ssh_client):
        mock_ssh_client.return_value = self.ssh_client_mock
        mock_policy_instance = MagicMock()
        mock_auto_add_policy.return_value = mock_policy_instance

        client = self.ssh_obj.create_ssh_connection()

        mock_ssh_client.assert_called_once()
        self.ssh_client_mock.load_system_host_keys.assert_called_once()
        self.ssh_client_mock.set_missing_host_key_policy.assert_called_once_with(mock_policy_instance)
        self.ssh_client_mock.connect.assert_called_once_with(
            hostname="test_host",
            username="test_user",
            password="test_pass",
            port=22
        )
        self.assertEqual(client, self.ssh_client_mock)

    @patch('paramiko.SSHClient')
    @patch('sys.stdout', new_callable=MagicMock)
    @patch('builtins.input', side_effect=["exit"])
    @patch('time.sleep', return_value=None)  # Prevent actual sleep
    def test_invoke_interactive_ssh_shell(self, mock_sleep, mock_input, mock_stdout, mock_ssh_client):
        mock_stdout.encoding = "utf-8" 
        mock_ssh_client.return_value = self.ssh_client_mock

        shell_mock = MagicMock()
        shell_mock.recv_ready.side_effect = [True, False]
        shell_mock.recv.return_value = b"Test output"
        self.ssh_client_mock.invoke_shell.return_value = shell_mock

        self.ssh_obj.invoke_interactive_ssh_shell()

        mock_ssh_client.assert_called_once()
        self.ssh_client_mock.invoke_shell.assert_called_once()
        shell_mock.send.assert_called_once_with("uname -a\n")
        shell_mock.recv_ready.assert_called()
        shell_mock.recv.assert_called_with(9999)

    def test_delete_method(self):
        self.ssh_obj.__delete__(self.ssh_client_mock)
        self.ssh_client_mock.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
