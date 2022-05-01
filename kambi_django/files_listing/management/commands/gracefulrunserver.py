import os
import signal

from django.core.management.commands import runserver
from django.core.servers.basehttp import WSGIServer


class Command(runserver.Command):
    help = 'Closes the specified poll for voting'

    def __init__(self, *args, **kwargs):
        self.wsgi_servers = []
        command_instance = self
        super().__init__(*args, **kwargs)

        class MyWSGIServer(WSGIServer):
            def __init__(self, *args, **kwargs):
                command_instance.wsgi_servers.append(self)
                return super().__init__(*args, **kwargs)

    def server_cls(self, *args, **kwargs):
        server = WS

    def handle(self, *args, **options):
        print("Running gracefully terminable runserver")
        signal.signal(signal.SIGINT, self._sigint_handler)
        print(f"PID: {os.getpid()}")
        print("Graceful")
        super().handle(*args, **options)

    def _sigint_handler(self):
        for server in self.wsgi_servers:
            pass
