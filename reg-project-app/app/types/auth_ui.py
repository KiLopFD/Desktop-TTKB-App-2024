'''
    This file contains the type definitions for the authentication UI
'''
#---------------------------------IMPORTS------------------------------------#
from typing import *
import ttkbootstrap as tb

RegInputFieldType = NewType(
    'RegInputFieldType', 
    Dict[Literal['username', 'fullname', 'email', 'phone', 'birthday', 'password'], Union[tb.Entry]]
    )

