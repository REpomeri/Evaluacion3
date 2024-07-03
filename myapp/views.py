import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone  
from myapp.models import Document, Compra
from .forms import DocumentForm, UserRegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            if form.cleaned_data['is_admin']:
                new_user.is_staff = True
                new_user.is_superuser = True
            new_user.save()
            messages.success(request, 'Usuario nuevo creado.')
            form = UserRegistrationForm()  
    else:
        form = UserRegistrationForm()

    users = User.objects.all()
    return render(request, 'register.html', {'form': form, 'users': users})


def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
    return redirect('register')  

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('upload_document')  
                else:
                    return redirect('compra_view')  
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def guest_login(request):
    return redirect('compra_view')

def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_document')
    else:
        form = DocumentForm()

    documents = Document.objects.all()
    return render(request, 'upload.html', {'form': form, 'documents': documents, 'edit': False})

def update_document(request, id):
    document = get_object_or_404(Document, id=id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('upload_document')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'upload.html', {'form': form, 'documents': Document.objects.all(), 'edit': True, 'document_id': id})

def delete_document(request, id):
    document = get_object_or_404(Document, id=id)
    document.delete()
    return redirect('upload_document')

def compra_view(request):
    documents = Document.objects.all()
    return render(request, 'compra.html', {'documents': documents})

def confirmar_compra(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        articulos = json.dumps(data['articulos'])
        precio_total = data['precio_total']
        compra = Compra(articulos=articulos, precio_total=precio_total, fecha_hora=timezone.now())
        compra.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'})

def historial_compras(request):
    compras = Compra.objects.all()
    compras_data = []

    for compra in compras:
        articulos = json.loads(compra.articulos)  
        compras_data.append({
            'id': compra.id,
            'articulos': articulos,
            'precio_total': compra.precio_total,
            'fecha_hora': compra.fecha_hora,
        })

    return render(request, 'historial.html', {'compras': compras_data})
