from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm, EditarPerfilForm 

# --- CAMBIO FORZADO PARA AZURE ---

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada para {username}! Ya puedes iniciar sesión.')
            return redirect('login') 
    else:
        form = RegistroUsuarioForm()
    
    # ESTA ES LA LÍNEA QUE DEBE LLEGAR A LA NUBE:
    return render(request, 'registration/registro.html', {'form': form})

@login_required
def perfil(request):
    if request.method == 'POST':
        perfil_form = EditarPerfilForm(request.POST, request.FILES, instance=request.user.perfil)
        if perfil_form.is_valid():
            perfil_form.save()
            messages.success(request, '¡Tu foto de perfil ha sido actualizada!')
            return redirect('perfil')
    else:
        # Crea el perfil si no existe
        if not hasattr(request.user, 'perfil'):
            from .models import Perfil
            Perfil.objects.create(usuario=request.user)
        perfil_form = EditarPerfilForm(instance=request.user.perfil)

    context = {
        'perfil_form': perfil_form
    }
    # Asegúrate de que este también coincida con tu carpeta real
    return render(request, 'usuarios/perfil.html', context)