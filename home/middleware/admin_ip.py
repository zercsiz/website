from django.http import HttpResponseForbidden
import os

class AdminIPRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Replace 'allowed_ip' with the IP address you want to allow
        # allowed_ip = '95.0.226.242'
        allowed_ip = os.getenv("allowed_admin_ip")

        # Get the client's IP address from the request
        client_ip = request.META.get('REMOTE_ADDR')

        # Check if the client's IP matches the allowed IP
        if client_ip != allowed_ip:
            return HttpResponseForbidden("Access forbidden. Your IP is not allowed to access the admin panel.")

        response = self.get_response(request)
        return response