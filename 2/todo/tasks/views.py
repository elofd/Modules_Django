from django.http import HttpResponse
from django.views import View
from random import randint


class ToDoView(View):

    def get(self, requests, *args, **kwargs):
        tasks = ['Random task {0}'.format(i) for i in range(1, 11)]
        result = ('<ul style="font-size: 220%; color: red;">'
                      f'<li>{tasks[randint(0, 9)]}</li>'
                      f'<li>{tasks[randint(0, 9)]}</li>'
                      f'<li>{tasks[randint(0, 9)]}</li>'
                      f'<li>{tasks[randint(0, 9)]}</li>'
                      f'<li>{tasks[randint(0, 9)]}</li>'
                  '</ul>')
        return HttpResponse(result)

