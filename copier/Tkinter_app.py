import tkinter
import tkinter.messagebox
from datetime import date
from datetime import timedelta
import concurrent.futures
from copier.crimsion_intereq import crimsion_intereq_selenium
from copier.canon_IR5540_Extract import extract_copier_canon_ir5540 
from copier.canon_IR3320_Extract import extract_copier_canon_ir3320
from copier.ricoh_C3503_Extract import extract_copier_ricoh_c3503
from copier.Toshiba_5015AC_Extract import extract_copier_toshiba_5015ac
import customtkinter

# customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
# customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

function_desc_dict ={
    "extract_all_copier_monthly": "export Cannon C3320, Canon C5540, Ricoh C3503, Toshiba 5015AC printing records.",
    "zerolize_all_copier_monthly": "zerolize Cannon C3320, Canon C5540, Toshiba 5015AC printing records. DO ZEROLIZE RICOH REPORT MANUALLY",
    "submit_outstanding_crimsion_sec47": "Extract All pdf cert under folder 99999 - CONSOLIDATION\CRIMSON SEC 47\SECTION 47C REPLY",
    "extract_monthly_crimision_billing_report": "Extract monthy crimision report and save under 99999 - CONSOLIDATION\CRIMSON SEC 47\CRIMSON LOGIC BILLING.xlsx",

}

