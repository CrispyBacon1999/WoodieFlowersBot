halp = {
	'default': 'This is the default help message. Message @Floodie_Wowers to have it updated.',
	'help': 'Provides help about the command trailing the /halp. Usage: "/halp command"'
}

general = {
	'plugin': {
		'level_low': 'You don\'t have a high enough level to run this command!'
	}
}

xp = {
	'none': 'User doesn\'t have any XP yet. Get talking!',
	'firstlast': 'Current User XP for %s %s: %d', # First Name, Last Name, XP
	'nolast': 'Current User XP for %s: %d' # First Name, XP
}

user = {
	'help': 'Gets information about a user.',
	'keyboard': 'Please select an option for information about the user.',
	'team': {
		'message': '%s is from team %d.', # Team Number
		'error': 'There was an error when calculating your result.'
	},
	'github': {
		'message': 'https://github.com/%s', # Github Username
		'error': 'This user hasn\'t set their github username yet.'
	},
	'reddit': {
		'message': 'https://reddit.com/u/%s', # Reddit Username
		'error': 'This user hasn\'t set their reddit username yet.'
	}
}

info = {
	'information': '''You are using Woodie Flowers - %s

	Username: %s
	Source Code: [GitHub](https://github.com/CrispyBacon1999/WoodieFlowersBot)
	'''
}

levels = {
	'level': 'Your level is set to: %s.'
}

ping = {
	'pong': 'PONG!'
}

set = {
	'help': 'Sets user info. \nNo param = team number\nr:Reddit Username\ngit:Github Username\n\nExample /set git:team254',
	'team': {
		'success': 'Successfully set your team to %d!', # Team Number
		'error': 'Could not set your team.'
	},
	'github': {
		'success': 'Successfully set your github username to %s!', # Github Username
		'error': 'Could not set your github username.'
	},
	'reddit': {
		'success': 'Successfully set your reddit username to %s!', # Reddit Username
		'error': 'Could not set your reddit username.'
	}
}

tba = {
	'help': 'Use /tba #### for a team, or /tba shortcode for an event. Then use the inline keyboard for individual information.',
	'team': {
		'standard': 'Team: %s\n\n%s' # Team number, team info
	},
	'event': {
		'standard': 'Event: %s\n\n%s' # Event number, event info
	}
}

github = {
	'help': 'Returns a github repository link using /github username repository.'
}

admin = {
	'help': 'Performs an administrative action on the replied to user.',
	'no_reply': 'Reply to a user!',
	'keyboard': 'Administrative Commands',
	'admin_only': 'You must be an admin to use this!',
	'unknown_error': 'An unknown error has occurred.',
	'kick': '%s has been kicked!', # User name
	'ban': '%s has been banned!', # User name
	'warn': '%s now has %d warns! If they get %d, they will be kicked!', # User name, number of warns, kick warns
}