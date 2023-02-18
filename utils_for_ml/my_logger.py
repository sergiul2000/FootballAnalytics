from datetime import date, datetime
import os


class logger:
    def __init__(self, file):
        self.file = file
    # def check_if_file_exists(self):
    #     if os.path.exists(self.file):
    #         return True
    #     else:
    #         return False

    # def auxiliar_print(self, text):
    #     # append mode
    #     file1 = open(self.file, "a")
    #     now = datetime.now()
    #     current_time = now.strftime("%c")
    #     file1.write(text+' '+current_time+'\n')
    #     file1.close()

    def print_logs_in_file(self, text):
        # check if file exists
        if os.path.exists(self.file):
            # print in specified file
            file1 = open(self.file, "a")
            if text != '':
                now = datetime.now()
                current_time = now.strftime("%c")
                file1.write(current_time+':  '+text+'\n')
                print(current_time+':  '+text+'\n')
            else:
                file1.write('\n')
                print()
            file1.close()
        return
