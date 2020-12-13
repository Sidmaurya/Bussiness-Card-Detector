
import watchdog.events 
import watchdog.observers 
import time 
import MainModel
from pathlib import Path
  
class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self): 
        # Set the patterns for PatternMatchingEventHandler 
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpeg','*.jpg','*.png'], 
                                                             ignore_directories=True, case_sensitive=False) 
  
    def on_created(self, event): 
        print("Watchdog received created event - % s." % event.src_path) 
        Path("out_image").mkdir(parents=True, exist_ok=True)
        Path("out_text").mkdir(parents=True, exist_ok=True)
        data_dict=MainModel.model_process(event.src_path)
        print(data_dict)

        # Event is created, Now process for model





  
  
if __name__ == "__main__": 
    src_path = "/mnt/c/Users/SID/Desktop/bussiness card detector/backend/images"
    event_handler = Handler() 
    observer = watchdog.observers.Observer() 
    observer.schedule(event_handler, path=src_path, recursive=True) 
    observer.start()
    print('observer initiated') 
    try: 
        while True: 
            time.sleep(1) 
    except KeyboardInterrupt: 
        observer.stop() 
        print('KeyboardInterrupt') 
    observer.join()