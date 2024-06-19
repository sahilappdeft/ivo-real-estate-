import json
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response

class CustomResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Only process DRF Responses
        if isinstance(response, Response):
            print(response.content, "::::::::::::::::::::::")
                        
            if response.status_code >= 400:
                new_response = {
                    'data': response.data,
                    'success': False,  # Corrected the spelling here
                }
            else:
                new_response = {
                    'data': response.data,
                    'success': True, # Corrected the spelling here
                }
            
            # Update response.content to ensure the client gets the updated data
            response.content = json.dumps(new_response)
        
        return response
