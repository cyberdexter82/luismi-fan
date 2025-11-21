# usuarios/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, ActualizarPerfilForm

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login') # Redirige al login después de registrarse
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required # Esto obliga a estar logueado para ver esta vista
def perfil(request):
    if request.method == 'POST':
        # Necesitamos request.FILES para las imágenes
        perfil_form = ActualizarPerfilForm(request.POST, request.FILES, instance=request.user.perfil)
        if perfil_form.is_valid():
            perfil_form.save()
            messages.success(request, '¡Tu foto de perfil ha sido actualizada!')
            return redirect('perfil')
    else:
        perfil_form = ActualizarPerfilForm(instance=request.user.perfil)

    context = {
        'perfil_form': perfil_form
    }
    return render(request, 'usuarios/perfil.html', context)