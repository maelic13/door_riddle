import datetime
from os.path import isfile
from tkinter import Label, mainloop, Tk


class TimerHelper:
    def __init__(self):
        self.tkinter = Tk()
        self.label = Label(
            self.tkinter, font=('calibri', 40, 'bold'),
            background='darkgrey', foreground='black')
        self._filename = 'timestamp.txt'

    def time(self):
        string = str(self._get_elapsed_time()).split(".")[0]
        self.label.config(text=string)
        self.label.after(1000, self.time)

    def run_timer(self):
        root = self.tkinter
        root.title('Timer')
        lbl = self.label
        lbl.pack(anchor='center')

        self.time()
        mainloop()

    def _get_elapsed_time(self):
        if not isfile(self._filename):
            self._write_current_date_and_time()
        with open(self._filename) as file:
            loaded = datetime.datetime.strptime(file.readline(), "%Y-%m-%d %H:%M:%S")
            return datetime.datetime.now() - loaded

    def _write_current_date_and_time(self):
        with open(self._filename, 'w') as file:
            file.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    TimerHelper().run_timer()
