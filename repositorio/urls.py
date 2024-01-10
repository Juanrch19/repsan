from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomSetPasswordForm 
from django.contrib.auth.views import PasswordResetConfirmView


urlpatterns = [
   path('signout', views.signout, name='signout'),
   path('inicio', views.inicio,name='inicio'),
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
    path('cadenavalor/docenciacalidad',
         views.docenciac, name='docenciac'),

      # Docencia de calidad
    path('cadenavalor/docenciacalidad',
         views.docenciac, name='docenciac'),
    path('cadenavalor/docenciac/docenciacalidad',
         views.docenciacalidad, name='docenciacalidad'),
    
    # Investigacion pertinente
    path('cadenavalor/investigacionpertinente',
         views.investigacionp, name="investigacionp"),
    path('cadenavalor/investigacionpertinente/gestioninvestigacion',
         views.gestioninvestigacion, name='gestioninvestigacion'),
    
    # Proyeccion social
    path('cadenavalor/extensionyproyección',
         views.extensioyp, name='extensioyp'),
    path('cadenavalor/extensionyproyeccion/extensionyproyeccionsocial',
         views.extensionyproyeccion, name="extensionyproyeccion"),

    #Procesos estrategicos
    path('cadenavalor/planeacionestra',
         views.planeacionestra, name='planeacionestra'),
    path('cadenavalor/planeacionestrategica/planeacionestrategicainstitucional',
         views.planeacionestrategica, name='planeacionestrategica'),

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
    path('cadenavlor/calidadintegral/evaluacionycontrol',
         views.evaluacionycontrol, name='evaluacionycontrol'),
    path('cadenavalor/calidadintegral/gestionintegrada',
         views.gestionintegrada,name='gestionintegrada'), 
    path('cadenavalor/calidadintegral/servicioalpublico',
         views.servicioalpublico, name='servicioalpublico'),
    path('cadenavalor/calidadintegral/autoevaluacionyacreditacion',
         views.autoevaluacionyacreditacion, name='autoevaluacionyacreditacion'),
    path('cadenavalor/calidadintegral/aseguramiento de la calidad de procesos',
         views.aseguramientodelacalidadprocesos, name='aseguramientodelacalidadprocesos'),
    
    #Talento Humano y Bienestar
    path('cadenavalor/talentohumanobienestar',
         views.talentohumanobienestar,name="talentohumanobienestar"),
    path('cadenavalor/talentohumanobienestar/controldisciplinario',
         views.controldisciplinario,name='controldisciplinario'),
    path('cadenavalor/talentohumanobienestar/bienestarinstitucional',
         views.bienestarinstitucional,name="bienestarinstitucional"),
    path('cadenavalor/talentohumanobienestar/pastoral',
         views.pastoral,name="pastoral"),
    path('cadenavalor/talentohumanobienestar/gestionydesarrollohumano',
         views.gestionydesarrollohumano,name="gestionydesarrollohumano"),
    path('procedimientos/seleccion y contratación',
         views.procedimientogth,name='procedimientogth'),
    # Procesos de apoyo
    
    #Gestión de infraestructura fisica y tecnologica
    path('cadenavalor/gestiondeinfraestructura',
         views.gestiondeinfraestructura, name='gestiondeinfraestructura'),
    path('cadenavalor/gestiondeinfraestructura/gestion de los sistemas de comunicacion y telecomunicaciones',
         views.gestionsistemas, name='gestionsistemas'),
    path('cadenavalor/gestiondeinfraestructura/gestiondelainfraestructurafisica',
         views.infraestructurafisica, name='infraestructurafisica'),
    path('cadenavalor/gestiondeinfraestructura/gestiondelainformacionbibliografica',
         views.informacionbibliografica, name='informacionbibliografica'),

    # Gestión administrativa y financiera
    path('cadenavalor/Gestión administrativa y financiera',
         views.gestionadminfinan, name='gestionadminfinan'),
    path('cadenavalor/gestionadminfinan/gestioncartera',
         views.gestioncartera, name='gestioncartera'),
    path('cadenavalor/gestionrefinanciero',
         views.gestionrefinanciero, name='gestionrefinanciero'),
    
    # Gestión de mercadeo
    path('cadenavalor/gestiondemercadeo',
         views.gestionmercadeo, name='gestionmercadeo'),
    path('cadenavalor/gestiondemercadeo/admisionesregistroycontrol',
         views.adminregiscontrol, name='adminregiscontrol'),

    #Gestión Juridica y contractual
    path('cadenavalor/gestiónjuridicaycontractual',
         views.gestionjuridica, name='gestionjuridica'), 
    path('cadenavalor/gestiónjuridicaycontractual/gestioncontractual',
          views.gestioncontractual, name='gestioncontractual'),
    path('cadenavalor/gestiónjuridicaycontractual/gestionjuridica',
          views.gestjuridica, name='gesjuridica'),


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

