import botconfig

PINK = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
ORANGE = '\033[93m'
RED = '\033[91m'
WHITE = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


# Determine which type of message to log, then call the appropriate function to log it
def log(msg):
    if msg['chat']['type'] == 'private':
        _log_private(msg)
    elif msg['chat']['type'] == 'supergroup':
        _log_supergroup(msg)


# Log a message from a supergroup to print the message in a neat format
def _log_supergroup(msg):
    if 'last_name' in msg['from']:
        print('%s%s%s - %s%s %s%s : %s%s%s' % (RED, msg['chat']['title'], PINK,
                                               BLUE, msg['from']['first_name'],
                                               msg['from']['last_name'], PINK,
                                               WHITE, msg['text'], WHITE))


# Log a message from a private message to print it in a neat format
def _log_private(msg):
    if 'last_name' in msg['from']:
        print('%s%s%s - %s%s %s%s : %s%s%s' % (RED, 'PRIVATE', PINK,
                                               BLUE, msg['from']['first_name'],
                                               msg['from']['last_name'], PINK,
                                               WHITE, msg['text'], WHITE))


# Log an error message
def error(msg):
    print(RED + msg + WHITE)


# Log an initialization message
def init_log(msg):
    print(ORANGE + msg + WHITE)
