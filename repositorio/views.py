from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import Http404
from repositorio.forms import CategoriaForm, DocumentForm, ProcesoForm
from repositorio.models import Categoria, Document, Proceso
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q 
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.http import HttpResponseServerError
import logging

@login_required(login_url='signin')
def inicio(request):
    return render(request,'inicio.html')

@login_required(login_url='signin')
def cadenavalor(request):
    return render(request, 'cadenavalor.html')

@login_required(login_url='signin')
def manuales(request):
    return render(request,'manuales/manuales.html')
@login_required(login_url='signin')
def politica(request):
    return render(request,'manuales/politicadecalidadintegral.html')
@login_required(login_url='signin')
def objetivos(request):
    return render(request,'manuales/objetivospolitica.html')

# Vistas Login
@login_required(login_url='signin')
def signup(request):
    if request.method == 'GET':
        return render(request, 'cuentas/signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('inicio')
            except IntegrityError:
                return render(request, 'cuentas/signup.html', {
                    'form': UserCreationForm,
                    'error': 'El Usuario ya existe'
                })
        return render(request, 'cuentas/signup.html', {
            'form': UserCreationForm,
            'error': 'No coinciden las contraseñas'
        })

@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'GET':
        return render(request, 'cuentas/signin.html', {
            'form': AuthenticationForm
        })

    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'cuentas/signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario es incorrecto o no existe'
            })
        else:
            login(request, user)
            return redirect('inicio')
        
#CRUD CATEGORIAS
@login_required(login_url='signin')
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request,'categorias/categorias.html',{'categorias': categorias})

@login_required(login_url='signin')
def crearcategoria(request):
    formulario = CategoriaForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        categoria = Categoria(
            nombre_categoria = formulario.cleaned_data['nombre_categoria']
        )
        categoria.save()
        return redirect('categorias')
    return render(request,'categorias/crearcategoria.html',{'formulario': formulario})

@login_required(login_url='signin')
def editarcategoria(request, id):
    categoria = Categoria.objects.get(id_categoria=id)
    formulario = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
    return render(request,'categorias/editarcategoria.html', {'formulario': formulario})
@login_required(login_url='signin')
def eliminarcategoria(request, id):
    categoria = Categoria.objects.get(id_categoria=id)
    categoria.delete()
    return redirect('categorias')

#CRUD DOCUMENTOS
@login_required(login_url='signin')
def documentos(request):
    documentos_list = Document.objects.all()

    # Lógica de búsqueda
    query = request.GET.get('q')
    if query:
        documentos_list = documentos_list.filter(
            Q(titulo__icontains=query) |
            Q(id_archivo__icontains=query) |
            Q(categoria__nombre_categoria__icontains=query)|
            Q(proceso__nombre_proceso__icontains=query)
        )

    # Configura el paginador, aquí se configura para mostrar 10 documentos por página
    paginator = Paginator(documentos_list, 10)
    page = request.GET.get('page')

    try:
        documentos = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        documentos = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), muestra la última página
        documentos = paginator.page(paginator.num_pages)

    return render(request, 'documentos/documentos.html', {'documentos': documentos, 'query': query})



def crear(request):
    formulario = DocumentForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():
        # Crea un nuevo documento
        documento = Document(
            proceso=formulario.cleaned_data['proceso'],
            codigo = formulario.cleaned_data['codigo'],
            categoria=formulario.cleaned_data['categoria'],
            titulo=formulario.cleaned_data['titulo'],
            file=formulario.cleaned_data['file'],
           
        )

        # Guarda el documento en la base de datos
        documento.save()

        return redirect('documentos')
    
    return render(request, 'documentos/creardocumento.html', {'formulario': formulario})

@login_required(login_url='signin')
def editardocumento(request, id):
    documento = get_object_or_404(Document, id_archivo=id)
    formulario = DocumentForm(request.POST or None, request.FILES or None, instance=documento)
    
    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            return redirect('documentos')

    return render(request, 'documentos/editardocumento.html', {'formulario': formulario})

