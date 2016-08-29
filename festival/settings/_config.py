SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'

# Twitter
SOCIAL_AUTH_TWITTER_KEY = 'yrxANrcJTm8CzzUrG2s0jpyQ6'
SOCIAL_AUTH_TWITTER_SECRET = 'X00D6zWaNQaw95elIiBbAGWtDfLfyhGofh5gNXhoYnyuq0NMlk'

# Facebook
#SOCIAL_AUTH_FACEBOOK_KEY = '1289589481056633'
SOCIAL_AUTH_FACEBOOK_KEY = '1289726427709605'
#SOCIAL_AUTH_FACEBOOK_KEY = '1733548576884914'
#SOCIAL_AUTH_FACEBOOK_SECRET = 'a743c9107b841d905f865f1bac89997b'
SOCIAL_AUTH_FACEBOOK_SECRET = '48725a2121658ea22e269c1cbf85a160'
#SOCIAL_AUTH_FACEBOOK_SECRET = '47ba3545489bf848f83773981f027e2b'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_hometown', 'user_actions.music', 'user_actions.video', 'user_likes', 'user_tagged_places']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
	#'fields': 'id,name,email'
	'fields': 'id, name, email, gender, age_range, hometown, likes, music, tagged_places, videos'
	#'fields': 'id, name, email, gender, age_range, hometown, likes, user_actions.music'
}

'''SOCIAL_AUTH_FACEBOOK_SCOPE = ['email',]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
	'fields': 'id,name,email,gender,age_range'
}'''