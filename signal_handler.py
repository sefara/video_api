import signal

class SignalHandler:
    shutdown_requested = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.request_shotdown)
        signal.signal(signal.SIGTERM, self.request_shotdown)

    def request_shotdown(self,*args):
        print ("Request to shutdown")
        self.shutdown_requested = True

    def can_run(self):
        return not self.shutdown_requested