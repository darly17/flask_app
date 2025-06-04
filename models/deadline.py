class Deadline:
    def __init__(self, date: str)->None:
        self._deadline= date
    
    def on_time(self)->bool:
        return True
