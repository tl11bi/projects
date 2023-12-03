from datetime import datetime


class AppLogs(object):

    def __init__(self):
        """
        Constructor for the log class.
        """
        self.logs_path = 'app.log'

    def get_logs(self):
        """
        This method retrieves logs from the file
        """
        with open(self.logs_path, 'r') as f:
            logs = f.read()
            return logs, 200

    def delete_logs(self):
        """
        This method deletes logs from the file
        """
        with open(self.logs_path, 'w') as f:
            f.write('')
            return "OK", 200

    def write_logs(self, message):
        to_save = datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " " + message + "\n"
        with open(self.logs_path, 'a') as f:
            f.write(to_save)
            print(to_save)

