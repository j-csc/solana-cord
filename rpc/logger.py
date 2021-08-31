import logging, sys, os

# Set up basic logger
logger = logging.getLogger('sol.client')

# Setup stdout logger
soh = logging.StreamHandler(sys.stdout)
logger.addHandler(soh)

# File handler for logging to a file
fh = logging.FileHandler('solClient.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

# create formatter
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
# add formatter to fh
fh.setFormatter(formatter)
soh.setFormatter(formatter)

# Get log level from env vars
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
if os.environ.get('DEBUG'):
    if log_level:
        logger.warn("Overriding LOG_LEVEL setting with DEBUG")
    log_level = 'DEBUG'

try:
    logger.setLevel(log_level)
except ValueError:
    logger.setLevel(logging.INFO)
    logger.warn("Variable LOG_LEVEL not valid - Setting Log Level to INFO")
