import csv
import json
import os
import re
import unicodedata

import h3
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.urls import reverse
from django.utils.text import slugify

def index(request):
    context = {}
    return render(request, 'accueil/accueil.html', context)