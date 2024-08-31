import sys
import logging
import logger

def error_message_detail(error,error_detail:sys):
    '''
    The error parameter represents the exception itself, 
    
    error_detail:sys parameter provides additional context about
    the exception,such as the filename and line number where it occurred.
    These parameters are used by the error_message_detail function 
    to construct a detailed error message that can be displayed to 
    the user or logged for debugging purposes.
    '''
    _,_,exec_tb = error_detail.exc_info()
    # Get file Name which has error
    file_name = exec_tb.tb_frame.f_code.co_filename
    # Get Line Number for the error
    line_no = exec_tb.tb_lineno
    # Get error details
    err = str(error)
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,  
        line_no,
        err
    )

    return error_message

class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail=error_detail)
    
    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as error:
        # Log the error message
        logging.info("An error occurred: {0} and details: {1}".
                     format(
                         str(error),
                            CustomException(error, sys)
                            ))
        # Raise the custom exception with additional details
        raise CustomException(error, sys)