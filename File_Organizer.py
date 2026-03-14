# File: file_organizer.py
# Author: Arthur Fonseca
# Description: Script that automatically organizes files by extension.

"""
File Organizer
==============

A Python automation script that organizes files automatically
into folders based on their file extensions.

Features
--------
- Detects compound extensions such as .tar.gz
- Prevents overwriting duplicate files
- Automatically creates directories
- Works across multiple user folders

Version
-------
1.0
"""

import os
import shutil
from pathlib import Path
import time

# --- PASTAS PARA LIMPAR ---
pastas_para_limpar = [
    Path.home() / "Downloads",
    Path.home() / "Desktop",
    Path.home() / "Área de Trabalho",
    Path.home() / "Documents",
    Path.home() / "Documentos",
    Path.home() / "Music",
    Path.home() / "Pictures",
    Path.home() / "Videos"
]

# --- MAPEAMENTO COMPLETO ---
mapeamento = {
    # Programação e Bancos
    ".cs": "Codigo_CSharp", ".sql": "Banco_de_Dados", ".py": "Scripts_Python",
    ".js": "Scripts_JS", ".html": "Web_Dev", ".css": "Web_Dev",

    # Documentos
    ".pdf": "PDFs", ".odt": "Docs_LibreOffice", ".docx": "Docs_Word",
    ".doc": "Docs_Word", ".xlsx": "Planilhas", ".xls": "Planilhas",
    ".csv": "Planilhas", ".txt": "Textos", ".pptx": "Apresentacoes",

    # Imagens (Incluindo WebP e GIMP)
    ".png": "Imagens", ".jpg": "Imagens", ".jpeg": "Imagens",
    ".gif": "Imagens", ".webp": "Imagens", ".xcf": "Projetos_GIMP",

    # Mídia
    ".mp4": "Videos", ".mkv": "Videos", ".mp3": "Musicas", ".wav": "Musicas",

    # Compactados e Instaladores
    ".zip": "Compactados", ".rar": "Compactados", ".7z": "Compactados",
    ".tar.gz": "Compactados", ".tar": "Compactados", ".gz": "Compactados",
    ".exe": "Instaladores", ".msi": "Instaladores", ".deb": "Instaladores", ".run": "Instaladores"
}


def obter_ou_criar_pasta(diretorio_pai, nome_desejado):
    if not diretorio_pai.exists():
        diretorio_pai.mkdir(parents=True, exist_ok=True)
    for item in diretorio_pai.iterdir():
        if item.is_dir() and item.name.lower() == nome_desejado.lower():
            return item
    nova = diretorio_pai / nome_desejado
    nova.mkdir(exist_ok=True)
    return nova


def gerar_nome_unico(caminho_arquivo):
    contador = 1
    nome_base, extensao = caminho_arquivo.stem, caminho_arquivo.suffix
    diretorio = caminho_arquivo.parent
    novo = caminho_arquivo
    while novo.exists():
        novo = diretorio / f"{nome_base} ({contador}){extensao}"
        contador += 1
    return novo


def organizar():
    for pasta_atual in pastas_para_limpar:
        if not pasta_atual.exists():
            continue

        for arquivo in pasta_atual.iterdir():
            if arquivo.is_file() and arquivo.name != "File_Organizer.py":

                nome_arquivo = arquivo.name.lower()
                extensao_encontrada = None

                # 1. Checagem especial para extensões compostas
                if nome_arquivo.endswith(".tar.gz"):
                    extensao_encontrada = ".tar.gz"
                else:
                    # 2. Checagem normal
                    ext_oficial = arquivo.suffix.lower()
                    if ext_oficial in mapeamento:
                        extensao_encontrada = ext_oficial

                    # 3. Recuperação de arquivos sem ponto
                    elif ext_oficial == "":
                        for ext_chave in mapeamento.keys():
                            ext_sem_ponto = ext_chave.replace(".", "")
                            if nome_arquivo.endswith(ext_sem_ponto):
                                extensao_encontrada = ext_chave
                                break

                # SE IDENTIFICOU, MOVE
                if extensao_encontrada:
                    nome_subpasta = mapeamento[extensao_encontrada]
                    pasta_destino = obter_ou_criar_pasta(pasta_atual, nome_subpasta)

                    if arquivo.parent == pasta_destino:
                        continue

                    caminho_final = gerar_nome_unico(pasta_destino / arquivo.name)

                    try:
                        shutil.move(str(arquivo), str(caminho_final))
                        print(f"[OK] {arquivo.name} -> {nome_subpasta}")
                    except Exception as e:
                        print(f"[ERRO] {arquivo.name}: {e}")


if __name__ == "__main__":
    print(">>> FAXINEIRO LOCAL SUPREMO ATIVADO! <<<")
    while True:
        try:
            organizar()
        except Exception as e:
            print(f">>> Erro: {e}")
        time.sleep(1800)
