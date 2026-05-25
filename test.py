import unittest
import threading
import client
import server_abfrage
host = '192.168.178.31'
port = 10000


class TestIntegration(unittest.TestCase):
    def test_client_server_communication(self):
        # 1. Server in einem separaten Hintergrund-Thread starten
        server_thread = threading.Thread(
            target=server_abfrage.server,
            args=(host, port),
            daemon=True
        )
        server_thread.start()

        # 2. Client im Haupt-Thread ausführen und Ergebnis prüfen
        result = client.client(host, port)
        self.assertEqual(result, 0)


if __name__ == '__main__':
    unittest.main()
