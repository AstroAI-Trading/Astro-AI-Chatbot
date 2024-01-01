from django.shortcuts import redirect
from django.conf import settings  # Import Django settings

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Middleware path: {request.path}, Authenticated: {request.user.is_authenticated}")  # Debugging line

        # Check if the request path is for a static file
        if request.path.startswith(settings.STATIC_URL):
            return self.get_response(request)

        response = self.get_response(request)

        allowed_paths = ['/login/', '/', '/register/', '/logout_page/', '/logout/']
        if not request.user.is_authenticated and request.path not in allowed_paths:
            print("Redirecting from middleware for path:", request.path)  # Debugging line
            return redirect('login_view')
        return response
