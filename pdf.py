from flask import Blueprint
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from flask import make_response, request
from datetime import datetime

from bd import seleccionar

bp = Blueprint('descargar', __name__) #al llamar el blue print en base sería (NomreBP.FuncionAsociadaARuta)

@bp.route('/descargar', methods=['POST'])

def generar_pdf():
    # Crear un objeto de lienzo PDF
    buffer = BytesIO()  # Crear un buffer de bytes para almacenar el PDF generado
    pdf = canvas.Canvas(buffer)

    id_pdf = request.form.get('id_pdf')

    titulo = f"ASISTENCIA - {id_pdf}"
    pdf.setTitle(titulo)

    data = seleccionar()
    dibujar_encabezado(pdf,50,600)
    dibujar_body(pdf,data,0,510)
    dibujar_footer(pdf,50,50)

    pdf.setPageSize((600, 650))  # Establecer un ancho de 500 puntos y un alto de 700 puntos
    # Guardar el lienzo y finalizar el PDF
    pdf.save()

    buffer.seek(0)  # Restablecer el puntero del buffer al principio
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={titulo}.pdf'
    return response

# ENCABEZADO
def dibujar_encabezado(pdf,x_encabezado,y_encabezado):
    # Definir las coordenadas para el encabezado y la línea
    x_linea = 50  # posición x de la línea
    y_linea = y_encabezado - 10  # posición y de la línea (ajusta la separación)
    # Configurar la fuente y el tamaño del texto del encabezado
    pdf.setFont("Helvetica-Bold", 18)
    # Dibujar el encabezado
    pdf.drawString(x_encabezado, y_encabezado, "ASISTENCIAS : FISI - UNMSM")
    # Dibujar la línea
    pdf.setLineWidth(5)  # grosor de la línea
    pdf.setStrokeColorRGB(4/255, 26/255, 47/255) 
    pdf.line(x_linea, y_linea, pdf._pagesize[0] - x_linea, y_linea)  # dibujar línea horizontal

# BODY
def dibujar_body(pdf,data,posicionx,posiciony):
    #data = obtener_data(id_solicitud)
    generar_titulo(pdf,posicionx+50,posiciony) #Título en posicion 100, 740
    #generar_infoSolicitante(pdf,data,posicionx,posiciony-60)
    #generar_infoServicios(pdf,data,posicionx,posiciony-170)
    generar_tabla(pdf,data,posicionx,posiciony-100)

def generar_titulo(pdf,xtitulo,ytitulo):
    fecha_actual = datetime.now()
    #titulo en sí -> 100,740
    pdf.setFont("Helvetica-Bold", 25)
    pdf.drawString(xtitulo, ytitulo, "ASISTENCIAS DEL DÍA")
    #id -> 100,725  
    pdf.setFont("Helvetica", 10)
    #pdf.drawString(xtitulo, ytitulo-15, f"Id-Solicitud: {formatear_id(data['id_solicitud'])}")
    #fecha -> 400, 725
    pdf.drawString(xtitulo+250, ytitulo-15, f"Fecha emision: {fecha_actual.date()}")

