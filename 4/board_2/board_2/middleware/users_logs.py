from datetime import datetime


class UsersLogs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        date = str(datetime.now())[:19]
        url = request.META.get('HTTP_HOST')
        page = request.path
        http_method = request.META.get('REQUEST_METHOD')
        with open('board_2/middleware/logs.txt', 'a', encoding='utf-8') as log_file:
            log_file.write('Дата посещений: {} URL: {}{} HTTP метод: {} \n'.format(
                date, url, page, http_method
            ))
        response = self.get_response(request)
        return response

