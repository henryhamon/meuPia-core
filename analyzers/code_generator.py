from typing import Dict, List
from utils.token_enum import TokenEnum

class CodeGenerator:
    def __init__(self, lexemePairs: List[Dict[str, str]]):
        self.lexeme_pairs = lexemePairs
        self.pos = 0
        self.python_code = []
        self.indent_level = 0

    def add_line(self, line):
        indent = "  " * self.indent_level
        self.python_code.append(f"{indent}{line}")

    def current_token(self) -> str:
        if self.pos < len(self.lexeme_pairs):
        return self.lexeme_pairs[self.pos]['token']
        return TokenEnum.END_OF_FILE.name
    
    def current_lexeme(self) -> str:
        if self.pos < len(self.lexeme_pairs):
        return self.lexeme_pairs[self.pos]['lexeme']
        return ''

    def advance(self):
        self.pos += 1

    def check_token(self, expected: TokenEnum) -> bool:
        return self.current_token() == expected.name

    # --- Geração Principal ---
    def generate(self):
        # Cabeçalho com Wrappers do meuPiá
        self.add_line("# -*- coding: utf-8 -*-")
        self.add_line("import sys")
        self.add_line("from lib.meupia_libs import *") # <--- AQUI ESTÁ O SEGREDO
        self.add_line("")

        # Pular algoritmo e nome
        self.advance() # ALGORITMO
        self.advance() # NOME STRING
        
        if self.check_token(TokenEnum.VAR):
            self.gen_variables()

        self.advance() # INICIO
        
        self.add_line("def main():")
        self.indent_level += 1
        
        while not self.check_token(TokenEnum.FIMALGORITMO) and not self.check_token(TokenEnum.END_OF_FILE):
        self.gen_statement()

        self.indent_level -= 1
        self.add_line("if __name__ == '__main__':")
        self.add_line("  main()")
        
        return "\n".join(self.python_code)

    def gen_variables(self):
        self.advance() # VAR
        # Em Python não declaramos tipos explicitamente assim, mas podemos inicializar
        while self.check_token(TokenEnum.ID):
            ids = []
            ids.append(self.current_lexeme())
            self.advance()
            
            while self.check_token(TokenEnum.COMMA):
                self.advance() # ,
                ids.append(self.current_lexeme())
                self.advance() # ID
                
            self.advance() # :
            tipo = self.current_lexeme() # Inteiro, etc
            self.advance() # TIPO
            
            # Inicializa variáveis para evitar erros no Python
            val_inicial = "0" if tipo == "inteiro" else "''"
            for var_name in ids:
                self.add_line(f"{var_name} = {val_inicial}")

    def gen_statement(self):
        if self.check_token(TokenEnum.ID):
        # Verifica se é func call ou atribuição (simplificado)
        # Precisaria da mesma logica de peek do parser
        # Assumindo atribuição se tiver <- logo depois
            lexeme = self.current_lexeme()
            self.advance()
            if self.check_token(TokenEnum.ATR):
                self.advance() # <-
                expr = self.gen_expression()
                self.add_line(f"{lexeme} = {expr}")
            elif self.check_token(TokenEnum.PARAB): # Chamada de função (Wrapper)
                self.advance() # (
                args = []
                while not self.check_token(TokenEnum.PARFE):
                    args.append(self.gen_expression())
                    if self.check_token(TokenEnum.COMMA): self.advance()
                self.advance() # )
                self.add_line(f"{lexeme}({', '.join(args)})")

        elif self.check_token(TokenEnum.ESCREVA):
        self.advance()
        self.advance() # (
        expr = self.gen_expression()
        self.add_line(f"print({expr})")
        self.advance() # )
        
        elif self.check_token(TokenEnum.LEIA):
        self.advance()
        self.advance() # (
        var_name = self.current_lexeme()
        self.advance() # ID
        self.add_line(f"{var_name} = input()") # Simplificado
        self.advance() # )

        # ... Implementar SE, PARA, etc. similarmente

    def gen_expression(self):
        # Essa função deve percorrer a expressão e retornar uma string
        # Exemplo simplificado (pega tokens até achar algo que não é expressão)
        expr = ""
        while self.check_token_any_expr():
            token = self.current_token()
            lexeme = self.current_lexeme()
            if token == 'LOGIGUAL': lexeme = "=="
            elif token == 'LOGDIFF': lexeme = "!="
            elif token == 'E': lexeme = " and "
            elif token == 'OU': lexeme = " or "
            expr += lexeme
            self.advance()
        return expr

    def check_token_any_expr(self):
        # Lista de tokens validos em expressão
        return self.current_token() in ['ID', 'NUMINT', 'STRING', 'OPMAIS', 'OPMENOS', 'OPMULTI', 'OPDIVI', 'PARAB', 'PARFE', 'LOGIGUAL'] # etc...