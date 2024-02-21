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



# When = focus, focusin, focusout

# Add validation to a widget
class FormValidation:
    base_master = None
    state_validate = {}
    
    @staticmethod
    def check_all_field(widget: RegInputFieldType):
        for key in widget:
            if key == 'username':
                add_validation(widget[key], FormValidation.validate_username)
            if key == 'fullname':
                add_validation(widget[key], FormValidation.check_fullname)
            if key == 'email':
                add_validation(widget[key], FormValidation.check_email)
            if key == 'phone':
                add_validation(widget[key], FormValidation.check_phone)
            if key == 'password':
                add_validation(widget[key], FormValidation.check_password)

    
    @staticmethod
    @validator
    def validate_username(event: ValidationEvent):
        notice_check = ""
        notice_right = "Tên đăng nhập hợp lệ\n"
        notice_check += "Tên đăng nhập không được để trống\n" if " " in event.postchangetext else ""
        notice_check += "Tên đăng nhập ít nhất 6 ký tự\n" if len(event.postchangetext) < 6 else ""
        notice_check += "Tên đăng nhập không quá 20 ký tự\n" if len(event.postchangetext) > 20 else ""
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg['username'].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate['username'] = False
            return False
            
        FormValidation.base_master.lbl_frame_reg['username'].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate['username'] = True
        return True
    
    @staticmethod
    @validator
    def check_fullname(event: ValidationEvent):
        notice_check = ""
        notice_right = "Họ và tên hợp lệ\n"
        notice_check += "Họ và tên phải chứa khoảng cách và ghi hoa chữ cái đầu\n" if " " not in event.postchangetext else ""
        notice_check += "Họ và tên ít nhất 6 ký tự\n" if len(event.postchangetext) < 6 else ""
        notice_check += "Họ và tên không quá 20 ký tự\n" if len(event.postchangetext) > 20 else ""
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg['fullname'].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate['fullname'] = False
            return False
        FormValidation.base_master.lbl_frame_reg['fullname'].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate['fullname'] = True
        return True
    
    @staticmethod
    @validator
    def check_email(event: ValidationEvent):
        notice_check = ""
        notice_right = "Email hợp lệ\n"
        notice_check += "Email không được để trống\n" if " " in event.postchangetext else ""
        notice_check += "Email không hợp lệ\n" if "@" not in event.postchangetext else ""
        notice_check += "Email ít nhất 6 ký tự\n" if len(event.postchangetext) < 6 else ""
        notice_check += "Email không quá 20 ký tự\n" if len(event.postchangetext) > 20 else ""
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg['email'].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate['email'] = False
            return False
        FormValidation.base_master.lbl_frame_reg['email'].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate['email'] = True
        return True
    
    @staticmethod
    @validator
    def check_phone(event: ValidationEvent):
        notice_check = ""
        notice_right = "Số điện thoại hợp lệ\n"
        notice_check += "Số điện thoại không được để trống\n" if " " in event.postchangetext else ""
        notice_check += "Số điện thoại không hợp lệ\n" if not str(event.postchangetext).isnumeric() else ""
        notice_check += "Số điện thoại phải đúng 10 số\n" if len(event.postchangetext) != 10 else ""
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg['phone'].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate['phone'] = False
            return False
        FormValidation.base_master.lbl_frame_reg['phone'].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate['phone'] = True
        return True
    
    @staticmethod
    @validator
    def check_password(event: ValidationEvent):
        notice_check = ""
        notice_right = "Mật khẩu hợp lệ\n"
        notice_check += "Mật khẩu không được để trống\n" if " " in event.postchangetext else ""
        notice_check += "Mật khẩu ít nhất 6 ký tự\n" if len(event.postchangetext) < 6 else ""
        notice_check += "Mật khẩu không quá 20 ký tự\n" if len(event.postchangetext) > 20 else ""
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg['password'].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate['password'] = False
            return False
        FormValidation.base_master.lbl_frame_reg['password'].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate['password'] = True
        return True
    