@login_required(login_url='signin')
@permission_required('delete_document', raise_exception=True)
def eliminardocumento(request, id):
    try:
        documento = Document.objects.get(id_archivo=id)
        # Asegúrate de que el documento existe antes de intentar eliminarlo
        if documento:
            # Elimina el documento
            documento.delete()
            return redirect('documentos')
        else:
            raise Http404("El documento no existe.")
    except Document.DoesNotExist:
        raise Http404("El documento no existe.")

@login_required(login_url='signin')
@permission_required('download_document', raise_exception=True)
def download(request, pk):
    document = get_object_or_404(Document, pk=pk)
    response = HttpResponse(document.file.read())
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        document.file.name)
    return response

#CRUD PROCESOS
@login_required(login_url='signin')
def procesos(request):
    procesos = Proceso.objects.all()
    return render(request,'procesos/procesos.html',{'procesos': procesos})

@login_required(login_url='signin')
def crearproceso(request):
    formulario = ProcesoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        proceso = Proceso(
            nombre_proceso = formulario.cleaned_data['nombre_proceso']
        )
        proceso.save()
        return redirect('procesos')
    return render(request,'procesos/crearproceso.html',{'formulario': formulario})

@login_required(login_url='signin')
def editarproceso(request, id):
    proceso = get_object_or_404(Proceso, id_proceso=id)
    formulario = ProcesoForm(request.POST or None, request.FILES or None, instance=proceso)
    
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirect('procesos', id=id)  # Redirige a la vista de detalle del proceso
    
    return render(request, 'procesos/editarproceso.html', {'formulario': formulario})

@login_required(login_url='signin')
def eliminarproceso(request, id):
    proceso = Proceso.objects.get(id_proceso=id)
    proceso.delete()
    return redirect('procesos')


#Visualizar Documentos
@xframe_options_exempt
def ver_pdf(request, id):
    document = get_object_or_404(Document, id_archivo=id)
    file_path = document.file.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

#Procesos Misionales
#Docencia Calidad
@login_required(login_url='signin')
def docenciac(request):
    return render(request, 'procesos/docenciac.html')
@login_required(login_url='signin')
def docenciacalidad(request):
    documentos = Document.objects.filter(titulo__iexact='Gestión de docencia')
    

    context = {'documentos': documentos}
    return render(request, 'procesos/docenciacalidad/docenciacalidad.html', context)

#Investigacion Pertinente
@login_required(login_url='signin')
def investigacionp(request):
    return render(request, 'procesos/investigacionpertinente.html')

@login_required(login_url='signin')
def gestioninvestigacion(request):
    documentos  = Document.objects.filter(titulo__iexact='Gestión de investigación')

    context = {'documentos': documentos}
    return render(request, 'procesos/investigacionpertinente/gestiondeinvestigacion.html', context)

#Proyeccion Social
@login_required(login_url='signin')
def extensioyp(request):
    return render(request, 'procesos/extensionproyeccion.html')
@login_required(login_url='signin')
def extensionyproyeccion(request):
    documentos = Document.objects.filter(titulo__iexact='Extensión y Proyección social')
    context ={'documentos': documentos}
    return render(request, 'procesos/proyeccionsocial/extensionproyeccion.html',context)

#Procesos Estrategicos
#Planeación Estrategicas
@login_required(login_url='signin')
def planeacionestra(request):
    return render(request, 'procesos/planeacionestra.html')
@login_required(login_url='signin')
def planeacionestrategica(request):
    documentos = Document.objects.filter(titulo__iexact='Planeación estratégica institucional')
    context = {'documentos': documentos}
    return render(request, 'procesos/planeacionestrategica/planeacionestrategica.html', context)

#Relaciones Interinstitucionales
@login_required(login_url='signin')
def relacionesinter(request):
    return render(request, 'procesos/relacionesinter.html')
@login_required(login_url='signin')
def internacionalizacion(request):
    return render(request, 'procesos/relacionesinter/internacionalizacion.html')
@login_required(login_url='signin')
def comunicacion(request):
    return render(request, 'procesos/relacionesinter/comunicacion.html')

