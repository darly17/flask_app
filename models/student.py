import json
import os
from pathlib import Path
from .course_project import Course_project
from .professor import Professor
from typing import Dict, List
from .research import Research

class Student :
    THEME_FILE = r"C:\Users\user\Desktop\dasha\Учеба\PPOIS2\APP\data_bases\theme.json"
    INFO_FILE= r"C:\Users\user\Desktop\dasha\Учеба\PPOIS2\APP\data_bases\info.json"
    def __init__(self, name: str, age: int, group: str, number: str )->None:
        self._name= name
        self._age= age
        self._group= group
        self._student_number= number
        self._info_for_cp : Dict[str,str]={}
        self._analysed_info_for_cp : Dict[str,str]={}

    
    def choose_theme ( self, course_project: Course_project)-> None: 
        try:
            with open(self.THEME_FILE, 'r', encoding='utf-8') as theme_file:
                theme_list= json.load(theme_file)
        except json.JSONDecodeError:
            print("Opening error")
        course_project.set_theme(theme_list[self._student_number])
    
    def edit_plan(self,course_project: Course_project,item_number: str, text: str)->None:
        
        if  not item_number.strip():
            print("You enter no text")
        else:
            course_project.set_work_plan(item_number,text)
            print("plan of work now:",course_project._work_plan)


    def get_information(self)->None:
        try:
            with open(self.INFO_FILE, 'r', encoding='utf-8') as info_file:
                self._info_for_cp= json.load(info_file)
        except json.JSONDecodeError:
            print("Opening error")

    def analyse_information(self,course_project: Course_project)->None:
        for article_theme in self._info_for_cp:
            if course_project._theme in article_theme :
                self._analysed_info_for_cp[article_theme]=self._info_for_cp[article_theme]
    
    
    def write_text(self,course_project: Course_project)->None:
        for article_theme in self._analysed_info_for_cp:
            course_project.set_text(self._analysed_info_for_cp[article_theme])

    def edit_text(self,course_project: Course_project,str_to_remove: str)->None:
        course_project.edit_text(str_to_remove)
    
    def consultation_with_professor(self,professor: Professor,research: Research)->None:
        for question in research._questions:
            research._answers[question]=professor.answer_question(question)
    def pass_corse_project(self,professor: Professor,course_project: Course_project)->bool:
        return professor.accept_course_project(course_project)

    
    

        



        