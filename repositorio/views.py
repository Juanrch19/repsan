from django.http import FileResponse, HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt
from django.http import Http404
from django.core.files.storage import default_storage
from repositorio.forms import CategoriaForm, DocumentForm, LoginForm, ProcesoForm, UserRequestForm,GlosarioForm
from repositorio.models import Categoria, Document, Proceso,Glosario
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db.models import Q 
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from django.http import HttpResponseServerError
from django.contrib.auth import login as auth_login


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'], password = cd['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('inicio')
                else:
                    return HttpResponse('No se encuentra la cuenta')
            else:
                return HttpResponse('Inicio de sesion invalido')
    else:
        form = LoginForm()
    return render(request,'cuentas/index.html',{'form':form})   

@login_required(login_url='login')
def inicio(request):
    return render(request,'inicio.html')

@login_required(login_url='login')
def cadenavalor(request):
    ultimos_archivos = Document.objects.order_by('-fecha_creacion')[:3]  # Obtén los últimos 5 archivos
    
    # Pasar los archivos al contexto del template
    context = {'ultimos_archivos': ultimos_archivos}
    
    return render(request, 'cadenavalor.html',context)

@login_required(login_url='login')
def manuales(request):
    return render(request,'manuales/manuales.html')
@login_required(login_url='login')
def politica(request):
    return render(request,'manuales/politicadecalidadintegral.html')
@login_required(login_url='login')
def objetivos(request):
    return render(request,'manuales/objetivospolitica.html')

# Vistas Login
def user_request(request):
    if request.method == 'POST':
        form = UserRequestForm(request.POST)
        if form.is_valid():
            # Procesar la solicitud y enviarla al administrador
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            reason = form.cleaned_data['reason']
            
            # Envía un correo electrónico al administrador con los detalles de la solicitud
            send_mail(
                'Solicitud de usuario',
                f'Se ha recibido una solicitud de usuario:\nNombre: {full_name}\nCorreo electrónico: {email}\nMotivo: {reason}',
                'from@example.com',
                ['proluxgamer456@gmail.com'],  # Reemplaza admin@example.com con la dirección de correo electrónico del administrador
                fail_silently=False,
            )

            # Redirigir a una página de confirmación
            return redirect('user_request_confirmation')
    else:
        form = UserRequestForm()
    return render(request, 'cuentas/user_request.html', {'form': form})

def user_request_confirmation(request):
    return render(request,'cuentas/user_request_confirmation.html')
        
@login_required(login_url='login')
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

@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect(reverse('login'))


#CRUD GLOSARIO
login_required(login_url='login')
def glosario(request):
    glosario_list = Glosario.objects.all().order_by('termino')

    query = request.GET.get('q')
    if query:
        glosario_list = glosario_list.filter(
            Q(termino__icontains=query) |
            Q(definicion__icontains=query)
        )

    paginator = Paginator (glosario_list, 30)
    page = request.GET.get('page')

    try:
        terminos = paginator.page(page)
    except PageNotAnInteger:
        # Si la página no es un número entero, muestra la primera página
        terminos = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango (por ejemplo, 9999), muestra la última página
        terminos = paginator.page(paginator.num_pages) 
    return render(request,'glosario/glosario.html',{'terminos': terminos, 'query':query})

login_required(login_url='login')
def nuevo_termino(request):
    """ Función para agregar un nuevo termino al glosario"""
    formulario = GlosarioForm(request.POST or None )
    if formulario.is_valid():
        glosario = Glosario(
            termino = formulario.cleaned_data['termino'],
            definicion = formulario.cleaned_data['definicion']
        ) 
        glosario.save()
        return redirect ('glosario')
    return render(request,'glosario/nuevo_termino.html',{'formulario':formulario})

login_required(login_url='login')
def editar_termino(request, id):
    termino = Glosario.objects.get(id_termino = id)
    formulario = GlosarioForm(request.POST or None, instance=termino)
    return render(request,'glosario/editartermino.html',{'formulario':formulario})

login_required(login_url='login')
def eliminar_termino(request, id):
    termino = Glosario.objects.get(id_termino = id)
    termino.delete()
    return redirect('glosario')

#CRUD CATEGORIAS
@login_required(login_url='login')
def categorias(request):
    categorias = Categoria.objects.all()
    return render(request,'categorias/categorias.html',{'categorias': categorias})

