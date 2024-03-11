'''
    This file is used to validate the input of the user
    - check_username: check the username
    - check_fullname: check the fullname
    - check_email: check the email
    - check_phone: check the phone
    - check_password: check the password
    - check_birthday: check the birthday
    - check_address: check the address
    - check_all_field: check all the field in the form
    - uncheck_all_field: uncheck all the field in the form
    - state_validate: store the state of the validation
    - base_master: store the master of the form
'''
from ttkbootstrap.validation import (
    add_numeric_validation,
    add_text_validation,
    add_option_validation,
    add_phonenumber_validation,
    add_range_validation,
    add_regex_validation,
    add_validation,
    validator,
    ValidationEvent,
)
import ttkbootstrap as tb
from datetime import datetime



# When = focus, focusin, focusout

# Add validation to a widget
class FormValidation:
    base_master = None
    state_validate = {}
    
    @staticmethod
    def check_all_field(widget_fields):
        for widget in widget_fields:
            if widget["label"] == "fullname":
                add_validation(widget["widget"], FormValidation.check_fullname)
            if widget["label"] == "phone":
                add_validation(widget["widget"], FormValidation.check_phone)
            if widget["label"] == "birthday":
                # ...
                add_validation(widget["widget"].entry, FormValidation.check_birthday)
            if widget["label"] == "email":
                add_validation(widget["widget"], FormValidation.check_email)
            if widget["label"] == "address":
                add_validation(widget["widget"], (lambda *event, label=widget["label"]: FormValidation.check_blank(*event, label=label)))
            if widget["label"] == "cmnd":
                add_validation(widget["widget"], (lambda *event, label=widget["label"]: FormValidation.check_blank(*event, label=label)))
            if widget["label"] == "sex":
                add_validation(widget["widget"], (lambda *event, label=widget["label"]: FormValidation.check_blank(*event, label=label)))

    
    @staticmethod
    def uncheck_all_field(widget_fields):
        for widget in widget_fields:
            FormValidation.base_master.lbl_frame_reg[widget['label']].config(text=widget['name_label'], bootstyle='primary')

    @staticmethod
    @validator
    def check_blank(event: ValidationEvent, label: str):
        print(event.postchangetext, label)
        notice_check = ""
        notice_right = "Cảm ơn bạn đã điền\n"
        notice_check += "Không được để rỗng\n" if str(event.postchangetext).__len__() == 0 else ""
        
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg[label].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate[label] = False
            return False
        FormValidation.base_master.lbl_frame_reg[label].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate[label] = True
        return True

    @staticmethod
    @validator
    def check_username(event: ValidationEvent):
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
        def check_regex(regex, text):
            import re
            # xxx-xxxx-xxx
            return re.match(regex, text)==None
        def check_numeric(text):
            return "".join(text.split("-")).isnumeric()
        notice_check = ""
        notice_right = "Số điện thoại hợp lệ\n"
        notice_check += "Số điện thoại không được để trống\n" if " " in event.postchangetext else ""
        notice_check += "Số điện thoại phải có dạng xxx-xxxx-xxx\n" if check_regex(r"^\d{3}-\d{4}-\d{3}$", event.postchangetext) else ""
        notice_check += "Số điện thoại không phải số\n" if not check_numeric(event.postchangetext) else ""
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
    
    @staticmethod
    @validator
    def check_birthday(event: ValidationEvent):
        notice_check = ""
        notice_right = "Ngày sinh hợp lệ\n"
        conv_date = datetime.strptime(event.postchangetext, '%m/%d/%Y')
        notice_check += "Ngày sinh không được để trống\n" if " " in event.postchangetext else ""
        # age > 17
        notice_check += "Ngày sinh không được <= 18\n" if (datetime.now()-conv_date).days//365 < 18 else ""
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg['birthday'].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate['birthday'] = False
            return False
        FormValidation.base_master.lbl_frame_reg['birthday'].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate['birthday'] = True
        return True
    

    @staticmethod
    @validator
    def check_address(event: ValidationEvent):
        notice_check = ""
        notice_right = "Địa chỉ hợp lệ\n"
        notice_check += "Địa chỉ không được để trống\n" if " " in event.postchangetext else ""
        notice_check += "Địa chỉ ít nhất 6 ký tự\n" if len(event.postchangetext) < 6 else ""
        notice_check += "Địa chỉ không quá 20 ký tự\n" if len(event.postchangetext) > 20 else ""
        if notice_check!="":
            FormValidation.base_master.lbl_frame_reg['address'].config(text=notice_check, bootstyle='danger')
            FormValidation.state_validate['address'] = False
            return False
        FormValidation.base_master.lbl_frame_reg['address'].config(text=notice_right, bootstyle='success')
        FormValidation.state_validate['address'] = True
        return True
    

