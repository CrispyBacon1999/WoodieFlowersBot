
logo = '''
 __          __             _ _        ______ _
 \ \        / /            | (_)      |  ____| |
  \ \  /\  / /__   ___   __| |_  ___  | |__  | | _____      _____ _ __ ___
   \ \/  \/ / _ \ / _ \ / _` | |/ _ \ |  __| | |/ _ \ \ /\ / / _ \ '__/ __|
    \  /\  / (_) | (_) | (_| | |  __/ | |    | | (_) \ V  V /  __/ |  \__ \\
     \/  \/ \___/ \___/ \__,_|_|\___| |_|    |_|\___/ \_/\_/ \___|_|  |___/

'''

TOKEN = ''
VERSION = 'v3.0'
logfile = 'logfile.json'
plugins = []


def init_plugins(bot):
    plugins = [

    ]

# Database Information
database = {
    'link': 'woodie.db',
    'tables': {
        'teams': {
            'name': 'memberteams',
            'columns': ['uid', 'team']
        },
        'ranks': {
            'name': 'ranks',
            'columns': ['uid', 'rank']
        },
        'stickers': {
            'name': 'stickerbinds',
            'columns': ['sticker', 'command']
        },
        'xp': {
            'name': 'userxp',
            'columns': ['uid', 'xp']
        },
        'messages': {
            'name': 'messages',
            'columns': ['key', 'message']
        },
        'requests': {
            'name': 'requests',
            'columns': ['uid', 'request']
        },
        'usernames': {
            'name': 'usernames',
            'columns': ['username', 'uid']
        },
        'warns': {
            'name': 'warns',
            'columns': ['uid', 'num']
        }
    }
}