@login_required(login_url='login')
def crearcategoria(request):
    formulario = CategoriaForm(request.POST or None)
    if formulario.is_valid():
        categoria = Categoria(
            nombre_categoria = formulario.cleaned_data['nombre_categoria']
        )
        categoria.save()
        return redirect('categorias')
    return render(request,'categorias/crearcategoria.html',{'formulario': formulario})

@login_required(login_url='login')
def editarcategoria(request, id):
    categoria = Categoria.objects.get(id_categoria=id)
    formulario = CategoriaForm(request.POST or None, request.FILES or None, instance=categoria)
    return render(request,'categorias/editarcategoria.html', {'formulario': formulario})

@login_required(login_url='login')
def eliminarcategoria(request, id):
    categoria = Categoria.objects.get(id_categoria=id)
    categoria.delete()
    return redirect('categorias')

#CRUD DOCUMENTOS
@login_required(login_url='login')
def documentos(request):
    documentos_list = Document.objects.all().order_by('id_archivo') 

    # Lógica de búsqueda
    query = request.GET.get('q')
    if query:
        documentos_list = documentos_list.filter(
            Q(titulo__icontains=query) |
            Q(codigo__icontains=query) |
            Q(id_archivo__icontains=query) |
            Q(categoria__nombre_categoria__icontains=query)|
            Q(proceso__nombre_proceso__icontains=query)
        )

    # Configura el paginador, aquí se configura para mostrar 10 documentos por página
    paginator = Paginator(documentos_list, 30)
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

@login_required(login_url='login')
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

@login_required(login_url='login')
def editardocumento(request, id):
    documento = get_object_or_404(Document, id_archivo=id)
    formulario = DocumentForm(request.POST or None, request.FILES or None, instance=documento)
    
    if request.method == 'POST':
        if formulario.is_valid():
            # Verificar si se carga un nuevo archivo
            if 'file' in request.FILES:
                # Eliminar el archivo anterior
                if documento.file:
                    file_path = documento.file.path
                    default_storage.delete(file_path)
            formulario.save()
            return redirect('documentos')

    return render(request, 'documentos/editardocumento.html', {'formulario': formulario})

@login_required(login_url='login')
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

@login_required(login_url='login')
def download(request, pk):
    document = get_object_or_404(Document, pk=pk)
    response = HttpResponse(document.file.read())
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(
        document.file.name)
    return response

#Visualizar Documentos
@login_required(login_url='login')
@xframe_options_exempt
def ver_pdf(request, id):
    document = get_object_or_404(Document, id_archivo=id)
    file_path = document.file.path
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
#CRUD PROCESOS
@login_required(login_url='login')
def procesos(request):
    procesos = Proceso.objects.all().order_by('id_proceso')
    return render(request,'procesos/procesos.html',{'procesos': procesos})

@login_required(login_url='login')
def crearproceso(request):
    formulario = ProcesoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        proceso = Proceso(
            nombre_proceso = formulario.cleaned_data['nombre_proceso']
        )
        proceso.save()
        return redirect('procesos')
    return render(request,'procesos/crearproceso.html',{'formulario': formulario})

@login_required(login_url='login')
def editarproceso(request, id):
    proceso = get_object_or_404(Proceso, id_proceso=id)
    def tributar():
        pass
    formulario = ProcesoForm(request.POST or None, request.FILES or None, instance=proceso)
    
    if request.method == 'POST' and formulario.is_valid():
        formulario.save()
        return redirect('procesos', id=id)  # Redirige a la vista de detalle del proceso
    
    return render(request, 'procesos/editarproceso.html', {'formulario': formulario})

@login_required(login_url='login')
def eliminarproceso(request, id):
    proceso = Proceso.objects.get(id_proceso=id)
    proceso.delete()
    return redirect('procesos')



#Procesos Misionales
#Docencia Calidad
@login_required(login_url='login')
def docenciac(request):
    return render(request, 'procesos/docenciac.html')
@login_required(login_url='login')
def enseñanzaprendizajeyevaluacion(request):
    documentos = Document.objects.filter(titulo__iexact='Enseñanza aprendizaje y evaluación')
    

    context = {'documentos': documentos}
    return render(request, 'procesos/docenciacalidad/enseñanzaprendizajeyevaluacion.html', context)
@login_required(login_url='login')
def desarrollocurricular(request):
    documentos = Document.objects.filter(titulo__iexact='Desarrollo curricular')
    

    context = {'documentos': documentos}
    return render(request, 'procesos/docenciacalidad/desarrollocurricular.html', context)