"""def generar_infoSolicitante(pdf,data,posix,posiy):
    # Obtener datos del solicitante
    nombre = data["solicitud"]["solicitante"]["persona"]["nombre_completo"]
    nro_documento = data["solicitud"]["solicitante"]["persona"]["ndocumento"]
    rol = data["solicitud"]["solicitante"]["rol"]["descripcion"]
    correo = data["solicitud"]["solicitante"]["correo"]
    telefono = data["solicitud"]["solicitante"]["telefono"]
    
    # Obtener datos de su predio
    predio = data["solicitud"]["predio"]["descripcion"]
    ruc = data["solicitud"]["predio"]["ruc"]
    tipo_predio = data["solicitud"]["predio"]["tipo_predio"]["nomre_predio"]

    # Combinacion
    nombreRol = nombre + "   -   "+rol
    if '\n' in nombreRol: nombreRol = nombreRol.replace('\n','') #me dieron data con saltos de linea (no pertenece a mi CUS)

    pdf.setFont("Helvetica-BoldOblique", 12)
    pdf.drawString(posix, posiy+15, "Solicitante")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(posix, posiy, "Nombre:")
    pdf.drawString(posix, posiy-20, "Nro documento:")
    pdf.drawString(posix, posiy-40, "Predio:")
    pdf.drawString(posix, posiy-60, "Tipo predio:")
    pdf.drawString(posix+200, posiy-20, "Correo:")
    pdf.drawString(posix+200, posiy-40, "Telefono:")
    pdf.drawString(posix+200, posiy-60, "R.U.C.:")
    
    pdf.drawString(posix+90, posiy, nombreRol)
    pdf.drawString(posix+90, posiy-20, nro_documento) 
    pdf.drawString(posix+90, posiy-40, predio)
    pdf.drawString(posix+90, posiy-60, tipo_predio)
    pdf.drawString(posix+270, posiy-20, correo)
    pdf.drawString(posix+270, posiy-40, str(telefono))
    pdf.drawString(posix+270, posiy-60, ruc)

def generar_infoServicios(pdf,data,posix,posiy):
    tipo_servicio = data["solicitud"]["servicio"]["descripcion"]
    cant_administradores = defaultCantidad(data["solicitud"]["cant_administracion"])
    cant_plimpieza = defaultCantidad(data["solicitud"]["cant_plimpieza"])
    cant_jardineros = defaultCantidad(data["solicitud"]["cant_jardineria"])
    cant_vigilantes = defaultCantidad(data["solicitud"]["cant_vigilantes"])

    pdf.setFont("Helvetica-BoldOblique", 12)
    pdf.drawString(posix, posiy+15, "Servicios")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(posix, posiy, "Tipo de servicio:")
    pdf.drawString(posix+90, posiy, tipo_servicio)
    
    pdf.drawString(posix, posiy-20, "Cantidad de administradores:")
    pdf.drawString(posix+150, posiy-20, str(cant_administradores))

    pdf.drawString(posix+200, posiy-20, "Cantidad de plimpieza:")
    pdf.drawString(posix+350, posiy-20, str(cant_plimpieza))

    pdf.drawString(posix, posiy-40, "Cantidad de jardineros:")
    pdf.drawString(posix+150, posiy-40, str(cant_jardineros))

    pdf.drawString(posix+200, posiy-40, "Cantidad de vigilantes:")
    pdf.drawString(posix+350, posiy-40, str(cant_vigilantes))"""


#generar tabla del body
def generar_tabla(pdf,data,posix,posiy):
    ids = [tupla[0] for tupla in data]
    ubis = [tupla[1] for tupla in data]
    lats = [tupla[2] for tupla in data]
    longs = [tupla[3] for tupla in data]

    # Construye la estructura de datos para la tabla
    table_data = [
        ['ID','UBICACIÓN','LATITUD','LONGITUD'],  # Nombres de las columnas
    ]

    for tupla in data:
        id,ubi,lat,long = tupla
        table_data.append([id,ubi,lat,long])

    color_azul = ((4/255, 26/255, 47/255))
    color_azulclaro = ((215/255, 235/255, 255/255))
    table = Table(table_data, colWidths=100, rowHeights=30)
    estilo_tabla = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), color_azul),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ])
    # Alternar colores de fondo para filas
    for i in range(1, len(table_data)):
        if i % 2 == 0 and i!=0:
            estilo_tabla.add('BACKGROUND', (0, i), (-1, i), colors.white)
        else:
            estilo_tabla.add('BACKGROUND', (0, i), (-1, i), color_azulclaro)
    
    table.setStyle(estilo_tabla)
    table.wrapOn(pdf, 400, 500)
    pdf.setFont("Helvetica-BoldOblique", 12)
    pdf.drawString(posix+100, posiy+5, "LISTA ASISTENCIAS")
    table.drawOn(pdf, posix+100, posiy-table._height-5)

# FOOTER
def dibujar_footer(pdf,x_footer,y_footer):
    pdf.setFont("Helvetica-Bold", 10)
    # Definir las coordenadas para el footer y la línea
    x_linea = x_footer  # posición x de la línea
    y_linea = y_footer + 20  # posición y de la línea (ajusta la separación)
    # Dibujar una línea negra encima del footer
    pdf.setLineWidth(5)  # Establecer el ancho de línea
    pdf.setStrokeColorRGB(4/255, 26/255, 47/255)  
    pdf.line(x_linea, y_linea, pdf._pagesize[0] - x_linea, y_linea)  # dibujar línea horizontal
    # Agregar texto al lienzo
    pdf.drawString(x_footer, y_footer, "\u00A9 2023 FISI. Todos los derechos reservados.")