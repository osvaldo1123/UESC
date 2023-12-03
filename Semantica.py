class Interp:
    def __init__(self):
        # Inicializa a pilha com uma tabela de simbolos vazia (escopo global)
        self.stack = [{}]

    def enter_escopo(self):
        # Adiciona uma nova tabela de simbolos vazia para um escopo novo
        self.stack.append({})

    def exit_escopo(self):
        # Remove a tabela de simbolos atual quando fecha um escopo
        self.stack.pop()

    def declara_variavel(self, nome, valor, tipo_dado):
        # Checa se a variavel já foi declarada no escopo atual
        if nome in self.stack[-1]:
            print(f"Erro: Variavel '{nome}' ja declarada neste escopo.")
        else:
            # Adiciona a variavel para a tabela de simbolos atual
            self.stack[-1][nome] = {'valor': valor, 'tipo': tipo_dado}

    def atribui_variavel(self, nome, valor):
        # Atualiza o valor da variavel na tabela de simbolos do escopo atual
        escopo_atual = self.stack[-1]

        # Checa se a variavel ja foi declarada nesse escopo
        if nome in escopo_atual:
            # Atualiza o valor da variavel no escopo atual
            escopo_atual[nome]['valor'] = valor
        else:
            # Checa se a variavel existe em escopos externos
            for tabela in reversed(self.stack[:-1]):
                if nome in tabela:
                    # Cria uma nova variavel com o mesmo nome dentro do escopo atual
                    escopo_atual[nome] = {'valor': valor, 'tipo': tabela[nome]['tipo']}
                    return
            # Variavel não encontrada em nenhum escopo
            print(f"Erro: Variavel '{nome}' nao declarada.")

    def print_variavel(self, nome):
        # Busca a variavel nas tabelas de simbolo (da mais interna pra mais externa)
        for tabela in reversed(self.stack):
            if nome in tabela:
                # Print do valor
                print(tabela[nome]['valor'])
                return
        print(f"Erro: Variavel '{nome}' nao declarada.")

    def infere_tipo_variavel(self, valor):
        # Infere o tipo da variavel baseado no no valor
        if isinstance(valor, int) or valor.isdigit() or (valor[0] == '-' and valor[1:].isdigit()):
            return 'tk_numero'
        elif isinstance(valor, str) and valor[0] == '"' and valor[-1] == '"':
            return 'tk_cadeia'
        else:
            return None

    def processa_declaracao_variavel(self, linha):
        # Tokeniza as linhas
        tokens = [token.strip() for token in linha.strip().split(',')]

        for i, token in enumerate(tokens):
            parts = token.split('=')

            if len(parts) == 2:
                # Infere o tipo
                variavel_nome = parts[0].strip()
                valor = parts[1].strip()

                # Checa se a variavel ja foi declarada nesse escopo
                if variavel_nome in self.stack[-1]:
                    print(f"Erro: Variavel '{variavel_nome}' ja declarada neste escopo.")
                else:
                    # Checa se o tipo da variavel é mencionado explicitamente
                    if ' ' in variavel_nome:
                        variavel_tipo, variavel_nome = variavel_nome.split(' ', 1)
                        tipo_dado = variavel_tipo
                    else:
                        # Infere o tipo caso não tenha sido declarado
                        tipo_dado = self.stack[-1].get(variavel_nome, {}).get('tipo', self.infere_tipo_variavel(valor))

                    # Declara a variavel
                    self.declara_variavel(variavel_nome, valor, tipo_dado)
            elif i > 0:
                # Token parte de uma declaração multipla na mesma linha
                prev_decl = tokens[i - 1]
                parts = f"{prev_decl},{token}".split('=')

                if len(parts) == 2:
                    variavel_nome = parts[0].strip()
                    valor = parts[1].strip()
                    tipo_dado = self.infere_tipo_variavel(valor)

                    # Declara a variavel
                    self.declara_variavel(variavel_nome, valor, tipo_dado)
                else:
                    print(f"Erro: Declaracao invalida: {token}")


# Exemplo
semantico = Interp()

# Codigo Fonte
code = """
BLOCO _principal_ 
NUMERO a = 10, b = 20 
CADEIA x

PRINT b 
PRINT a
x= "Ola mundo"
x=a 
PRINT x
BLOCO _n1_ 
CADEIA a = "Compiladores" 
NUMERO c 
c=-0.45 
PRINT b 
PRINT c 
FIM _n1_

BLOCO _n2_ 
CADEIA b = "Compiladores" 
PRINT a 
PRINT b 
a=11
CADEIA a= "Bloco2"
PRINT a 
PRINT c
BLOCO _n3_ 
NUMERO a=-0.28, c=-0.28
PRINT a 
PRINT b 
PRINT c 
d="Compiladores"
PRINT d
e=d
PRINT e
FIM _n3_ 
FIM _n2_ 
PRINT c 
PRINT a
FIM _principal_
"""

linhas = code.split('\n')

for linha in linhas:
    tokens = linha.split()
    if len(tokens) > 0:
        if tokens[0] == 'BLOCO':
            semantico.enter_escopo()
        elif tokens[0] == 'FIM':
            semantico.exit_escopo()
        elif tokens[0] == 'PRINT':
            semantico.print_variavel(tokens[1])
        elif '=' in linha:
            semantico.processa_declaracao_variavel(linha)
        elif tokens[0] not in ['NUMERO', 'CADEIA']:
            print(f"Erro: Declaracao Invalida: {linha}")
