from customtkinter import CTk, CTkLabel, CTkEntry, CTkFrame, CTkButton, StringVar, LEFT, TOP, BOTTOM, RIGHT
from threading import Thread
import time
# from typing import Optional

class App(CTk):
    def __init__(self):
        super().__init__()

        # Configuration
        self.title('DailyTimer')
        self.geometry('300x200')

        # Simple Variables
        self.SPLIT_SYMB = ':'
        self.IS_TIMER_EDIT = True
        self.IS_START = False
        self.LABEL_PADXY = (10, 0)

        # StringVariables
        self.timer_variable_days = StringVar(self, value='00')          # Days
        self.timer_variable_hours = StringVar(self, value='00')         # Hours
        self.timer_variable_minnutes = StringVar(self, value='00')      # Minutes
        self.timer_variable_seconds = StringVar(self, value='00')       # Secinds
        self.timer_variable_miliseconds = StringVar(self, value='00')   # MiliSeconds

        # Load first scene
        self.start_body()

    def _el(self, element:CTkLabel | CTkEntry | CTkButton | CTkFrame, *args, pack:dict = None, **kwargs) -> CTkLabel | CTkEntry | CTkButton | CTkFrame:
        obj = element(*args, **kwargs)
        obj.pack(**pack if pack != None else {})
        return obj
    
    def change_label_to_entry(self, fisrt_list, second_list, pxy=(0, 0)):
        # event.widget.pack_forget()
        if self.IS_TIMER_EDIT:
            self.edit_btn.pack(side=BOTTOM)
            [el.pack_forget() for el in fisrt_list]
            [el.pack(side=LEFT) for el in second_list]
            self.IS_TIMER_EDIT = False
        else:
            self.edit_btn.pack_forget()
            [el.pack_forget() for el in second_list]
            [el.pack(side=LEFT, padx=pxy[0], pady=pxy[1]) for el in fisrt_list]
            self.IS_TIMER_EDIT = True
        

    def start_stop(self):
        if self.IS_START:
            self.IS_START = False
            self.start_btn.configure(text='Start')
        else:
            self.IS_START = True
            self.start_btn.configure(text='Stop')


    def _thread_timer(self):
        while True:
            if self.IS_START:
                if int(self.timer_variable_miliseconds.get()) < 99:
                    val1 = int(self.timer_variable_miliseconds.get()) + 1
                    if val1 < 10: val1 = '0' + str(val1)

                    self.timer_variable_miliseconds.set(str(val1))
                else:
                    if int(self.timer_variable_seconds.get()) < 59:
                        val1 = int(self.timer_variable_seconds.get()) + 1
                        if val1 < 10: val1 = '0' + str(val1)

                        self.timer_variable_seconds.set(str(val1))

                    else:
                        if int(self.timer_variable_minnutes.get()) < 59:
                            val1 = int(self.timer_variable_minnutes.get()) + 1
                            if val1 < 10: val1 = '0' + str(val1)

                            self.timer_variable_minnutes.set(str(val1))

                        else:
                            if int(self.timer_variable_hours.get()) < 23:
                                val1 = int(self.timer_variable_hours.get()) + 1
                                if val1 < 10: val1 = '0' + str(val1)

                                self.timer_variable_hours.set(str(val1))
                            
                            else:
                                if int(self.timer_variable_days.get()) < 100:
                                    val1 = int(self.timer_variable_days.get()) + 1
                                    if val1 < 10: val1 = '0' + str(val1)

                                    self.timer_variable_days.set(str(val1))

                                else:
                                    self.timer_variable_days.set('00')
                            
                                self.timer_variable_hours.set('00')


                            self.timer_variable_minnutes.set('00')


                        self.timer_variable_seconds.set('00')


                    self.timer_variable_miliseconds.set('00')

            time.sleep(0.01)
        

    def start_body(self):
        self._el(CTkLabel, self, text='Daily Timer')

        self.timer_elements_label = []
        self.timer_elements_entry = []
        list_variables = [self.timer_variable_days, self.timer_variable_hours, self.timer_variable_minnutes, self.timer_variable_seconds, self.timer_variable_miliseconds]

        self.timer_main_frame = self._el(CTkFrame, self, height=150)
        self._el(CTkLabel, self.timer_main_frame, pack={'side': TOP}, width=230, text='Days  |  Hours  |     Min     |   Sec   |   MS  ', fg_color="#232323", text_color='#676767')
        
        self.timer_frame = self._el(CTkFrame, self.timer_main_frame)
        for idx, timer_var in enumerate(list_variables):
            label_el = self._el(CTkLabel, self.timer_frame, pack={'side': LEFT}, textvariable=timer_var, width=30, fg_color="#232323")
            self.timer_elements_label.append(label_el)
            label_el.bind('<Double-ButtonPress-1>', lambda x: self.change_label_to_entry(self.timer_elements_label, self.timer_elements_entry))

            entry_el = self._el(CTkEntry, self.timer_frame, pack={'side': LEFT}, textvariable=timer_var, width=30)
            self.timer_elements_entry.append(entry_el)

            entry_el.pack_forget()
            
            if idx != len(list_variables) - 1:
                split_el = self._el(CTkLabel, self.timer_frame, text=self.SPLIT_SYMB, pack={'side': LEFT}, width=20, fg_color="#232323", text_color='#676767')
                split_el.bind('<Double-ButtonPress-1>', lambda x: self.change_label_to_entry(self.timer_elements_label, self.timer_elements_entry))

                self.timer_elements_label.append(split_el)
                self.timer_elements_entry.append(split_el)
            else:
                self.edit_btn = self._el(CTkButton, self.timer_frame, pack={'side': BOTTOM}, width=230, text='Save changes', command=lambda: self.change_label_to_entry(self.timer_elements_label, self.timer_elements_entry))
                self.edit_btn.pack_forget()

        self.start_btn = self._el(CTkButton, self, pack={'side': TOP, 'pady': 20}, text='Start', command=self.start_stop)

        Thread(target=self._thread_timer, daemon=True).start()
            


    # Main Loop GUI
    def mainloop(self, n = 0):
        return super().mainloop(n)
    
if __name__ == '__main__':
    App().mainloop()