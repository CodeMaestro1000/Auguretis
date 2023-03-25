from fastapi.security import OAuth2PasswordRequestForm

class OAuthSerializer(OAuth2PasswordRequestForm):
    """
    Utility class so I don't have to worry about how to pass a username and password (both strings)
    to login_for_access_token that needs a OAuth2PasswordRequestForm instance
    """
    def __init__(self, username, password):
        super().__init__(username=username, password=password, scope="")
        # set scope to "" to prevent the code from throwing an AttributeError exception