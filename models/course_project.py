from .deadline import Deadline 
from typing import Dict, List
from .research import Research
class Course_project:
    def __init__(self, deadlines: List[str])->None:
        self._theme: str = ''
        self._text: List[str] = []
        self._deadlines: Dict[int,Deadline] = {}
        self._work_plan: Dict[str,str] = {}
        number_of_deadline = 1
        for date in deadlines:
            deadline = Deadline(date)
            self._deadlines[number_of_deadline] = deadline
            number_of_deadline += 1

         
    def set_theme (self,theme: str)->None:
        self._theme=theme
    def set_text(self,new_text: str)->None:
        self._text.append(new_text)
    def edit_text(self, str_to_remove: str)->None:
        for sentence in self._text:
            if str_to_remove in sentence:
                str_to_remove=sentence
        try:
            self._text.remove (str_to_remove)
        except ValueError:
            print('No such sentences in text')
    
        
    def set_work_plan(self,item_number: str, subtask: str)->None:
        self._work_plan[item_number]=[subtask]

    