from urllib import request
from django.shortcuts import render
from .models import Alumnos, Comentario
from .forms import ComentarioContactoForm
from .models import ComentarioContacto
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
import datetime
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages


# Create your views here.

def registros(request):
    alumnos=Alumnos.objects.all()
    return render(request, "registros/principal.html",{'alumnos':alumnos})

def registrar(request):
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid():
            form.save()
            comentarios=ComentarioContacto.objects.all()
            return render(request,'registros/mensaje.html',
                {'comentarios':comentarios})
    form = ComentarioContactoForm()
    return render(request,'registros/contacto.html',{'form':form})

def contacto(request):
    return render(request,"registros/contacto.html")

def comentario(request):
    comentario=ComentarioContacto.objects.all()
    return render(request, "registros/mensaje.html",{'comentario':comentario})


def eliminarComentarioContacto(request, id,
        confirmacion='registros/confirmarEliminacion.html'):
        comentario=get_object_or_404(ComentarioContacto, id=id)
        if request.method=='POST':
             comentario.delete()
             comentario=ComentarioContacto.objects.all()
             return render(request,"registros/mensaje.html",
                           {'comentario':comentario})
        return render(request, confirmacion, {'object':comentario})


def editarComentario(request, id):
    comentario = get_object_or_404(ComentarioContacto, id=id)

    if request.method == 'POST':
        comentario.usuario = request.POST.get('usuario')
        comentario.mensaje = request.POST.get('mensaje')
        comentario.save()
        return redirect('Mensaje')

    return render(request, 'registros/editar.html', {'comentario': comentario})


def consultar1(request):
    alumnos=Alumnos.objects.filter(carrera="TI")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar2(request):
    alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar3(request):
    alumnos=Alumnos.objects.all().only("matricula", "nombre", "carrera", "turno", "imagen")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar4(request):
    alumnos=Alumnos.objects.filter(turno__contains="Vesp")
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar5(request):
    alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar6(request):
    fechaInicio=datetime.date(2025, 10, 28)
    fechaFin=datetime.date(2025, 11, 26)
    alumnos=Alumnos.objects.filter(created__range=(fechaInicio,fechaFin))
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar7(request):
    alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
    return render(request, "registros/consultas.html",{'alumnos':alumnos})

def consultar8(request):
    comentarios = ComentarioContacto.objects.filter(mensaje__startswith='h')
    return render(request, "registros/consultas.html", {'comentarios': comentarios})


def archivos(request):
    if request.method == 'POST':
        form = FormArchivos(request.POST, request.FILES)
        if form.is_valid():
            titulo = request.POST['titulo']
            descripcion = request.POST['descripcion']
            archivo = request.FILES['archivo']
            insert = Archivos(titulo=titulo, descripcion=descripcion,
            archivo=archivo)
            insert.save()
            return render(request,"registros/archivos.html")
        else:
            messages.error(request, "Error al procesar el formulario")
    else:
        return render(request,"registros/archivos.html",{'archivo':Archivos})
        
    








