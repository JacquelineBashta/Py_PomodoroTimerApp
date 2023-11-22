
import tkinter
from tkinter import ttk
from playsound import playsound


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#f16849"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

WORK_MIN = 50
SHORT_BREAK_MIN = 10
LONG_BREAK_MIN = 20
REPEAT = 2

# WORK_MIN = 0.5
# SHORT_BREAK_MIN = 0.25
# LONG_BREAK_MIN = 0.5
# REPEAT = 2


class PomoApp:
    def __init__(self) -> None:

        self._reinit_vars()
        self.setup_gui()

    def _reinit_vars(self):
        self.work_min = WORK_MIN
        self.short_break = SHORT_BREAK_MIN
        self.long_break = LONG_BREAK_MIN
        self.repeat = REPEAT
        self.curr_repeat = 0
        self.count_up_job = None
        self.count_down_job = None

    def reset_pressed(self):
        if self.count_up_job:
            self.window.after_cancel(self.count_up_job)
        if self.count_down_job:
            self.window.after_cancel(self.count_down_job)
        self.lbl_activity.config(text="Timer", fg=GREEN)
        self.lbl_checks.config(text="")
        self.canvas.itemconfigure(self.lbl_counter, text="00:00")
        self._reinit_vars()

    def start_pressed(self):
        self.curr_repeat += 1
        self.window.attributes('-topmost', 1)
        self.window.attributes('-topmost', 0)
        if self.curr_repeat % (self.repeat*2) == 0:
            # do long break sequence
            self.lbl_activity.config(text="Long Break", fg=RED)
            playsound('long_break.wav')
            long_break = int(self.long_break*60)
            self.count_down(long_break)
            self.lbl_checks.config(text="  ")
            self.curr_repeat = 0
        elif self.curr_repeat % 2 == 0:
            # do short break sequence
            self.lbl_activity.config(text="Break", fg=PINK)
            playsound('short_break.wav')
            short_break = int(self.short_break*60)
            self.count_down(short_break)
        else:
            # do work sequence
            self.lbl_activity.config(text="Work", fg=GREEN)
            playsound('work.wav')
            work_sec = int(self.work_min*60)
            self.count_up(work_sec)
            curr_text = self.lbl_checks.cget("text")
            self.lbl_checks.config(text=curr_text+"✔")

    def setup_gui(self):
        self.window = tkinter.Tk()
        self.window.title("Pomodoro")
        self.window.config(width=500, height=500, bg=YELLOW, padx=50, pady=50)

        self.lbl_activity = tkinter.Label(text="Timer", bg=YELLOW, fg=GREEN)
        self.lbl_activity.config(font=(FONT_NAME, 44, "bold"))
        self.lbl_activity.grid(column=1, row=0)

        self.canvas = tkinter.Canvas(width=204, height=224,
                                     background=YELLOW, highlightthickness=0)
        self.tomato_img = tkinter.PhotoImage(file="tomato.png")
        self.canvas.create_image(103, 112, image=self.tomato_img)
        self.lbl_counter = self.canvas.create_text(
            103, 130, text="0:00", font=(FONT_NAME, 35, "bold"), fill="white")

        self.canvas.grid(column=1, row=1)
        self.btn_start = tkinter.Button(
            text="Start", command=self.start_pressed)
        self.btn_start.config(bg="white")
        self.btn_start.grid(column=0, row=2)

        self.btn_reset = tkinter.Button(
            text="Reset", command=self.reset_pressed)
        self.btn_reset.config(bg="white")
        self.btn_reset.grid(column=2, row=2)

        self.lbl_checks = tkinter.Label(text="", bg=YELLOW, fg=GREEN)
        self.lbl_checks.config(font=(FONT_NAME, 15, "bold"))
        self.lbl_checks.grid(column=1, row=3)

    def show_timer(self, tmr_in_sec):
        seconds = tmr_in_sec % 60
        minutes = tmr_in_sec // 60
        sec_lead_0 = '0' if seconds < 10 else ''
        min_lead_0 = '0' if minutes < 10 else ''
        label_txt = f"{min_lead_0}{minutes}:{sec_lead_0}{seconds}"
        self.canvas.itemconfigure(self.lbl_counter, text=label_txt)

    def count_up(self, max_val, tmr_sec=0):
        self.show_timer(tmr_sec)
        if tmr_sec < max_val:
            self.count_up_job = self.window.after(
                1000, self.count_up, max_val, tmr_sec+1)

        else:
            self.start_pressed()

    def count_down(self, tmr_sec):
        self.show_timer(tmr_sec)
        if tmr_sec > 0:
            self.count_down_job = self.window.after(
                1000, self.count_down, tmr_sec-1)
        else:
            self.start_pressed()

    def run(self):
        self.window.mainloop()


timer = PomoApp()
timer.run()