#Investigacion Pertinente
@login_required(login_url='login')
def investigacionp(request):
    return render(request, 'procesos/investigacionpertinente.html')

@login_required(login_url='login')
def gestioninvestigacion(request):
    documentos  = Document.objects.filter(titulo__iexact='Gestión de investigación')

    context = {'documentos': documentos}
    return render(request, 'procesos/investigacionpertinente/gestiondeinvestigacion.html', context)

#Proyeccion Social
@login_required(login_url='login')
def extensioyp(request):
    return render(request, 'procesos/extensionproyeccion.html')
@login_required(login_url='login')
def extensionyproyeccion(request):
    documentos = Document.objects.filter(titulo__iexact='Extensión y Proyección social')
    context ={'documentos': documentos}
    return render(request, 'procesos/proyeccionsocial/extensionproyeccion.html',context)
@login_required(login_url='login')
def relacionamientoconegresados(request):
    documentos = Document.objects.filter(titulo__iexact='Relacionamiento con egresados')
    context ={'documentos': documentos}
    return render(request, 'procesos/proyeccionsocial/relacionamientoconegresados.html',context)
@login_required(login_url='login')
def prorelacionamientoegresados(request):
    documentos = Document.objects.filter(titulo__iexact='Relacionamiento con egresados')
    context ={'documentos': documentos}
    return render(request, 'procesos/proyeccionsocial/procedimientos/relacionamientoegresados.html',context)

#Procesos Estrategicos
#Planeación Estrategicas
@login_required(login_url='login')
def planeacionestra(request):
    return render(request, 'procesos/planeacionestra.html')
@login_required(login_url='login')
def planeacionestrategica(request):
    documentos = Document.objects.filter(titulo__iexact='Planeación estratégica institucional')
    context = {'documentos': documentos}
    return render(request, 'procesos/planeacionestrategica/planeacionestrategica.html', context)
@login_required(login_url='login')
def gestiondelainformacion(request):
    documentos = Document.objects.filter(titulo__iexact='Gestión de la información')
    context = {'documentos': documentos}
    return render(request, 'procesos/planeacionestrategica/gestiondelainformacion.html', context)
@login_required(login_url='login')
def reporteSNIES(request):
    return render(request,'procesos/planeacionestrategica/procedimientos/reporteSNIES.html')

#Relaciones Interinstitucionales
@login_required(login_url='login')
def relacionesinter(request):
    return render(request, 'procesos/relacionesinter.html')
@login_required(login_url='login')
def internacionalizacion(request):
    return render(request, 'procesos/relacionesinter/internacionalizacion.html')
@login_required(login_url='login')
def comunicacion(request):
    return render(request, 'procesos/relacionesinter/comunicacion.html')

#Calidad Integral
@login_required(login_url='login')
def calidadintegral(request):
    return render(request, 'procesos/calidadintegral.html')
@login_required(login_url='login')
def autoevaluacionyacreditacion(request):
    return render(request, 'procesos/calidadintegral/autoevaluacionyacreditacion.html')
@login_required(login_url='login')
def gestiondelservicioalusuario(request):
    return render(request,'procesos/calidadintegral/gestiondelservicioalusuario.html')
@login_required(login_url='login')
def gestiondelregistrocalificado(request):
    return render(request,'procesos/calidadintegral/gestiondelregistrocalificado.html')
@login_required(login_url='login')
def aseguramientodelacalidadacademica(request):
    return render(request,'procesos/calidadintegral/aseguramientodelacalidadacademica.html')
@login_required(login_url='login')
def auditorias(request):
    return render(request,'procesos/calidadintegral/auditorias.html')
@login_required(login_url='login')
def gestionintegrada(request):
    return render(request,'procesos/calidadintegral/gestionintegrada.html')
login_required(login_url='login')
def servicioalpublico(request):
    return render(request, 'procesos/calidadintegral/servicioalpublico.html')
login_required(login_url='login')
def aseguramientodelacalidadprocesos(request):
    return render(request, 'procesos/calidadintegral/aseguramientodelacalidadprocesos.html')
#Procedimientos
login_required(login_url='login')
def renovacionregistro(request):
    return render(request,'procesos/calidadintegral/procedimientos/renovacionregistro.html')
login_required(login_url='login')
def creacionprogramas(request):
    return render(request,'procesos/calidadintegral/procedimientos/creacionprogramas.html')
login_required(login_url='login')
def evaluacionycontrol(request):
    return render(request,'procesos/calidadintegral/procedimientos/evaluacionycontrol.html')
