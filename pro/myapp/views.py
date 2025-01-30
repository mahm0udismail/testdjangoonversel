from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from datetime import datetime

def hello(request):
    return HttpResponse("Hello, World!")


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)