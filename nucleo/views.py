from django.shortcuts import render

# 1. Página Principal
def vista_inicio(request):
    return render(request, 'index.html')

# 2. Página de Música Disponible
def vista_musica(request):
    return render(request, 'musicadisponible.html')

# 3. Página de Próximamente
def vista_proximamente(request):
    return render(request, 'proximamente.html')

# 4. Álbum: 20 Años
def vista_album_20(request):
    return render(request, 'album20anos.html')

# 5. Álbum: Romance
def vista_album_romance(request):
    return render(request, 'albumromance.html')

# 6. Álbum: Luis Miguel 2010
def vista_album_2010(request):
    return render(request, 'albumluismiguel2010.html')