from django.shortcuts import render

# Create your views here.
def MovieFunc(request):
    return render(request, 'chartpage.html')

def into1Func(request):
    return render(request, 'introducetest1.html')

def into2Func(request):
    return render(request, 'introducetest2.html')

def into3Func(request):
    return render(request, 'introducetest3.html')

def into4Func(request):
    return render(request, 'introducetest4.html')

def into5Func(request):
    return render(request, 'introducetest5.html')

def into6Func(request):
    return render(request, 'introducetest6.html')





