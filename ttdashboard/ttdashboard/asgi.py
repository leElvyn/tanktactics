import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ttdashboard.settings')
asgi_thingy =get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import map.routing


application = ProtocolTypeRouter({
    "http": asgi_thingy,     # Just HTTP for now. (We can add other protocols later.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            map.routing.websocket_urlpatterns
        )
    ),
})
