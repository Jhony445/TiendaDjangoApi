from django.shortcuts import render, redirect
import requests
from datetime import datetime
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import random

def home(request):
    return render(request, 'tienda/home.html')

def libros(request):
    libros_url = 'https://localhost:7160/api/libromaterial'
    autores_url = 'https://localhost:7122/api/Autor'

    if request.method == 'POST':
        return crear_libro(request)
    else:
        try:
            response_libros = requests.get(libros_url, verify=False)
            response_libros.raise_for_status()
            libros_data = response_libros.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de la API de libros: {e}")
            libros_data = []

        try:
            response_autores = requests.get(autores_url, verify=False)
            response_autores.raise_for_status()
            autores_data = response_autores.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener datos de la API de autores: {e}")
            autores_data = []

        context = {
            'libros': libros_data,
            'autores': autores_data,
            'crear_libro_url': reverse('crear_libro'),  # Añadir esta línea
        }
        return render(request, 'tienda/libros.html', context)

def crear_libro(request):
    url = 'https://localhost:7160/api/libromaterial'

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        fechaPublicacion = request.POST.get('fechaPublicacion')
        autorLibro = request.POST.get('autorLibro')

        # Formatear la fecha a ISO 8601
        fechaPublicacion = datetime.strptime(fechaPublicacion, "%Y-%m-%dT%H:%M").isoformat() + "Z"

        data = {
            "titulo": titulo,
            "fechaPublicacion": fechaPublicacion,
            "autorLibro": autorLibro
        }

        try:
            response = requests.post(url, json=data, verify=False)
            response.raise_for_status()
            print("Libro creado exitosamente")
            return redirect('libros')
        except requests.exceptions.RequestException as e:
            print(f"Error al crear el libro: {e}")
            

    return redirect('libros')

def autores(request):
    url = 'https://localhost:7122/api/Autor'

    if request.method == 'POST':
        # Si la solicitud es POST, intenta crear un nuevo autor
        return crear_autor(request)

    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Lanzar una excepción si la solicitud no tiene éxito
        autores_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API de autores: {e}")
        autores_data = []

    context = {
        'autores': autores_data,
    }
    return render(request, 'tienda/autores.html', context)

def crear_autor(request):
    url = 'https://localhost:7122/api/Autor'

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        fechaNacimiento = request.POST.get('fechaNacimiento')

        # Formatear la fecha a ISO 8601
        fechaNacimiento = datetime.strptime(fechaNacimiento, "%Y-%m-%d").isoformat() + "Z"

        data = {
            "nombre": nombre,
            "apellido": apellido,
            "fechaNacimiento": fechaNacimiento
        }

        try:
            response = requests.post(url, data=data, verify=False)
            response.raise_for_status()  # Lanza una excepción si la solicitud no tuvo éxito
            print("Autor creado exitosamente")
            return JsonResponse({"message": "Autor creado exitosamente"}, status=201)
        except requests.exceptions.RequestException as e:
            print(f"Error al crear el autor: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    # Si no es método POST o hubo un error, redirige a la página de autores
    return JsonResponse({"error": "Método no permitido"}, status=405)

def cupones(request):
    cupones_url = 'https://localhost:7121/api/Cupones'

    if request.method == 'POST':
        cupon_code = request.POST.get('cuponCode')
        porcentaje_descuento = request.POST.get('porcentajeDescuento')
        descuento_minimo = request.POST.get('descuentoMinimo')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')

        data = {
            'cuponCode': cupon_code,
            'procentajeDescuento': porcentaje_descuento,
            'descuentoMinimo': descuento_minimo,
            'startDate': start_date,
            'endDate': end_date,
        }

        try:
            response = requests.post(cupones_url, json=data, verify=False)
            response.raise_for_status()  # Lanza una excepción si la solicitud no tuvo éxito
            return JsonResponse({'message': 'Cupón creado exitosamente'}, status=201)
        except requests.exceptions.RequestException as e:
            print(f"Error al crear el cupón: {e}")
            return JsonResponse({'error': 'Error al crear el cupón'}, status=500)

    # Si es una solicitud GET, obtener los datos de los cupones
    try:
        response = requests.get(cupones_url, verify=False)
        response.raise_for_status()  # Lanza una excepción si la solicitud no tuvo éxito
        cupones_data = response.json().get('result', [])  # Obtener el resultado de la respuesta
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API de cupones: {e}")
        cupones_data = []

    context = {
        'cupones': cupones_data,
    }
    return render(request, 'tienda/cupones.html', context)

def crear_cupon(request):
    url = 'https://localhost:7121/api/Cupones'  # URL de tu API de creación de cupones

    cupon_code = request.POST.get('cuponCode')
    porcentaje_descuento = request.POST.get('porcentajeDescuento')
    descuento_minimo = request.POST.get('descuentoMinimo')

    data = {
        'cuponCode': cupon_code,
        'procentajeDescuento': porcentaje_descuento,
        'descuentoMinimo': descuento_minimo,
    }

    try:
        response = requests.post(url, json=data, verify=False)
        response.raise_for_status()  # Lanza una excepción si la solicitud no tuvo éxito
        return JsonResponse({'message': 'Cupón creado exitosamente'}, status=201)
    except requests.exceptions.RequestException as e:
        print(f"Error al crear el cupón: {e}")
        return JsonResponse({'error': 'Error al crear el cupón'}, status=500)

def detalle_libro(request, libro_id):
    libro_url = f'https://localhost:7160/api/libromaterial/{libro_id}'
    autores_url = 'https://localhost:7122/api/Autor'
    libros_url = 'https://localhost:7160/api/libromaterial'

    try:
        response_libro = requests.post(libro_url, verify=False)
        response_libro.raise_for_status()
        libro_data = response_libro.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API de libro: {e}")
        libro_data = {}

    try:
        response_autores = requests.get(autores_url, verify=False)
        response_autores.raise_for_status()
        autores_data = response_autores.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API de autores: {e}")
        autores_data = []

    try:
        response_libros = requests.get(libros_url, verify=False)
        response_libros.raise_for_status()
        libros_data = response_libros.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener datos de la API de libros: {e}")
        libros_data = []

    # Seleccionar 5 libros aleatorios
    libros_aleatorios = random.sample(libros_data, min(len(libros_data), 5))

    context = {
        'libro': libro_data,
        'autores': autores_data,
        'libros': libros_aleatorios,
    }
    return render(request, 'tienda/detalle_libro.html', context)