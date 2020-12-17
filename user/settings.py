# Settings for user and JWT

import datetime

AUTH_USER_MODEL = 'user.User'

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'user.serializer.user_serializer.CustomRegisterSerializer'
}
REST_USE_JWT = True


JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
}
