"""
Graphical user interface.
"""
import tkinter as tk
import tkinter.ttk as ttk

from numpy import pad


class LogsTable(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config(padding=15)
        self.pack_propagate(False)

        self.treeview = ttk.Treeview(self)
        self.vertical_scrollbar = ttk.Scrollbar(self, orient='vertical')
        self.horizontal_scrollbar = ttk.Scrollbar(self, orient='horizontal')

        self.horizontal_scrollbar.pack(side='bottom', fill='x')
        self.treeview.pack(side='left', fill='both', expand=True)
        self.vertical_scrollbar.pack(side='left', fill='y')

        self.treeview.config(yscrollcommand=self.vertical_scrollbar.set)
        self.treeview.config(xscrollcommand=self.horizontal_scrollbar.set)
        self.vertical_scrollbar.config(command=self.treeview.yview)
        self.horizontal_scrollbar.config(command=self.treeview.xview)

        self.treeview.config(show='headings')
        self.treeview.config(columns=('message'))
        self.treeview.heading('message', text='Message')


class TimeLapsed(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config(padding=15)

        self.label = ttk.Label(self)
        self.label.config(anchor='center')
        self.label.pack(side='top', fill='x')


class KillCount(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config(padding=15)

        self.label = ttk.Label(self)
        self.label.config(anchor='center')
        self.label.pack(side='top', fill='x')


class RunningStatus(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.config(padding=15)

        self.label = ttk.Label(self)
        self.label.pack(side='right')
        self.label.config(text='oo')


class Gui(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # creating widgets.
        self.time_lapsed = TimeLapsed(self)
        self.kill_count = KillCount(self)
        self.logs_table = LogsTable(self)
        self.running_status = RunningStatus(self)
        self.confirm_button = ttk.Button(self)

        self.kill_count.pack(side='top', fill='x')
        self.time_lapsed.pack(side='top', fill='x')
        self.logs_table.pack(side='top', fill='both', expand=True)
        self.confirm_button.pack(side='top', fill='x', padx=15, pady=15)
        self.running_status.pack(side='top', fill='x')

        # initial configurations.
        self.geometry('500x500+0+0')
        self.title('Pro - Wild Bot.')
        self.apply_style()
    
    def get_confirm_button(self) -> ttk.Button:
        return self.confirm_button
    
    def apply_style(self) -> None:
        style = ttk.Style()
        style.configure('.', background='white')
        self.config(background='white')
        style.configure('.', font='Consolas 16 normal')
        style.configure('Treeview', rowheight=40)
        style.configure('Treeview.Heading', font='Consolas 16 normal')
    
    
    def clear_logs(self) -> None:
        """
        Remove all messages in logs table.
        """
        treeview = self.logs_table.treeview
        treeview.delete(*treeview.get_children())

    def insert_log(self, message: str) -> None:
        """
        Insert a new message in logs table.
        """
        treeview = self.logs_table.treeview
        treeview.insert('', 'end', values=(message, ))
    
    def set_kill_count_message(self, message: str) -> None:
        """
        Set a new kill count message.
        """
        label = self.kill_count.label
        label.config(text=message)
    
    def set_time_lapsed_message(self, message: str) -> None:
        """
        Set a new time lapsed message.
        """
        label = self.time_lapsed.label
        label.config(text=message)
    
    def set_running_status_message(self, message: str) -> None:
        """
        Set a new running status message.
        """
        label = self.running_status.label
        label.config(text=message)
    
    def set_confirm_button_text(self, text: str) -> None:
        """
        Set a new text to confirm button.
        """
        self.confirm_button.config(text=text)
    