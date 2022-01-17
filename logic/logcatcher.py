#!/usr/bin/env python3
import sys
import io
import logging
import traceback

class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, log_level=logging.INFO):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())
         
    def flush(self):
        pass

def set_log_catcher(log_name=sys.argv[0]+'.log'):
    logging.basicConfig(filename=log_name, level=logging.DEBUG, filemode="w")
    log = logging.getLogger(__name__)
  
    sl = StreamToLogger(log, logging.INFO)
    sys.stdout = sl
    sl = StreamToLogger(log, logging.ERROR)
    sys.stderr = sl
  
    '''    
    # Separate exception handler with custom logging options
    def my_handler(exc_type, exc_obj, tb):
        log.exception('\n'.join(traceback.format_tb(tb)), exc_info=False, stack_info=False)
        log.exception(str(exc_obj), exc_info=False, stack_info=False)

    # Install exception handler
    sys.excepthook = my_handler
    '''

# Test log catcher
if __name__ == "__main__":
    sys.stdout.write("Start testing\n")
    sys.stdout.flush()
    set_log_catcher()
    sys.stdout.write("Test stdout redirect")
    sys.stderr.write("Test stderr redirect")
    sys.stderr.write("Test exceptions redirect")
    def spam():
        with open('nonexists.txt') as f:
            pass
    
    spam()

