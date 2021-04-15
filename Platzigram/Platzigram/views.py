"""Platzigram views."""

from django.http import HttpResponse, JsonResponse

# Utilities
from datetime import datetime


def hello_world(request):
    """Return a greeting."""

    # Usar debugger para acceder a los metodos de HttpRequest
    """import pdb; pdb.set_trace()"""
    numbers = request.GET["numbers"]
    response = JsonResponse({"Numeros": numbers})
    now = datetime.now()
    return HttpResponse(response)