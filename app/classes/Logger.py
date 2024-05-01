import toml
import datetime
import os

class Logger():
    def __init__(self)-> None:
        super().__init__()
    
    def log(self, state , message , server = None) -> None:
        date_time = datetime.datetime.now()
        date = date_time.strftime("%d/%m/%Y")
        log_date = date_time.strftime("%d_%m_%Y")
        time = date_time.strftime("%H:%M:%S")

        
        if server == None:
            lf = open(f'app/logs/{log_date}.txt' , 'a')
        else:
            lf = open(f'app/logs/server_log/{server}/{log_date}.txt' , 'a')
        
        match state:
            case "error":
                msg = f"{time} [ERROR]: {message}"
            case "info":
                msg = f"{time} [INFO]: {message}"
            case _:
                return None
        lf.write(f'{msg}\n')
        print(f'{date} {msg}')