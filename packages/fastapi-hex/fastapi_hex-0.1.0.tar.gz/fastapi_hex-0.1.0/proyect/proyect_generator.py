import os

def generator(name):
    estructura = [
        "nginx/ssl",
        "nginx/sites",
        "microservice/app/example/domain",
        "microservice/app/example/application",
        "microservice/app/example/infrastructure",
        "microservice/app/tests"
    ]

    archivos = ["app/main.py", "README.md", ".env"]

    # Crear directorio base
    os.makedirs(name, exist_ok=True)

    # Crear subdirectorios
    for carpeta in estructura:
        os.makedirs(os.path.join(name, carpeta), exist_ok=True)

    # Crear archivos vacíos
    for archivo in archivos:
        ruta_archivo = os.path.join(name, archivo)
        with open(ruta_archivo, "w") as f:
            f.write("")  # Deja otros archivos vacíos por ahora

    print(f"Proyecto '{name}' creado con éxito.")