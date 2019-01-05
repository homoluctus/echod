class BaseHandler:
    def __init__(self, connection, client_address):
        self.connection = connection
        self.client_address = client_address

        try:
            self.process()
        except:
            raise

    def process(self):
        pass
