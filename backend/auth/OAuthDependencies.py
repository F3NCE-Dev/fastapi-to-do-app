from config.config import settings
import urllib.parse

def generate_google_oauth_uri():
    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": "http://localhost:5500/frontend/index.html",
        "response_type": "code",
        "scope": " ".join(
            [
                "openid",
                "profile",
                "email",
            ]
        ),
        "access_type": "offline",
    }

    query_string = urllib.parse.urlencode(query_params, quote_via=urllib.parse.quote)
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    return f"{base_url}?{query_string}"
