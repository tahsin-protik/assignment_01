class Bad_format_of_data(Exception):
   
    def __init__(self, status="400", message="Bad Format of Data"):
        self.status = status
        self.message = message
        super().__init__(self.message)