#Calidad Integral
@login_required(login_url='signin')
def calidadintegral(request):
    return render(request, 'procesos/calidadintegral.html')
@login_required(login_url='signin')
def autoevaluacionyacreditacion(request):
    return render(request, 'procesos/calidadintegral/autoevaluacionyacreditacion.html')
@login_required(login_url='signin')
def gestiondelservicioalusuario(request):
    return render(request,'procesos/calidadintegral/gestiondelservicioalusuario.html')
@login_required(login_url='signin')
def gestiondelregistrocalificado(request):
    return render(request,'procesos/calidadintegral/gestiondelregistrocalificado.html')
@login_required(login_url='signin')
def aseguramientodelacalidadacademica(request):
    return render(request,'procesos/calidadintegral/aseguramientodelacalidadacademica.html')
@login_required(login_url='signin')
def auditorias(request):
    return render(request,'procesos/calidadintegral/auditorias.html')
@login_required(login_url='signin')
def gestionintegrada(request):
    return render(request,'procesos/calidadintegral/gestionintegrada.html')
login_required(login_url='signin')
def servicioalpublico(request):
    return render(request, 'procesos/calidadintegral/servicioalpublico.html')
login_required(login_url='signin')
def aseguramientodelacalidadprocesos(request):
    return render(request, 'procesos/calidadintegral/aseguramientodelacalidadprocesos.html')

#Talento humano y Bienestar
@login_required(login_url='signin')
def talentohumanobienestar(request):
    return render(request,'procesos/talentohumanobienestar.html')
@login_required(login_url='signin')
def controldisciplinario (request):
    return render(request,'procesos/talentohumanobienestar/controldisciplinario.html')
@login_required(login_url='signin')
def bienestarinstitucional(request):
    return render(request,'procesos/talentohumanobienestar/bienestarinstitucional.html')
@login_required(login_url='signin')
def pastoral(request):
    return render(request,'procesos/talentohumanobienestar/pastoral.html')
@login_required(login_url='signin')
def gestionydesarrollohumano(request):
    return render(request,'procesos/talentohumanobienestar/gestionydesarrollohumano.html')
@login_required(login_url='signin')
def procedimientogth(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/seleccionycontratacion.html')

#Procesos de Apoyo
#Gestion administrativa y financiera
@login_required(login_url='signin')
def gestionadminfinan(request):
    return render(request, 'procesos/gestionadminfinan.html')
@login_required(login_url='signin')
def gestioncartera(request):
    return render(request, 'procesos/gestionadministrativa/gestioncartera.html')
@login_required(login_url='signin')
def gestionrefinanciero(request):
    return render(request, 'procesos/gestionadministrativa/gestionrefinanciero.html')

#Gestion Mercadeo y Admisiones
@login_required(login_url='signin')
def gestionmercadeo(request):
    return render(request, 'procesos/gestiondemercadeo.html')
@login_required(login_url='signin')
def adminregiscontrol(request):
    return render(request, 'procesos/gestionmercadeo/admisionesregistrocon.html')

#Gestión de infraestructura
@login_required(login_url='signin')
def gestiondeinfraestructura(request):
    return render(request, 'procesos/gestiondeinfraestructura.html')
@login_required(login_url='signin')
def gestionsistemas(request):
    return render(request,'procesos/gestiondeinfraestructura/gestiondesistemascomunicacion.html')
@login_required(login_url='signin')
def infraestructurafisica(request):
    return render(request,'procesos/gestiondeinfraestructura/infraestructurafisica.html')
@login_required(login_url='signin')
def informacionbibliografica(request):
    return render(request,'procesos/gestiondeinfraestructura/informacionbibliografica.html')

#Gestión juridica y contractual
@login_required(login_url='signin')
def gestionjuridica(request):
    return render(request, 'procesos/gestionjuridica.html')
@login_required(login_url="signin")
def gestioncontractual(request):
    return render(request,'procesos/gestionjuridica/gestioncontractual.html')
@login_required(login_url="signin")
def gestjuridica(request):
    return render(request,'procesos/gestionjuridica/gestionjuridica.html')
