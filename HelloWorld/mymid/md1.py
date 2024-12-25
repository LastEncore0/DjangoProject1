from django.utils.deprecation import MiddlewareMixin

class Md1Md1(MiddlewareMixin):
    def process_request(self, request):
        print('Request is comming')

    def process_response(self, request, response):
        print('Response is completing')
        return response