from django.shortcuts import render, redirect
from .forms import RoleSelectionForm

def select_role(request):
    if request.method == 'POST':
        form = RoleSelectionForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data['role']
            if role == 'customer':
                return redirect('customer:signup')
            elif role == 'delivery':
                return redirect('delivery:signup')
            elif role == 'restaurant':
                return redirect('restaurant:signup')
    else:
        form = RoleSelectionForm()
    return render(request, 'accounts/select_role.html', {'form': form})

from django.shortcuts import redirect

def redirect_login(request):
    role = request.GET.get('role')
    if role == 'customer':
        return redirect('customer:login')
    elif role == 'delivery':
        return redirect('delivery:login')
    elif role == 'restaurant':
        return redirect('restaurant:login')
    return redirect('accounts:select_role')

def logout(request):
    request.session.flush() 
    return redirect('accounts:select_role') 
