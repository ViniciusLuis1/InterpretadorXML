# Validador de NF-e em Python

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Um analisador léxico, sintático e semântico construído em Python para validar a estrutura e o conteúdo de arquivos XML de Notas Fiscais Eletrônicas (NF-e) do Brasil. Este projeto foi desenvolvido como trabalho final para a disciplina de Compiladores.

---

## Funcionalidades Principais

-   **Análise Léxica com Estados:** Utiliza um lexer com estados para diferenciar de forma robusta o conteúdo das tags e seus atributos.
-   **Análise Sintática Hierárquica:** Emprega um parser de descida recursiva para validar a estrutura aninhada do XML, incluindo blocos repetidos como a lista de produtos.
-   **Análise Semântica Detalhada:** Aplica regras de negócio para validar o conteúdo dos campos, como:
    -   Formatos de data e hora (`dhEmi`)
    -   Tipos de dados (numérico, texto, float)
    -   Valores específicos (ex: `versao="4.00"`)
    -   Comprimento e formato de campos (CNPJ, UF, códigos)
-   **Relatório de Erros:** Gera uma lista clara e detalhada de todos os erros sintáticos ou semânticos encontrados no arquivo.

## Tecnologias Utilizadas

-   **Python 3:** Linguagem principal do projeto.
-   **PLY (Python Lex-Yacc):** Biblioteca utilizada para a construção do analisador léxico.

## Como Usar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd NOME-DO-REPOSITORIO
    ```

3.  **Instale as dependências:**
    ```bash
    pip install ply
    ```

4.  **Execute o analisador:**
    Passe o caminho do arquivo XML que você deseja validar como argumento.

    ```bash
    # Exemplo com um arquivo válido
    python main.py nfe_final_valido.xml

    # Exemplo com um arquivo inválido
    python main.py nfe_final_semantica_invalida.xml
    ```

## Exemplo de Saída (Erro Semântico)

```bash
--- Análise concluída com erros: ---
- Erro semântico na linha 1: Atributo 'versao' da tag <infNFe> deve ser '4.00'. Valor: '5.00'
- Erro semântico na linha 1: Tag 'serie' deve ser numérica. Valor: '1A'
- Erro semântico na linha 1: 'dhEmi' está no formato de data/hora incorreto. Valor: '2018/05/28'
- Erro semântico na linha 1: Tag 'CNPJ' deve ser um CNPJ com 14 dígitos. Valor: '0818716800016'
- Erro semântico na linha 1: Tag 'UF' não é uma UF válida. Valor: 'XX'
- Erro semântico na linha 1: Tag 'vProd' deve ser um valor numérico (float). Valor: '0,01'
- Erro semântico na linha 1: Tag 'CST' do imposto deve ter 2 dígitos. Valor: '0'
- Erro semântico na linha 1: Tag 'vPIS' deve ser um valor numérico (float). Valor: 'zero'
- Erro semântico na linha 1: Tag 'vNF' deve ser um valor numérico (float). Valor: 'zerovirgulaum'
```

## Autor

* **Vinícius Luis de Oliveira Pereira** - [SEU-USUARIO-DO-GITHUB](https://github.com/SEU-USUARIO-DO-GITHUB)