from validador_nfe_lexer import lexer
import sys
import datetime
import re # valida cnpj

tags_validadas = {}

class ValidadorNFeParser:
    def __init__(self):
        self.lookahead = None
        self.errors = []

    def match(self, token_type):
        if self.lookahead and self.lookahead.type == token_type:
            self.lookahead = lexer.token()
        else:
            erro_msg = f"Erro de sintaxe na linha {self.lookahead.lineno if self.lookahead else 'desconhecida'}: Esperado '{token_type}', encontrado '{self.lookahead.type if self.lookahead else 'Fim do Arquivo'}'"
            if not self.errors or self.errors[-1] != erro_msg:
                self.errors.append(erro_msg)
            if self.lookahead:
                 self.lookahead = lexer.token()

    #FUNÇÕES DE VALIDAÇÃO SEMÂNTICA
    def validar_cnpj(self, valor, linha, nome_tag):
        if not re.match(r'^\d{14}$', valor):
            self.errors.append(f"Erro semântico na linha {linha}: Tag '{nome_tag}' deve ser um CNPJ com 14 dígitos. Valor: '{valor}'")
        else:
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")
            
    def validar_uf(self, valor, linha, nome_tag):
        ufs_validas = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
        if valor not in ufs_validas:
             self.errors.append(f"Erro semântico na linha {linha}: Tag '{nome_tag}' não é uma UF válida. Valor: '{valor}'")
        else:
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")

    def validar_numerico_simples(self, valor, linha, nome_tag):
        if not valor.isdigit():
            self.errors.append(f"Erro semântico na linha {linha}: Tag '{nome_tag}' deve ser numérica. Valor: '{valor}'")
        else:
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")

    def validar_float_simples(self, valor, linha, nome_tag):
        try:
            float(valor)
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")
        except ValueError:
            self.errors.append(f"Erro semântico na linha {linha}: Tag '{nome_tag}' deve ser um valor numérico (float). Valor: '{valor}'")
    
    def validar_cst(self, valor, linha, nome_tag):
        if not valor.isdigit() or len(valor) != 2:
            self.errors.append(f"Erro semântico na linha {linha}: Tag '{nome_tag}' do imposto deve ter 2 dígitos. Valor: '{valor}'")
        else:
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")

    def validar_cuf(self, valor, linha, nome_tag):
        if not valor.isdigit() or len(valor) != 2:
            self.errors.append(f"Erro semântico na linha {linha}: O '{nome_tag}' deve ter 2 dígitos numéricos. Valor: '{valor}'")
        else:
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")
            
    def validar_natOp(self, valor, linha, nome_tag):
        if len(valor) > 60:
            self.errors.append(f"Erro semântico na linha {linha}: '{nome_tag}' deve ter no máximo 60 caracteres. Valor: '{valor}'")
        else:
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")
    
    def validar_mod(self, valor, linha, nome_tag):
        if not valor.isdigit() or len(valor) != 2:
            self.errors.append(f"Erro semântico na linha {linha}: '{nome_tag}' deve ter 2 dígitos numéricos. Valor: '{valor}'")
        else:
            print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")

    def validar_dhEmi(self, valor, linha, nome_tag):
        # Aceita o formato com ou sem fuso horário
        formatos_aceitos = ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%z']
        validado = False
        for fmt in formatos_aceitos:
            try:
                # Remove o ':' do fuso horário para compatibilidade com %z em algumas versões
                if fmt.endswith('%z') and valor[-3] == ':':
                    valor_ajustado = valor[:-3] + valor[-2:]
                    datetime.datetime.strptime(valor_ajustado, fmt)
                else:
                    datetime.datetime.strptime(valor, fmt)
                
                print(f"[OK] Tag '{nome_tag}' com valor '{valor}' validada.")
                validado = True
                break
            except ValueError:
                continue
        if not validado:
            self.errors.append(f"Erro semântico na linha {linha}: '{nome_tag}' está no formato de data/hora incorreto. Valor: '{valor}'")

    def validar_versao_infNFe(self, valor, linha):
        if valor != "4.00":
            self.errors.append(f"Erro semântico na linha {linha}: Atributo 'versao' da tag <infNFe> deve ser '4.00'. Valor: '{valor}'")
        else:
            print(f"[OK] Atributo 'versao' com valor '{valor}' validado.")
    
    def validar_nItem(self, valor, linha):
        if not valor.isdigit():
             self.errors.append(f"Erro semântico na linha {linha}: Atributo 'nItem' da tag <det> deve ser numérico. Valor: '{valor}'")
        else:
            print(f"[OK] Atributo 'nItem' com valor '{valor}' validado.")
    
    def validar_texto_simples(self, valor, linha, nome_tag):
        pass
    
    # ANÁLISE SINTÁTICA
    def parse(self, data):
        lexer.input(data)
        self.lookahead = lexer.token()
        self.nfe()
        if not self.errors:
            print("\nAnálise concluída com sucesso! Nenhuma inconsistência encontrada.")
        else:
            print("\n--- Análise concluída com erros: ---")
            for e in self.errors:
                print(f"- {e}")
        return not self.errors

    def nfe(self):
        if self.lookahead and self.lookahead.value == '<NFe':
            self.match('TAG_ABERTURA_COM_NOME') 
            self.parse_atributos('NFe', {}) 
            self.match('MAIOR_QUE')
            self.infNFe()
            self.signature()
            self.match('TAG_FECHAMENTO') 
        else:
            self.errors.append("Erro: O arquivo não parece ser uma NF-e (tag <NFe> não encontrada no início).")

    def infNFe(self):
        if self.lookahead and self.lookahead.value == '<infNFe':
            self.match('TAG_ABERTURA_COM_NOME')
            self.parse_atributos(nome_tag_pai='infNFe', mapa_validacao={'versao': self.validar_versao_infNFe})
            self.match('MAIOR_QUE')
            self.conteudo_infNFe()
            self.match('TAG_FECHAMENTO')

    def conteudo_infNFe(self):
        # Ordem simplificada para validação: ide, emit, det*, total
        if self.lookahead and self.lookahead.value == '<ide':
            self.ide()
        if self.lookahead and self.lookahead.value == '<emit':
            self.emit()
        
        while self.lookahead and self.lookahead.value == '<det':
            self.det()

        if self.lookahead and self.lookahead.value == '<total':
            self.total()
        
        while self.lookahead and self.lookahead.value != '</infNFe>':
            if self.lookahead is None: break
            self.errors.append(f"Aviso: Tag {self.lookahead.value} não está sendo validada dentro de <infNFe>.")
            self.pular_bloco_desconhecido(self.lookahead.value[1:])


    def ide(self):
        self.parse_bloco_com_tags('ide', {
            'cUF': self.validar_cuf, 'natOp': self.validar_natOp, 'mod': self.validar_mod, 
            'serie': self.validar_numerico_simples, 'nNF': self.validar_numerico_simples, 'dhEmi': self.validar_dhEmi
        })

    def emit(self):
        if self.lookahead and self.lookahead.value == '<emit':
            self.match('TAG_ABERTURA_COM_NOME')
            self.match('MAIOR_QUE')
            self.parse_tag_simples('CNPJ', self.validar_cnpj)
            self.parse_tag_simples('xNome', self.validar_texto_simples)
            self.enderEmit()
            while self.lookahead and self.lookahead.value != '</emit>':
                self.pular_bloco_desconhecido(self.lookahead.value[1:])

            self.match('TAG_FECHAMENTO')

    def enderEmit(self):
        self.parse_bloco_com_tags('enderEmit', {'xLgr': self.validar_texto_simples, 'UF': self.validar_uf})

    def det(self):
        if self.lookahead and self.lookahead.value == '<det':
            self.match('TAG_ABERTURA_COM_NOME')
            self.parse_atributos(nome_tag_pai='det', mapa_validacao={'nItem': self.validar_nItem})
            self.match('MAIOR_QUE')
            self.prod()
            self.imposto()
            self.match('TAG_FECHAMENTO')

    def prod(self):
        self.parse_bloco_com_tags('prod', {
            'cProd': self.validar_texto_simples, 'xProd': self.validar_texto_simples, 'vProd': self.validar_float_simples
        })

    def imposto(self):
        if self.lookahead and self.lookahead.value == '<imposto':
            self.match('TAG_ABERTURA_COM_NOME')
            self.match('MAIOR_QUE')
            self.icms()
            self.pis()
            while self.lookahead and self.lookahead.value != '</imposto>':
                self.pular_bloco_desconhecido(self.lookahead.value[1:])

            self.match('TAG_FECHAMENTO')

    def icms(self):
        if self.lookahead and self.lookahead.value == '<ICMS':
            self.match('TAG_ABERTURA_COM_NOME')
            self.match('MAIOR_QUE')
            if self.lookahead and self.lookahead.value == '<ICMS00':
                self.icms00()
            self.match('TAG_FECHAMENTO')

    def icms00(self):
        self.parse_bloco_com_tags('ICMS00', {'CST': self.validar_cst, 'vBC': self.validar_float_simples, 'vICMS': self.validar_float_simples})

    def pis(self):
        if self.lookahead and self.lookahead.value == '<PIS':
            self.match('TAG_ABERTURA_COM_NOME')
            self.match('MAIOR_QUE')
            self.pisAliq()
            self.match('TAG_FECHAMENTO')

    def pisAliq(self):
        self.parse_bloco_com_tags('PISAliq', {'CST': self.validar_cst, 'vBC': self.validar_float_simples, 'vPIS': self.validar_float_simples})
        
    def total(self):
        if self.lookahead and self.lookahead.value == '<total':
            self.match('TAG_ABERTURA_COM_NOME')
            self.match('MAIOR_QUE')
            self.icmsTot()
            self.match('TAG_FECHAMENTO')

    def icmsTot(self):
        self.parse_bloco_com_tags('ICMSTot', {'vProd': self.validar_float_simples, 'vNF': self.validar_float_simples})

    def signature(self):
        if self.lookahead and self.lookahead.value == '<Signature':
            print("[INFO] Bloco de Assinatura encontrado, pulando...")
            self.pular_bloco_desconhecido('Signature')
        
    def parse_bloco_com_tags(self, nome_bloco, mapa_validacao):
        if self.lookahead and self.lookahead.value == f'<{nome_bloco}':
            self.match('TAG_ABERTURA_COM_NOME')
            self.match('MAIOR_QUE')
            while self.lookahead and self.lookahead.value != f'</{nome_bloco}>':
                nome_tag = self.lookahead.value[1:]
                if nome_tag in mapa_validacao:
                    self.parse_tag_simples(nome_tag, mapa_validacao[nome_tag])
                else:
                    self.pular_bloco_desconhecido(nome_tag)
            self.match('TAG_FECHAMENTO')

    def parse_tag_simples(self, nome_tag, funcao_validacao):
        linha_atual = self.lookahead.lineno
        self.match('TAG_ABERTURA_COM_NOME')
        self.match('MAIOR_QUE')
        valor_tag = ''
        if self.lookahead and self.lookahead.type == 'CONTEUDO':
            valor_tag = self.lookahead.value
            self.match('CONTEUDO')
        funcao_validacao(valor_tag, linha_atual, nome_tag)
        tag_fechamento_esperada = f'</{nome_tag}>'
        if self.lookahead and self.lookahead.value == tag_fechamento_esperada:
            self.match('TAG_FECHAMENTO')
        else:
             self.errors.append(f"Erro de sintaxe na linha {self.lookahead.lineno if self.lookahead else 'desconhecida'}: Esperada tag de fechamento '{tag_fechamento_esperada}'")

    def parse_atributos(self, nome_tag_pai, mapa_validacao):
        while self.lookahead and self.lookahead.type == 'IDENTIFICADOR':
            nome_atributo = self.lookahead.value
            linha_atual = self.lookahead.lineno
            self.match('IDENTIFICADOR')
            self.match('IGUAL')
            valor_atributo = self.lookahead.value
            self.match('VALOR_ATRIBUTO')
            if nome_atributo in mapa_validacao:
                mapa_validacao[nome_atributo](valor_atributo, linha_atual)
            else:
                print(f"[INFO] Atributo '{nome_atributo}' na tag <{nome_tag_pai}> ignorado (não validado).")

    def pular_bloco_desconhecido(self, nome_tag):
        # Avança o lexer até encontrar a tag de fechamento correspondente
        tag_fechamento_esperada = f'</{nome_tag}>'
        nivel = 1
        self.match('TAG_ABERTURA_COM_NOME')
        while nivel > 0 and self.lookahead:
            if self.lookahead.type == 'TAG_ABERTURA_COM_NOME':
                # Verifica se é uma tag com o mesmo nome para tratar aninhamento
                if self.lookahead.value == f'<{nome_tag}':
                    nivel += 1
            elif self.lookahead.type == 'TAG_FECHAMENTO':
                if self.lookahead.value == tag_fechamento_esperada:
                    nivel -= 1
            
            if nivel == 0:
                break
            self.lookahead = lexer.token()
        
        if self.lookahead and self.lookahead.value == tag_fechamento_esperada:
             self.match('TAG_FECHAMENTO')