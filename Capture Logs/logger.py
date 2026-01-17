import logging
import logging.handlers
from collections import deque

class SmartContextHandler(logging.Handler):
    """
    1. Records logs in RAM.
    2. Discards them if fine.
    3. Saves to DISK only on ERROR.
    """
    def __init__(self, target_handler, capacity=20):
        super().__init__()
        self.target = target_handler
        self.buffer = deque(maxlen=capacity) 

    def emit(self, record):
        self.buffer.append(record)
        if record.levelno >= logging.ERROR:
            self.flush_to_target()

    def flush_to_target(self):
        while self.buffer:
            self.target.handle(self.buffer.popleft())

def setup_logging():
    root_logger = logging.getLogger()

    for h in root_logger.handlers:
        if isinstance(h, SmartContextHandler):
            return

    # Files created in Root
    file_handler = logging.handlers.RotatingFileHandler(
        filename='TELEGRAM_BOT.log', 
        mode='a', 
        maxBytes=100 * 1024, # 100KB
        backupCount=2,       
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO) 

    smart_handler = SmartContextHandler(target_handler=file_handler, capacity=20)

    root_logger.setLevel(logging.INFO)
    
    if root_logger.handlers:
        root_logger.handlers = []

    root_logger.addHandler(console_handler)
    root_logger.addHandler(smart_handler)
    
    logging.info("✅ Smart Logger Activated.")
