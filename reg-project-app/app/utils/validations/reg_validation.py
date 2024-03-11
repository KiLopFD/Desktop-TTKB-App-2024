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
from app.types.main import *

class RegValidation:
    base_master = None
    state_validate = {}

    @staticmethod
    @validator
    def check_count_member(event: ValidationEvent):
        notice_check = ""
        notice_right = "Số lượng thành viên hợp lệ\n"
        notice_check += "Số lượng thành viên không được để trống\n" if event.postchangetext == "" else ""
        notice_check += "Số lượng thành viên phải là số\n" if not event.postchangetext.isdigit() else ""
        notice_check += "Số lượng thành viên phải lớn hơn 0\n" if int(event.postchangetext) <= 0 else ""
        if notice_check!="":
            RegValidation.base_master.lbl_frame_reg['count_member'].config(text=notice_check, bootstyle='danger')
            RegValidation.state_validate['count_member'] = False
            return False
            
        RegValidation.base_master.lbl_frame_reg['count_member'].config(text=notice_right, bootstyle='success')
        RegValidation.state_validate['count_member'] = True
        return True