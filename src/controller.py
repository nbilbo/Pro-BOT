"""
Configure backend and frontend to work together.
"""
import threading
from src.auto import Backend
from src.gui import Gui

class Controller:
    def __init__(self) -> None:
        """
        Configure backend and frontend to work together.
        """
        self.frontend = Gui()
        self.backend = Backend()

        # first, the widgets configurations.
        time_lapsed = 'Time lapsed 00:00 second(s)'
        kill_count = 'Kill count: 0'
        running_status = 'Status: Off'
        confirm_button_text = 'Start'

        self.frontend.set_kill_count_message(kill_count)
        self.frontend.set_time_lapsed_message(time_lapsed)
        self.frontend.set_running_status_message(running_status)
        self.frontend.set_confirm_button_text(confirm_button_text)

        # second, the widgets commands.
        self.frontend.get_confirm_button().config(command=self.confirm_button_clicked)

    def start(self) -> None:
        """
        Start the graphical user interface.
        """
        self.frontend.mainloop()
    
    def confirm_button_clicked(self) -> None:
        if not self.backend.running:
            self.frontend.set_confirm_button_text('Stop.')
            self.frontend.set_running_status_message('Status: On')

            # thread to run the bot.
            threading.Thread(target=self.backend.start).start()

            # thread to update the logs.
            threading.Thread(target=self.update_logs).start()
        else:
            self.frontend.set_confirm_button_text('Start.')
            self.frontend.set_running_status_message('Status: Offline')
            self.backend.running = False
            self.backend.stop()
    
    def update_logs(self) -> None:
        from time import perf_counter

        last_update = perf_counter()
        while self.backend.running:
            if (perf_counter() -last_update) >= 1:
                defeated = self.backend.defeated
                time_lapsed = round(perf_counter() - self.backend.time_running, 2)
                self.frontend.set_kill_count_message(f'Kill counts: {defeated}')
                self.frontend.set_time_lapsed_message(f'Time lapsed: {time_lapsed} second(s)')
                self.frontend.clear_logs()
                for log in self.backend.logs[::-1]:
                    self.frontend.insert_log(log)
                last_update = perf_counter()


