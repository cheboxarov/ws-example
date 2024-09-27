
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter
from graph.routing import ws_urlpatterns
from channels.sessions import SessionMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtime_graph.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        SessionMiddleware(
            URLRouter(
                ws_urlpatterns
            )
        )
    )
})
