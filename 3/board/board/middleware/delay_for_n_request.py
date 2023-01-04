from time import sleep


class DelayForNRequest:
    def __init__(self, get_response):
        self.get_response = get_response
        self.count = 0

    def __call__(self, request):
        self.count += 1
        if self.count == 5:
            sleep(5)
            self.count = 0
        response = self.get_response(request)
        return response
