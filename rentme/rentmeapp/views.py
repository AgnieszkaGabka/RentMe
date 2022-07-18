from django.shortcuts import render
from datetime import datetime, date

from django.contrib.auth import authenticate, login, logout
from django.core.checks import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View

