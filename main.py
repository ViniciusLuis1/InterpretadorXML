from validador_nfe_parser import ValidadorNFeParser
import sys

def main():
    if len(sys.argv) != 2:
        print("Uso: python main.py <caminho_para_o_xml>")
        sys.exit(1)
        
    caminho_arquivo = sys.argv[1]

    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            dados_xml = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado.")
        sys.exit(1)

    print(f"--- Iniciando análise do arquivo: {caminho_arquivo} ---\n")
    
    parser = ValidadorNFeParser()
    parser.parse(dados_xml)

if __name__ == '__main__':
    main()