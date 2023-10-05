from collections import defaultdict
import sys

char_atual = ''  # Char atual sendo processado
linha = 1
coluna = 1
index = 0
token_usos = defaultdict(lambda: defaultdict(int)) #Dicionario de tokens
error_messages = []


# Le o codigo fonte
def read_codigo_fonte(file_name):
    try:
        with open(file_name, 'r') as file:
            source_code = file.read()
        return source_code
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_name}' nao encontrado.")
        exit(1)


def gettoken(source_code):
    global char_atual, linha, coluna, index

    # Aumenta linhas/coluna no caso de espaço e quebra de linha
    while char_atual and char_atual.isspace():
        if char_atual == '\n':
            linha += 1
            coluna = 1
        else:
            coluna += 1
        index += 1  # Passa para o próximo caractere
        if index < len(source_code):
            char_atual = source_code[index]
        else:
            char_atual = None

    if not char_atual:
        print("Fim de arquivo.")
        return None, None, None, None  # Retorno de fim de arquivo

    # Variaveis para construção do lexema
    lexema = char_atual
    linha_inicio = linha
    coluna_incio = coluna

    # Estados do AFD
    states = {
        "START": 0,
        "ACCEPT1": 1,
        "ACCEPT2": 2,
        "ACCEPT3": 3,
        "ACCEPT4": 4,
        "ACCEPT5": 5,
        "ACCEPT6": 6,
        "ACCEPT7": 7,
        "STATE1": 8,
        "STATE2": 9,
        "STATE3": 10,
        "STATE4": 11,
        "STATE5": 12,
        "STATE6": 13,
        "STATE7": 14,
        "STATE8": 15,
        "STATE9": 16,
        "STATE10": 17,
        "STATE11": 18,
        "STATE12": 19,
        "STATE13": 20,
        "STATE14": 21,
        "STATE15": 22,
        "STATE16": 23,
        "STATE17": 24,
        "STATE18": 25,
        "STATE19": 26,
        "STATE20": 27,
        "STATE21": 28,
        "STATE22": 29,
        "STATE23": 30,
        "STATE24": 31,
        "STATE25": 32
    }

    # Posiciona o AFD no estado inicial
    state = states["START"]
    while state != -1:
    #    print(f"Character: {char_atual}, Estado: {state}")
        if state == states["START"]:
            if char_atual == '/':
                state = states["ACCEPT1"]
            elif char_atual == '|':
                state = states["ACCEPT1"]
            elif char_atual == '&':
                state = states["ACCEPT1"]
            elif char_atual == '/':
                state = states["ACCEPT1"]
            elif char_atual == '-':
                state = states["ACCEPT1"]
            elif char_atual == '+':
                state = states["ACCEPT1"]
            elif char_atual == '*':
                state = states["ACCEPT1"]
            elif char_atual == ',':
                state = states["ACCEPT2"]
            elif char_atual == '(':
                state = states["ACCEPT3"]
            elif char_atual == ')':
                state = states["ACCEPT4"]
            elif char_atual == '>':
                state = states["ACCEPT5"]
            elif char_atual == '=':
                state = states["ACCEPT6"]
            elif char_atual == '!':
                state = states["STATE1"]
            elif char_atual == ':':
                state = states["STATE1"]
            elif char_atual.isdigit():
                state = states["STATE2"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE3"]
            elif 'G' <= char_atual <= 'Z':
                state = states["STATE4"]
            elif char_atual == '"':
                state = states["STATE5"]
            elif char_atual == '<':
                state = states["STATE6"]
            elif char_atual == '#':
                state = states["STATE7"]
            elif char_atual == '\'':
                state = states["STATE8"]
            elif char_atual.islower() and 'a' <= char_atual <= 'z':
                state = states["STATE9"]
            else:
                token_type = "TK_ERROR"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE1"]:
            if char_atual == '=':
                state = states["ACCEPT6"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Atribuicao mal feita"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE2"]:
            if char_atual.isdigit():
                state = states["STATE2"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE2"]
            elif char_atual == 'e':
                state = states["STATE10"]
            elif char_atual == '.':
                state = states["STATE11"]
            else:
                lexema = lexema[:-1]
                token_type = "TK_NUM"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE3"]:
            if char_atual.isdigit():
                state = states["STATE2"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE2"]
            elif char_atual == 'e':
                state = states["STATE10"]
            elif char_atual == '.':
                state = states["STATE11"]
            elif char_atual == '$':
                state = states["STATE12"]
            else:
                lexema = lexema[:-1]
                token_type = "TK_NUM"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE4"]:
            if char_atual == '$':
                state = states["STATE12"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Moeda mal escrita"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE5"]:
            if char_atual == '"':
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Cadeia vazia"
                return token_type, lexema, linha_inicio, coluna_incio
            else:
                state = states["STATE13"]

        elif state == states["STATE6"]:
            if char_atual == '=':
                state = states["ACCEPT6"]
            elif char_atual.islower() and 'a' <= char_atual <= 'z':
                state = states["STATE14"]
            else:
                lexema = lexema[:-1]
                token_type = "TK_OP_RELACIONAL"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE7"]:
            if char_atual == '\n':
                lexema = lexema[:-1]
                token_type = "TK_COMENT"
                return token_type, lexema, linha_inicio, coluna_incio
            else:
                state = states["STATE7"]

        elif state == states["STATE8"]:
            if char_atual == '\'':
                state = states["STATE15"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Comentario em bloco nao aberto"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE9"]:
            if char_atual.islower() and 'a' <= char_atual <= 'z' or char_atual == '_':
                state = states["STATE9"]
            else:
                if lexema[:-1] == 'programa':
                    lexema = lexema[:-1]
                    token_type = "TK_PROGRAMA"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'fim_programa':
                    lexema = lexema[:-1]
                    token_type = "TK_FIM_PROGRAMA"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'se':
                    lexema = lexema[:-1]
                    token_type = "TK_SE"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'senao':
                    lexema = lexema[:-1]
                    token_type = "TK_SENAO"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'entao':
                    lexema = lexema[:-1]
                    token_type[:-1] = "TK_ENTAO"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'imprima':
                    lexema = lexema[:-1]
                    token_type = "TK_IMPRIMA"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'leia':
                    lexema = lexema[:-1]
                    token_type = "TK_LEIA"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'leia':
                    lexema = lexema[:-1]
                    token_type = "TK_LEIA"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                elif lexema[:-1] == 'enquanto':
                    lexema = lexema[:-1]
                    token_type = "TK_ENQUANTO"
                    index -= 1
                    return token_type, lexema, linha_inicio, coluna_incio
                else:
                    token_type = "TK_ERROR"
                    index -= 1
                    lexema = "Palavra reservada nao encontrada"
                    return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE10"]:
            if char_atual == '-':
                state = states["STATE16"]
            elif char_atual.isdigit():
                state = states["STATE17"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE17"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Numero mal formado"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE11"]:
            if char_atual.isdigit():
                state = states["STATE18"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE18"]

        elif state == states["STATE12"]:
            if char_atual.isdigit():
                state = states["STATE19"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Moeda mal formatada"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE13"]:
            if char_atual == '"':
                state = states["STATE20"]
            elif char_atual == '\n':
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Cadeia com quebra de linha"
                return token_type, lexema, linha_inicio, coluna_incio
            else:
                state = states["STATE13"]

        elif state == states["STATE14"]:
            if char_atual.islower() and 'a' <= char_atual <= 'z':
                state = states["STATE14"]
            elif char_atual.isdigit():
                state = states["STATE14"]
            elif char_atual == '>':
                state = states["ACCEPT7"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Identificador mal escrito"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE15"]:
            if char_atual == '\'':
                state = states["STATE21"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Comentario em bloco nao aberto"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE16"]:
            if char_atual.isdigit():
                state = states["STATE17"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE17"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Numero mal formatado"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE17"]:
            if char_atual.isdigit():
                state = states["STATE17"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE17"]
            else:
                lexema = lexema[:-1]
                token_type = "TK_NUM"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE18"]:
            if char_atual.isdigit():
                state = states["STATE18"]
            elif 'A' <= char_atual <= 'F':
                state = states["STATE18"]
            elif char_atual == 'e':
                state = states["STATE10"]
            else:
                lexema = lexema[:-1]
                token_type = "TK_NUM"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE19"]:
            if char_atual.isdigit():
                state = states["STATE19"]
            elif char_atual == '.':
                state = states["STATE22"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Moeda mal formatada"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE20"]:
            if char_atual == '\n':
                linha += 1
            else:
                lexema = lexema[:-1]
                index -= 1
                token_type = "TK_CADEIA"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE21"]:
            if char_atual == '\'':
                state = states["STATE23"]
            else:
                state = states["STATE21"]

        elif state == states["STATE22"]:
            if char_atual.isdigit():
                state = states["STATE24"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Moeda mal formatada"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE23"]:
            if char_atual == '\'':
                state = states["STATE25"]
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Comentario em bloco nao fechado"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE24"]:
            if char_atual.isdigit():
                lexema = lexema[:-1]
                token_type = "TK_MOEDA"
                return token_type, lexema, linha_inicio, coluna_incio
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Moeda mal formatada"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["STATE25"]:
            if char_atual == '\'':
                lexema = lexema[:-1]
                token_type = "TK_COMENT"
                return token_type, lexema, linha_inicio, coluna_incio
            else:
                token_type = "TK_ERROR"
                index -= 1
                lexema = "Comentario em bloco nao fechado"
                return token_type, lexema, linha_inicio, coluna_incio

        elif state == states["ACCEPT1"]:
            token_type = "TK_OP_LOGICO"
            return token_type, lexema, linha_inicio, coluna_incio
        elif state == states["ACCEPT2"]:
            token_type = "TK_VIRGULA"
            return token_type, lexema, linha_inicio, coluna_incio
        elif state == states["ACCEPT3"]:
            lexema = lexema[:-1]
            token_type = "TK_AB_PARENT"
            index -= 1
            return token_type, lexema, linha_inicio, coluna_incio
        elif state == states["ACCEPT4"]:
            lexema = lexema[:-1]
            index -= 1
            token_type = "TK_FE_PARENT"
            return token_type, lexema, linha_inicio, coluna_incio
        elif state == states["ACCEPT5"]:
            token_type = "TK_OP_RELACIONAL"
            lexema = lexema[:-1]
            index -= 1
            return token_type, lexema, linha_inicio, coluna_incio
        elif state == states["ACCEPT6"]:
            if lexema[:-1] == ':=':
                token_type = "TK_ATRIB"
                return token_type, lexema, linha_inicio, coluna_incio
            else:
                token_type = "TK_OP_RELACIONAL"
                return token_type, lexema, linha_inicio, coluna_incio
        elif state == states["ACCEPT7"]:
            lexema = lexema[:-1]
            index -= 1
            token_type = "TK_IDENT"
            return token_type, lexema, linha_inicio, coluna_incio

        if index == len(source_code): #AFD chegou ao final do arquivo dentro de um comentário em bloco
            if state in [states["STATE8"], states["STATE15"], states["STATE21"], states["STATE23"], states["STATE25"]]:
                token_type = "TK_ERROR"
                lexema = "Comentario em bloco nao fechado"
                return token_type, lexema, linha_inicio, coluna_incio

        if index < len(source_code):
            index += 1
            if index < len(source_code):
                char_atual = source_code[index]
                lexema += char_atual
            coluna += 1


#Conta a frequência de aparição de tokens no código fonte e salva separadamente
def get_token_usos(tokens):
    token_usos = {}
    for token in tokens:
        token_type = token["Token Type"]
        lexema = token["lexema"]

        if token_type not in token_usos:
            token_usos[token_type] = {"usos": 1, "lexemas": {lexema}}
        else:
            token_usos[token_type]["usos"] += 1
            token_usos[token_type]["lexemas"].add(lexema)

    return token_usos


def print_token_usos(token_usos):
    with open("token_tabela_usos.txt", "w") as token_usos_file:
        sys.stdout = token_usos_file

        print("TOKEN".ljust(25) + "|" + "USOS".rjust(15))
        print("-" * 40)

        total_tokens = 0

        # Sort the token frequencies
        usos_ordenados = sorted(token_usos.items(), key=lambda x: x[1]["usos"], reverse=True)

        for token_type, info in usos_ordenados[:-1]:
            if token_type != "TK_ERROR":  # Pula os erros
                usos = info["usos"]
                token_type = token_type.ljust(25)  # Alinha as colunas
                uses = str(usos).rjust(15)
                total_tokens += usos
                print(token_type + "|" + uses)

        print("-" * 40)
        print(f"TOTAL TOKENS:".ljust(25) + "|" + str(total_tokens).rjust(15))
    sys.stdout = sys.__stdout__


def print_token_tabela(tokens):
    with open("token_tabela_lista.txt", "w") as token_lista_file:
        sys.stdout = token_lista_file

        print("LINHA".ljust(10) + "|" + "COLUNA".ljust(10) + "|" + "TOKEN".ljust(25) + "|" + "LEXEMA")
        print("-" * 80)

        for token in tokens[:-1]:
            if token["Token Type"] != "TK_ERROR":  # Pula os erros
                linha = token["Linha inicial"]
                coluna = token["Coluna inicial"]
                token_type = token["Token Type"].ljust(25)
                lexema = token["lexema"]
                print(f"{linha}".ljust(10) + "|" + f"{coluna}".ljust(10) + "|" + f"{token_type}" + "|" + lexema)


def main():
    global char_atual, linha, index
    # Abre o arquivo
    source_code = read_codigo_fonte('ex2.cic')
    # Inicializa a leitura de caracteres
    char_atual = source_code[index]

    # Lista para salvar as tokens
    tokens = []

    # Loop para passar pelo codigo fonte caractere a caractere
    while index < len(source_code):
        token_result = gettoken(source_code)

        token_type, lexema, linha_inicio, coluna_incio = token_result

        # Adiciona a token retornada a lista
        tokens.append({
            "Token Type": token_type,
            "lexema": lexema,
            "Linha inicial": linha_inicio,
            "Coluna inicial": coluna_incio
        })

        if token_type == "TK_ERROR":
            error_messages.append({
                "mensagem": f"Erro lexico na linha {linha_inicio} coluna {coluna_incio}: {lexema}",
                "linha": linha_inicio,
                "coluna": coluna_incio})

        index += 1  # Avança para o próximo caracter

        if index < len(source_code):
            char_atual = source_code[index]  # Update char_atual

    with open("erros_saida.txt", "w") as erros_file:
        sys.stdout = erros_file
        linhas = source_code.split('\n')
        for erro in error_messages:
            erro_linha = erro["linha"]
            erro_mensagem = erro["mensagem"]

            if erro_linha > 0 and erro_linha <= len(linhas):
                linha = linhas[erro_linha]  # Vai para a linha para a linha onde está o erro
                print(f"[{erro_linha}] {linha}")
                print(" " * (erro_linha) + " " * erro["coluna"] + "^")
                print(erro_mensagem)
            else:
                print(erro_mensagem)

    sys.stdout = sys.__stdout__

    token_usos = get_token_usos(tokens)
    print_token_usos(token_usos)
    print_token_tabela(tokens)


if __name__ == "__main__":
    main()