function_group_list ={
    "Copier Extract": ["extract_all_copier_monthly","zerolize_all_copier_monthly"],
    "Crimision Logic": ["submit_outstanding_crimsion_sec47","extract_monthly_crimision_billing_report"]
}

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        
        self.title("Smartyware Extraction")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.desc_text = list(function_desc_dict.values())[0]
        self.function_selected = list(function_group_list.keys())[0]

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        self.radio_var = tkinter.IntVar(value=0)
        
        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Function Options")
        self.label_radio_group.grid(row=4, column=0, columnspan=1, pady=5, padx=5, sticky="")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           text = function_group_list[self.function_selected][0],
                                                           value=0, command=self.change_radio_option)
        self.radio_button_1.grid(row=5, column=0, pady=5, padx=5, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           text = function_group_list[self.function_selected][1],
                                                           value=1, command=self.change_radio_option)
        self.radio_button_2.grid(row=6, column=0, pady=5, padx=5, sticky="n")

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Function",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)
        self.radio_function_var = tkinter.IntVar(value=0)
        self.label_radio_function_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Function Options")
        self.label_radio_function_group.grid(row=4, column=0, columnspan=1, pady=5, padx=5, sticky="")
        self.button_1 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                variable= self.radio_function_var,
                                                value=0,
                                                text="Copier Extract",
                                                # fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.change_function_button)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkRadioButton(master=self.frame_left,
                                                variable= self.radio_function_var,
                                                value=1,
                                                text="Crimision Logic",
                                                # fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.change_function_button)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        # self.button_3 = customtkinter.CTkButton(master=self.frame_left,
        #                                         text="CTkButton 3",
        #                                         fg_color=("gray75", "gray30"),  # <- custom tuple-color
        #                                         command=self.button_event)
        # self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left)
        self.switch_1.grid(row=9, column=0, pady=10, padx=20, sticky="w")

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text = self.desc_text,
                                                   height=100,
                                                   wraplength=300,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        # self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        # self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

        # ============ frame_right ============


        # self.radio_button_3 = customtkinter.CTkRadioButton(master=self.frame_right,
        #                                                    variable=self.radio_var,
        #                                                    value=2)
        # self.radio_button_3.grid(row=7, column=0, pady=5, padx=5, sticky="n")
  


        
        # self.slider_1 = customtkinter.CTkSlider(master=self.frame_right,
        #                                         from_=0,
        #                                         to=1,
        #                                         number_of_steps=3,
        #                                         command=self.progressbar.set)
        # self.slider_1.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        # self.slider_2 = customtkinter.CTkSlider(master=self.frame_right,
        #                                         command=self.progressbar.set)
        # self.slider_2.grid(row=5, column=0, columnspan=2, pady=10, padx=20, sticky="we")

        # self.slider_button_1 = customtkinter.CTkButton(master=self.frame_right,
        #                                                height=25,
        #                                                text="CTkButton",
        #                                                command=self.button_event)
        # self.slider_button_1.grid(row=4, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        # self.slider_button_2 = customtkinter.CTkButton(master=self.frame_right,
        #                                                height=25,
        #                                                text="CTkButton",
        #                                                command=self.button_event)
        # self.slider_button_2.grid(row=5, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        # self.checkbox_button_1 = customtkinter.CTkButton(master=self.frame_right,
        #                                                  height=25,
        #                                                  text="CTkButton",
        #                                                  border_width=3,   # <- custom border_width
        #                                                  fg_color=None,   # <- no fg_color
        #                                                  command=self.button_event)
        # self.checkbox_button_1.grid(row=6, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        # self.check_box_1 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                              text="CTkCheckBox")
        # self.check_box_1.grid(row=6, column=0, pady=10, padx=20, sticky="w")

        # self.check_box_2 = customtkinter.CTkCheckBox(master=self.frame_right,
        #                                              text="CTkCheckBox")
        # self.check_box_2.grid(row=6, column=1, pady=10, padx=20, sticky="w")

        # self.entry = customtkinter.CTkEntry(master=self.frame_right,
        #                                     width=120,
        #                                     placeholder_text="CTkEntry")
        # self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Confirm Function",
                                                command=self.button_event)
        self.button_5.grid(row=9, column=0, columnspan=1, pady=20, padx=20, sticky="we")
        
        self.label_info_password = customtkinter.CTkLabel(master=self.frame_right,
                                                   text = "password",
                                                   justify=tkinter.LEFT)
        
        password_string = tkinter.StringVar(self.frame_right, value="SmartProp800")
        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=80,
                                            placeholder_text="Password",
                                            textvariable=password_string)
        # self.entry.grid(row=7, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        # set default values
        self.radio_button_1.select()
        self.switch_2.select()
        # self.slider_1.set(0.2)
        # self.slider_2.set(0.7)
        # self.progressbar.set(0.5)
        # self.slider_button_1.configure(state=tkinter.DISABLED, text="Disabled Button")
        # self.radio_button_3.configure(state=tkinter.DISABLED)
        # self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        # self.check_box_2.select()
    def change_radio_option(self):
        
        if self.radio_var.get() == 0 :
            self.label_info_1.config(text = function_desc_dict[function_group_list[self.function_selected][0]])
            
        elif self.radio_var.get() == 1 :
            self.label_info_1.config(text = function_desc_dict[function_group_list[self.function_selected][1]])
        
        
            
            
    def change_function_button(self):
        self.function_selected = list(function_group_list.keys())[self.radio_function_var.get()]
        
        self.radio_button_1.config(text =function_group_list[self.function_selected][0] )
        self.radio_button_2.config(text =function_group_list[self.function_selected][1] )
        
        if self.function_selected == "Crimision Logic" :
            
            self.entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we" )
            self.label_info_password.grid(column=0, row=7, sticky="w", padx=2, pady=2)
        else:
            self.entry.grid_remove()
            self.label_info_password.grid_remove()
            
        self.change_radio_option()
    
    def button_event(self):
        
        function_press = list(function_group_list.values())[self.radio_function_var.get()][self.radio_var.get()]
        confirm_message_box  =tkinter.messagebox.askquestion("confirm function", 
        f'confirm to proceed with {function_press}'
        )
        if confirm_message_box =="no" : return
            
        if function_press == "extract_all_copier_monthly" :
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                executor.submit(extract_copier_canon_ir3320().get_counter_list)
                executor.submit(extract_copier_canon_ir5540().get_counter_list)
                executor.submit(extract_copier_ricoh_c3503().get_counter_list)
                executor.submit(extract_copier_toshiba_5015ac().get_counter_list)

        elif function_press == "zerolize_all_copier_monthly" :
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(extract_copier_canon_ir5540().clear_counter_list)
                executor.submit(extract_copier_canon_ir3320().clear_counter_list)
                executor.submit(extract_copier_toshiba_5015ac().clear_counter_list)

        elif function_press == "submit_outstanding_crimsion_sec47" :
            crimsion_intereq_instance = crimsion_intereq_selenium(PASSWORD=self.entry.get())
            crimsion_intereq_instance.upload_outstanding_sec()
        
        elif function_press == "extract_monthly_crimision_billing_report" :
            report_month = date(date.today().year, date.today().month , 1) - timedelta(days=1)
            crimsion_intereq_instance = crimsion_intereq_selenium(PASSWORD=self.entry.get())
            crimsion_intereq_instance.retrieve_monthly_report(report_month)

        else : print ("empty")


    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()