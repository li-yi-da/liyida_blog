from django.utils.deprecation import MiddlewareMixin
class R1(MiddlewareMixin):

    def process_request(self,request):
        print('request1')

    def process_response(self,request,response):
        print('response1')
        return response
from django.shortcuts import HttpResponse
class R2(MiddlewareMixin):

    def process_request(self,request):
        print('request2')
        # return HttpResponse('回去')
    def process_response(self,request,response):
        print('response2')
        return response

class R3(MiddlewareMixin):

    def process_request(self, request):
        print('request3')

    def process_response(self,request,response):
        print('response3')
        return response