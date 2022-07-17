import threading


class Timer:
    def __init__(self, timeout, callback, server_id, server_type, purpose='election'):
        self.timeout = timeout
        self.callback = callback
        self.server_id = server_id
        self.server_type = server_type
        self.purpose = purpose
        self.running = False

    def start(self):
        self.timer = self.create_timer()
        self.running = True
        self.timer.start()
        #print(f"********* Timer STARTED for {self.server_id} of type {self.server_type} for purpose {self.purpose} *********")

    def create_timer(self):
        timer = threading.Timer(self.timeout, self.run)
        timer.daemon = True
        return timer

    def run(self):
        #print(f"********* Timer TRIGGERED for {self.server_id} of type {self.server_type} for purpose of {self.purpose} *********")
        self.callback()
        if self.running:
            self.timer = self.create_timer()
            self.timer.start()

    def stop(self):
        #print(f"********* Timer STOPPED for {self.server_id} of type {self.server_type} for purpose of {self.purpose} *********")
        self.running = False
        self.timer.cancel()

    def reset(self):
        #print(f"********* Timer RESETTING for {self.server_id} of type {self.server_type} for purpose of {self.purpose} *********")
        self.stop()
        self.start()
