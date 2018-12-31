class BaseHandler:
    def __init__(self, connection, client_address):
        self.connection = connection
        self.client_address = client_address

        try:
            self.setup()
            self.handle()
        except:
            raise
        finally:
            self.end()

    def setup(self):
        pass

    def handle(self):
        pass

    def end(self):
        pass