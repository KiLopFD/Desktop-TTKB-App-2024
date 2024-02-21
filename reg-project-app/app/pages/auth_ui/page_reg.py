import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime
from app.db.setup import Account
from app.utils.validations.form_validation import FormValidation
from ttkbootstrap.toast import ToastNotification


class PageReg(tb.Frame):

    def __init__(self, master, base_master,**kwargs):
        super().__init__(master, **kwargs, bootstyle='dark', padding=10)
        self.master = master
        self.base_master = base_master
        self.pack(expand=True, fill=tb.BOTH)
        # Set base master
        #--------------------------------
        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Login Group
        frame_log = tb.Frame(self)
        frame_log.pack(fill=X, pady=30, side=TOP)
        # Create Global Label Frame For Each Field Using Base Master
        self.base_master.lbl_frame_reg = {}
        #--------------------------------
        for field in self.base_master.reg_input_fields:
            lbl_frame = tb.LabelFrame(frame_log, text=field['name'])
            lbl_frame.pack(fill=X, pady=4)
            # Update the label frame to the base master
            self.base_master.lbl_frame_reg[field['label']] = lbl_frame
            #--------------------------------
            if field['label'] == 'phone':
                self.create_menu_phone(lbl_frame)
                field['widget'] = tb.Entry(lbl_frame, textvariable=field['var'])
                field['widget'].pack(fill=X, padx=5, pady=5)
                continue
            elif field['label'] == 'birthday':
                field['widget'] = tb.DateEntry(lbl_frame)
                field['widget'].pack(fill=X, padx=5, pady=5)
                continue
            field['widget'] = tb.Entry(lbl_frame, textvariable=field['var'])
            field['widget'].pack(fill=X, padx=5, pady=5)

        # Action Group
        frame_action = tb.Frame(self)
        frame_action.pack(fill=X, pady=10, side=TOP)
        frame_center = tb.Frame(frame_action)
        frame_center.pack()
        btn_login = tb.Button(frame_center, text='Đăng Nhập', bootstyle='secondary', command=lambda: self.base_master.nb.select(0))
        btn_login.pack(side=LEFT, padx=5)
        btn_register = tb.Button(frame_center, text='Đăng Ký', bootstyle='primary', command=self.reg_account)
        btn_register.pack(side=LEFT, padx=5)

        # Footer Group
        frame_footer = tb.Frame(self)
        frame_footer.pack(fill=X, pady=10, side=BOTTOM)
        lbl_footer = tb.Label(frame_footer, text='Chào mừng bạn quay lại')
        lbl_footer.pack()

        # Validation
        FormValidation.base_master = self.base_master
        FormValidation.check_all_field(self.base_master.get_all_reg_widgets())


    def create_menu_phone(self, master):
        self.menubutton = tb.Menubutton(master, text='+84')
        list_phone = ['+84', '+1', '+81', '+82', '+86', '+82']
        self.menubutton.menu = tb.Menu(self.menubutton, tearoff=0)
        self.menubutton['menu'] = self.menubutton.menu
        for phone in list_phone:
            self.menubutton.menu.add_command(label=phone, command=lambda phone=phone: self.set_phone(phone))
        self.selected_phone = tb.StringVar()
        self.menubutton.pack(side=LEFT, padx=5)

    def set_phone(self, phone):
        self.selected_phone.set(phone)
        self.menubutton.config(text=phone)
        print(self.selected_phone.get())

    def reg_account(self):
        if False in FormValidation.state_validate.values():
            ToastNotification(
                title='Thông Báo',
                message='Vui lòng kiểm tra lại thông tin',
                duration=3000,
                bootstyle='danger',
                alert=True,
            ).show_toast()
            return
        account = Account(
            username=self.base_master.reg_input_fields[0]['var'].get(),
            fullname=self.base_master.reg_input_fields[1]['var'].get(),
            email=self.base_master.reg_input_fields[2]['var'].get(),
            phone=self.selected_phone.get() + self.base_master.reg_input_fields[3]['var'].get(),
            birthday=datetime.strptime(self.base_master.reg_input_fields[4]['widget'].entry.get(), '%m/%d/%Y'),
            password=self.base_master.reg_input_fields[5]['var'].get(),
            role='user'
        )
        self.base_master.account_dao.add(account)
        # Reset all fields
        for field in self.base_master.reg_input_fields:
            field['var'].set('')
            self.base_master.lbl_frame_reg[field['label']].config(text=field['name'], bootstyle='default')
        self.base_master.nb.select(0)
        print('Registed', account)



