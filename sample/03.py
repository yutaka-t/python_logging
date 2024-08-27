import logging
from logging.handlers import SMTPHandler
smtp_handler = SMTPHandler(mailhost=('smtp.example.com', 587),
                           fromaddr='from@example.com',
                           toaddrs=['to@example.com'],
                           subject='Application Error')
logger.addHandler(smtp_handler)
