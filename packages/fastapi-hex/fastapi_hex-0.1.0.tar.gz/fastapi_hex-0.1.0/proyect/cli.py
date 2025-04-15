import argparse
from proyect.proyect_generator import generator

def main():
    parser = argparse.ArgumentParser(description="Inicializa un proyecto FastAPI con arquitectura Hexagonal.")
    parser.add_argument("accion", choices=["init"], help="Acción que deseas realizar.")
    parser.add_argument("nombre", help="Nombre del proyecto.")
    args = parser.parse_args()

    if args.accion == "init":
        generator(args.nombre)

if __name__ == "__main__":
    main()
