from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock



class Config_popup(Popup):
    
    def save_config(self, w, r, l, caller):
        print(f"Work: {w}, Rest: {r}, Long Rest: {l}")
        caller.apply_config(w, r, l)
        self.dismiss()

    # I have no clue, if this is the simplest way to do this, but it works
    def get_info(self, caller):
        self.work_time = caller.work_time
        self.rest_time = caller.rest_time
        self.long_rest_time = caller.long_rest_time
        self.caller = caller

class MainGrid(GridLayout):

    def start_stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.clock_event.cancel()
            self.ids.start_stop.text = "Start"
            self.ids.status.text = "Paused during " + self.curent_faze
        else:
            self.is_running = True
            self.clock_event = Clock.schedule_interval(self.update_timer, 1)
            self.ids.start_stop.text = "Stop"
            self.curent_faze = "Working..."
            self.ids.status.text = "Working..."

    def reset_timer(self):
        print("App reset")

    def open_config(self):
        self.config_popup = Config_popup()
        self.config_popup.get_info(self)
        self.config_popup.open()

    def apply_config(self, work, rest, long_rest):
        print(self)
        #caller.work_time = work*60
        #caller.rest_time = rest*60
        #caller.long_rest_time = long_rest*60
        #caller.original_times = [work*60, rest*60, long_rest*60]
        #caller.working = True
        #caller.faze_count = 0
        #caller.ids.timer.text = f"{work}:00"
        #caller.ids.status.text = "Work Timer"
        #if caller.is_running:
        #    caller.clock_event.cancel()
        #    caller.is_running = False
        #caller.ids.start_stop.text = "Start"

    def update_timer(self, t):
        if self.is_working:
            self.work_time -= 1
            time = self.work_time
        else:
            self.rest_time -= 1
            time = self.rest_time
        minutes, remainder = divmod(time, 60)
        self.ids.timer.text = ("%02d:%02d" % (minutes, remainder))
        self.check_time()

    def check_time(self):
        if self.work_time == 0:
            self.is_working = False
            self.work_time = self.original_times[0]
            self.ids.timer.text = f"{self.rest_time}:00"
            self.ids.status.text = "Break Time"
            self.faze_count += 1
        if self.rest_time == 0:
            self.is_working = True
            self.rest_time = self.original_times[1]
            self.ids.timer.text = f"{self.work_time}:00"
            self.ids.status.text = "Working..."
            self.faze_count += 1

class Work_timerApp(App):
    def build(self):
        return MainGrid()

Work_timerApp().run()