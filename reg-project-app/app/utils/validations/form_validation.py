from ttkbootstrap.validation import (
    add_numeric_validation,
    add_text_validation,
    add_option_validation,
    add_phonenumber_validation,
    add_range_validation,
    add_regex_validation,
    add_validation,
    validator,
    ValidationEvent
)

import ttkbootstrap as tb



# Add validation to a widget

class FormValidation:
    master = None
    
    @staticmethod
    def check_username(widget):
        @validator
        def validate_text(event: ValidationEvent):
            if ' ' in event.postchangetext:
                return False
            return True

        add_validation(widget, validate_text)
