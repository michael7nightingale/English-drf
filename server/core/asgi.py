import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from .middleware import TokenAuthMiddleware
from chats.routing import websocket_urlpatterns


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                URLRouter(websocket_urlpatterns)
            )
        ),

    }
)
