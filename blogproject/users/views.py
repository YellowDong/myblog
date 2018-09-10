from users.form import RegisterForm
from django.shortcuts import redirect, render


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})


def index(request):
    return render(request, 'index.html')