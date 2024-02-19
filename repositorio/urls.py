from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm 
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
     
   path('signout', views.signout, name='signout'),
   path('inicio', views.inicio,name='inicio'),
   path('user-request/', views.user_request,name='user_request'),
   path('user-request-confirmation/', views.user_request_confirmation, name='user_request_confirmation'),

   
   #Manueales
   path('manuales',views.manuales, name='manuales' ),
   path('manuales/politica de calidad integral',views.politica, name='politica' ),
   path('manuales/Objetivos de calidad',views.objetivos, name='objetivos' ),

   #Recordar contraseña  
   path('reset_password/', 
        auth_views.PasswordResetView.as_view(template_name="cuentas/password_reset.html"),name="reset_password"),
   path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="cuentas/password_reset_sent.html"),name="password_reset_done"),
   path('reset/<uidb64>/<token>/', 
          PasswordResetConfirmView.as_view(
               template_name="cuentas/password_reset_form.html",
               form_class=CustomSetPasswordForm, 
          ),
          name="password_reset_confirm"),
          
   path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="cuentas/password_reset_done.html"),name="password_reset_complete"),

   # Visualizador
    path('ver-pdf/<int:id>/', views.ver_pdf, name='ver_pdf'),
    path('cadenavalor', views.cadenavalor, name='cadenavalor'),
  
      # Docencia de calidad
    path('cadenavalor/docenciacalidad',
         views.docenciac, name='docenciac'),
    path('cadenavalor/docenciac/Enseñanza aprendizaje y evaluación',
         views.enseñanzaprendizajeyevaluacion, name='enseñanzaprendizajeyevaluacion'),
    path('cadenavalor/docenciac/Desarrollo curricular',
         views.desarrollocurricular, name='desarrollocurricular'),
    
    # Investigacion pertinente
    path('cadenavalor/investigacionpertinente',
         views.investigacionp, name="investigacionp"),
    path('cadenavalor/investigacionpertinente/gestion de investigacion',
         views.gestioninvestigacion, name='gestioninvestigacion'),
    
    # Proyeccion social
    path('cadenavalor/extensionyproyección',
         views.extensioyp, name='extensioyp'),
    path('cadenavalor/extensionyproyeccion/extension y proyeccion social',
         views.extensionyproyeccion, name="extensionyproyeccion"),
    path('cadenavalor/extensionyproyeccion/Relacionamiento con egresados',
         views.relacionamientoconegresados, name="relacionaminetoconegresados"),
    path('cadenavalor/extensionyproyeccion/procedimientos/Relacionamiento con egresados',
         views.prorelacionamientoegresados, name="prorelacionamientoegresados"),

    #Procesos estrategicos
    path('cadenavalor/planeacionestra',
         views.planeacionestra, name='planeacionestra'),
    path('cadenavalor/planeacionestrategica/planeacion estrategica institucional',
         views.planeacionestrategica, name='planeacionestrategica'),
    path('cadenavalor/planeacionestrategica/gestión de la información',
         views.gestiondelainformacion, name='gestiondelainformacion'),
    path('cadenavalor/planeacionestrategica/procedimientos/Reporte de Información al SNIES',
         views.reporteSNIES, name='reporteSNIES'),

    #Relaciones Interinstitucionales
    path('cadenavalor/relacionesinter',
         views.relacionesinter, name='relacionesinter'),
    path('cadenavalor/relacionesinter/internacionalizacion',
         views.internacionalizacion, name='internacionalizacion'),
    path('cadenavalor/relacionesinter/comunicacion',
         views.comunicacion, name='comunicacion'),

    #Calidad Integral
    path('cadenavalor/calidadintegral',
         views.calidadintegral, name='calidadintegral'),
    path('cadenavlor/calidadintegral/auditorias',
         views.auditorias, name='auditorias'),
    path('cadenavalor/calidadintegral/gestionintegrada',
         views.gestionintegrada,name='gestionintegrada'), 
    path('cadenavalor/calidadintegral/servicioalpublico',
         views.servicioalpublico, name='servicioalpublico'),
    path('cadenavalor/calidadintegral/autoevaluacion y acreditacion',
         views.autoevaluacionyacreditacion, name='autoevaluacion y acreditacion'),
    path('cadenavalor/calidadintegral/aseguramiento de la calidad de procesos',
         views.aseguramientodelacalidadprocesos, name='aseguramientodelacalidadprocesos'),
    path('cadenavalor/calidadintegral/gestion del servicio al usuario',
          views.gestiondelservicioalusuario, name='gestiondelservicioalusuario'),
    path('cadenavalor/calidadintegral/gestiondel registro calificado',
          views.gestiondelregistrocalificado, name='gestiondelregistrocalificado'),
    path('cadenavalor/calidadintegral/aseguramiento de la calidad academica',
          views.aseguramientodelacalidadacademica, name='aseguramientodelacalidadacademica'),
    #Procedimientos
    path('cadenavalor/calidadintegral/procediminetos/Autoevaluación Programas',
         views.autoevaluacionprogramas,name="autoevaluacionprogramas"),
    path('cadenavalor/calidadintegral/procedimientos/Servicio al Cliente PQRs',
         views.servicioalclientepqr,name="servicioalclientepqr"),
    path('cadenavalor/calidadintegral/procedimientos/Creación de programas académicos',
         views.creacionprogramas,name="creacionprogramas"),
    path('cadenavalor/calidadintegral/procedimientos/Evaluación y control',
         views.evaluacionycontrol,name='evaluacionycontrol'),
    path('cadenavalor/calidadintegral/procedimientos/Modificación de los programas académicos',
         views.modificacionprogramas, name='modificacionprogramas'), 
    path('cadenavalor/calidadintegral/procedimientos/Pre-radicación de cumplimiento de condiciones de calidad institucional',
         views.preradicacion, name='preradicacion'), 
    
    #Talento Humano y Bienestar
    path('cadenavalor/talento humano bienestar',
         views.talentohumanobienestar,name="talentohumanobienestar"),
    path('cadenavalor/talentohumanobienestar/control disciplinario',
         views.controldisciplinario,name='controldisciplinario'),
    path('cadenavalor/talentohumanobienestar/bienestar institucional',
         views.bienestarinstitucional,name="bienestarinstitucional"),
    path('cadenavalor/talentohumanobienestar/pastoral',
         views.pastoral,name="pastoral"),
    path('cadenavalor/talentohumanobienestar/gestion y esarrollo humano',
         views.gestionydesarrollohumano,name="gestionydesarrollohumano"),
   #Procedimientos
   path('cadenavalor/talentohumanobienestar/procedimientos/Induccion a Estudiantes',
         views.induccionestudiantes,name="induccionestudiantes"),
    path('cadenavalor/talentohumanobienestar/procedimientos/Desarrollo e Implementación de Programas de Salud y Bienestar',
         views.saludybienestar,name="saludybienestar"),
    path('cadenavalor/talentohumanobienestar/procedimientos/Deteccion de plagio',
         views.plagio,name="plagio"),
    path('procedimientos/seleccion y contratación',
         views.procedimientogth,name='procedimientogth'),
    path('procedimientos/Inducción a colaboradores',
          views.induccioncolaboradores, name='induccioncolaboradores'),
    path('procedimientos/desvinculacion',
         views.desvinculacion,name="desvinculacion"),
    path('procedimientos/disciplinario',
         views.disciplinario,name="disciplinario"),

    # Procesos de apoyo
    #Gestión de infraestructura fisica y tecnologica
    path('cadenavalor/gestion de infraestructura',
         views.gestiondeinfraestructura, name='gestiondeinfraestructura'),
    path('cadenavalor/gestiondeinfraestructura/gestion de los sistemas de comunicacion y telecomunicaciones',
         views.gestionsistemas, name='gestionsistemas'),
    path('cadenavalor/gestiondeinfraestructura/gestion de la infraestructura fisica',
         views.infraestructurafisica, name='infraestructurafisica'),
    path('cadenavalor/gestiondeinfraestructura/gestion de la informacion bibliografica',
         views.informacionbibliografica, name='informacionbibliografica'),

    # Gestión administrativa y financiera
    path('cadenavalor/Gestión administrativa y financiera',
         views.gestionadminfinan, name='gestionadminfinan'),
    path('cadenavalor/gestionadminfinan/gestion cartera',
         views.gestioncartera, name='gestioncartera'),
    path('cadenavalor/gestion recursos financieros',
         views.gestionrefinanciero, name='gestionrefinanciero'),
    path('cadenavalor/gestion recursos financieros/gestión documental',
         views.gestiondocumental, name='gestiondocumental'),
    path('cadenavalor/gestión administrativa y financiera/gestion recursos financieros/procedimientos/Aplicación de becas descuento y patrocinios',
         views.becas, name='becas'),
    path('cadenavalor/gestión administrativa y financiera/gestion recursos financieros/procedimientos/Matriculas',
         views.matriculas, name='matriculas'),
    
    # Gestión de mercadeo
    path('cadenavalor/gestion de mercadeo',
         views.gestionmercadeo, name='gestionmercadeo'),
    path('cadenavalor/gestiondemercadeo/admisiones registro y control',
         views.adminregiscontrol, name='adminregiscontrol'),

    #Gestión Juridica y contractual
    path('cadenavalor/gestiónjuridicaycontractual',
         views.gestionjuridica, name='gestionjuridica'), 
    path('cadenavalor/gestiónjuridicaycontractual/gestion contractual',
          views.gestioncontractual, name='gestioncontractual'),
    path('cadenavalor/gestiónjuridicaycontractual/gestion juridica',
          views.gestjuridica, name='gesjuridica'),


    #CRUD Glosario
    path('Glosario', views.glosario, name='glosario'),
    path('nuevo_termino',views.nuevo_termino, name='nuevotermino'),
    path('editartermino/<int:id>/', views.editar_termino, name='editartermino'),
    path('eliminar_termino/<int:id>/', views.eliminar_termino, name='eliminartermino'),
    #CRUD Categorias
    path('categorias', views.categorias, name='categorias'),
    path('crearcategoria', views.crearcategoria, name='crearcategoria'),
    path('editarcategoria/<int:id>/', views.editarcategoria, name='editarcategoria'),
    path('eliminarcategoria/<int:id>/', views.eliminarcategoria, name='eliminarcategoria'),
    # CRUD PROCESOS
    path('procesos', views.procesos, name='procesos'),
    path('crearproceso', views.crearproceso, name='crearproceso'),
    path('editarproceso/<int:id>/', views.editarproceso, name='editarproceso'),
    path('eliminarproceso/<int:id>/', views.eliminarproceso, name='eliminarproceso'),

    # CRUD documentos
    path('documentos', views.documentos, name='documentos'),
    path('documentos/crear', views.crear, name='crear'),
    path('documentos/editar/<int:id>/', views.editardocumento, name='editardocumento'),
    path('documentos/eliminar/<int:id>/', views.eliminardocumento, name='eliminardocumento'),
    path('documents/<int:pk>/download/', views.download, name='download'),
]