login_required(login_url='login')
def modificacionprogramas(request):
    return render(request,'procesos/calidadintegral/procedimientos/modificacionprogramas.html')
login_required(login_url='login')
def preradicacion(request):
    return render(request,'procesos/calidadintegral/procedimientos/preradicacion.html')
login_required(login_url='login')
def servicioalclientepqr(request):
    return render(request,'procesos/calidadintegral/procedimientos/servicioalclientepqr.html')
login_required(login_url='login')
def autoevaluacionprogramas(request):
    return render(request,'procesos/calidadintegral/procedimientos/autoevaluacionprogramas.html')
#Talento humano y Bienestar
@login_required(login_url='login')
def talentohumanobienestar(request):
    return render(request,'procesos/talentohumanobienestar.html')
@login_required(login_url='login')
def controldisciplinario (request):
    return render(request,'procesos/talentohumanobienestar/controldisciplinario.html')
@login_required(login_url='login')
def bienestarinstitucional(request):
    return render(request,'procesos/talentohumanobienestar/bienestarinstitucional.html')
@login_required(login_url='login')
def pastoral(request):
    return render(request,'procesos/talentohumanobienestar/pastoral.html')
@login_required(login_url='login')
def gestionydesarrollohumano(request):
    return render(request,'procesos/talentohumanobienestar/gestionydesarrollohumano.html')

#Procedimientos
login_required(login_url='login')
def induccionestudiantes(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/induccionestudiantes.html')
login_required(login_url='login')
def saludybienestar(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/saludybienestar.html')
login_required(login_url='login')
def plagio(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/plagio.html')
@login_required(login_url='login')
def induccioncolaboradores(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/induccionacolaboradores.html')
@login_required(login_url='login')
def procedimientogth(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/seleccionycontratacion.html')
@login_required(login_url='login')
def desvinculacion(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/desvinculacion.html')
@login_required(login_url='login')
def disciplinario(request):
    return render(request,'procesos/talentohumanobienestar/procedimientos/disciplinario.html')

#Procesos de Apoyo
#Gestion administrativa y financiera
@login_required(login_url='login')
def gestionadminfinan(request):
    return render(request, 'procesos/gestionadminfinan.html')
@login_required(login_url='login')
def gestioncartera(request):
    return render(request, 'procesos/gestionadministrativa/gestioncartera.html')
@login_required(login_url='login')
def gestionrefinanciero(request):
    return render(request, 'procesos/gestionadministrativa/gestionrefinanciero.html')
@login_required(login_url='login')
def gestiondocumental(request):
    return render(request, 'procesos/gestionadministrativa/gestiondocumental.html')
@login_required(login_url='login')
def becas(request):
    return render(request, 'procesos/gestionadministrativa/procedimientos/becas.html')
@login_required(login_url='login')
def matriculas(request):
    return render(request, 'procesos/gestionadministrativa/procedimientos/matriculas.html')

#Gestion Mercadeo y Admisiones
@login_required(login_url='login')
def gestionmercadeo(request):
    return render(request, 'procesos/gestiondemercadeo.html')
@login_required(login_url='login')
def adminregiscontrol(request):
    return render(request, 'procesos/gestionmercadeo/admisionesregistrocon.html')

#Gestión de infraestructura
@login_required(login_url='login')
def gestiondeinfraestructura(request):
    return render(request, 'procesos/gestiondeinfraestructura.html')
@login_required(login_url='login')
def gestionsistemas(request):
    return render(request,'procesos/gestiondeinfraestructura/gestiondesistemascomunicacion.html')
@login_required(login_url='login')
def infraestructurafisica(request):
    return render(request,'procesos/gestiondeinfraestructura/infraestructurafisica.html')
@login_required(login_url='login')
def informacionbibliografica(request):
    return render(request,'procesos/gestiondeinfraestructura/informacionbibliografica.html')
#Procedimientos
@login_required(login_url='login')
def asignacioninfraestructura(request):
    return render(request,'procesos/gestiondeinfraestructura/procedimientos/asignacioninfraestructura.html')

#Gestión juridica y contractual
@login_required(login_url='login')
def gestionjuridica(request):
    return render(request, 'procesos/gestionjuridica.html')
@login_required(login_url="signin")
def gestioncontractual(request):
    return render(request,'procesos/gestionjuridica/gestioncontractual.html')
@login_required(login_url="signin")
def gestjuridica(request):
    return render(request,'procesos/gestionjuridica/gestionjuridica.html')
