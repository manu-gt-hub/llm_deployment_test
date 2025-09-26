import os
from tools.google_handler import load_data, add_row, save_dataframe

def main():
    # SECRET AREA
    secret = "empty"
    print(f"El secret antes de acceder a el es: {secret}")
    
    secret = os.getenv("SECRET_TEST")

    if secret != 'empty':
         print("✅ El secret fue cargado correctamente.")
    
    if secret == 'madness':
        print("✅ El contenido del secret fue cargado correctamente.")
        print(f"El secret despues de acceder a el es: {secret}")
    else:
        print("❌ El contenido del secret no es correcto.")

    # CSV AREA
    print("🔧 Creando DataFrame inicial...")
    df = load_dataframe()
    
    print("➕ Añadiendo nueva fila...")
    df = añadir_fila(df)

    print("💾 Guardando CSV actualizado...")
    guardar_dataframe(df)


if __name__ == "__main__":
    main()
