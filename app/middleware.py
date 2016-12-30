class CorsMiddleware(object):
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):

        response = self.get_response(request)
        
        response['Access-Control-Allow-Origin']='*'
        response['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With, accept, origin, Authorization, x-csrftoken, '
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        return response
        
        