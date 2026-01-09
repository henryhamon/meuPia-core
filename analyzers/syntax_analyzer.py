from typing import Dict, List

from utils.token_enum import TokenEnum

class SyntacticError(Exception):
  pass

class Parser:
  def __init__(self, lexemePairs: List[Dict[str, str]]):
    self.lexeme_pairs = lexemePairs
    self.pos = 0

  def current_token(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['token']
    
    return TokenEnum.END_OF_FILE.name
  
  def current_lexeme(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['lexeme']
    
    return ' '
  
  def current_code_index(self) -> str:
    if self.pos < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos]['code_index']

    return self.lexeme_pairs[-1].get('code_index', 'unknown')

  def peek_next_token(self) -> str:
    if self.pos + 1 < len(self.lexeme_pairs):
      return self.lexeme_pairs[self.pos + 1]['token']
    return ''

  def expect_token(self, expected: TokenEnum):
    if self.current_token() == expected.name:
      self.pos += 1
      return
    
    lexeme = self.current_lexeme()
    code_index = self.current_code_index()
    raise SyntacticError(f'Esperado "{expected.value}", encontrado "{lexeme}" na linha {code_index}')
  
  def check_token(self, expected: TokenEnum) -> bool:
    return self.current_token() == expected.name
  
  def check_token_any(self, expected: List[TokenEnum]) -> bool:
    return any(self.current_token() == t.name for t in expected)

  def parse(self):
    self.expect_token(TokenEnum.ALGORITMO)
    self.expect_token(TokenEnum.STRING)

    if self.check_token(TokenEnum.VAR):
      self.grammar_variable_block()

    self.expect_token(TokenEnum.INICIO)

    while not self.check_token_any([TokenEnum.FIMALGORITMO, TokenEnum.END_OF_FILE]):
      self.statement()

    self.expect_token(TokenEnum.FIMALGORITMO)

    if self.pos < len(self.lexeme_pairs):
      extra_lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntacticError(f'Código inesperado após "fimalgoritmo": "{extra_lexeme}" na linha {code_index}')

  def statement(self):
    # --- ALTERAÇÃO PRINCIPAL ---
    if self.check_token(TokenEnum.ID):
      # Verifica o que vem depois do ID para decidir
      next_tok = self.peek_next_token()
      
      if next_tok == TokenEnum.ATR.name:
        self.grammar_var_assignment()
      elif next_tok == TokenEnum.PARAB.name:
        self.grammar_function_call()
      else:
        # Fallback para erro ou atribuição mal formada
        self.grammar_var_assignment()

    elif self.check_token(TokenEnum.ESCREVA):
      self.grammar_command_escreva()
    elif self.check_token(TokenEnum.LEIA):
      self.grammar_command_leia()
    elif self.check_token(TokenEnum.SE):
      self.grammar_command_se()
    elif self.check_token(TokenEnum.PARA):
      self.grammar_command_para()
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntacticError(f'Token inesperado "{lexeme}" na linha {code_index}')

  # ----------------
  # Gramáticas
  # ----------------
  
  # --- NOVA GRAMÁTICA: CHAMADA DE FUNÇÃO ---
  def grammar_function_call(self):
    self.expect_token(TokenEnum.ID)     # Nome da função (ex: ia_treinar)
    self.expect_token(TokenEnum.PARAB)  # (
    
    # Se não fechar parenteses logo, temos argumentos
    if not self.check_token(TokenEnum.PARFE):
        self.grammar_arithmetic_expression() # Primeiro argumento
        
        # Enquanto houver vírgula, temos mais argumentos
        while self.check_token(TokenEnum.COMMA):
            self.expect_token(TokenEnum.COMMA)
            self.grammar_arithmetic_expression()

    self.expect_token(TokenEnum.PARFE)  # )

  def grammar_variable_block(self):
    self.expect_token(TokenEnum.VAR)

    while self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)

      # IDs opcionais separados por vírgula
      while self.check_token(TokenEnum.COMMA):
        self.expect_token(TokenEnum.COMMA)
        self.expect_token(TokenEnum.ID)

      self.expect_token(TokenEnum.COLON)
      self.expect_token(TokenEnum.TIPO)

  def grammar_var_assignment(self):
    self.expect_token(TokenEnum.ID)
    self.expect_token(TokenEnum.ATR)
    self.grammar_arithmetic_expression()

  def grammar_command_escreva(self):
    self.expect_token(TokenEnum.ESCREVA)
    self.expect_token(TokenEnum.PARAB)

    # Termos suportados por escreva
    # Nota: Poderíamos expandir aqui para aceitar expressões completas no futuro
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.STRING):
      self.expect_token(TokenEnum.STRING)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntacticError(f'Valor inesperado no comando escreva: "{lexeme}" na linha {code_index}')

    self.expect_token(TokenEnum.PARFE)

  def grammar_command_leia(self):
    self.expect_token(TokenEnum.LEIA)
    self.expect_token(TokenEnum.PARAB)

    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    else:
      lexeme = self.current_lexeme()
      code_index = self.current_code_index()
      raise SyntacticError(f'Esperado variável no comando leia, encontrado "{lexeme}" na linha {code_index}')

    self.expect_token(TokenEnum.PARFE)
  
  def grammar_command_se(self):
    self.expect_token(TokenEnum.SE)
    self.grammar_logic_expression()

    self.expect_token(TokenEnum.ENTAO)
    while not self.check_token_any([TokenEnum.SENAO, TokenEnum.FIMSE]):
      self.statement()
    
    if self.check_token(TokenEnum.SENAO):
      self.expect_token(TokenEnum.SENAO)
      while not self.check_token(TokenEnum.FIMSE):
        self.statement()

    self.expect_token(TokenEnum.FIMSE)

  def grammar_command_para(self):
    self.expect_token(TokenEnum.PARA)
    self.expect_token(TokenEnum.ID)
    self.expect_token(TokenEnum.ATE)
    self.expect_token(TokenEnum.NUMINT)

    # Passo opcional
    if self.check_token(TokenEnum.PASSO):
      self.expect_token(TokenEnum.PASSO)
      self.expect_token(TokenEnum.NUMINT)

    while not self.check_token(TokenEnum.FIMPARA):
      self.statement()

    self.expect_token(TokenEnum.FIMPARA)

  #
  # Fundamental
  #
  def grammar_arithmetic_expression(self):
    self.grammar_arithmetic_term()
    
    while self.check_token_any([TokenEnum.OPMAIS, TokenEnum.OPMENOS, TokenEnum.OPMULTI, TokenEnum.OPDIVI]):
      self.pos += 1
      self.grammar_arithmetic_term()

  def grammar_arithmetic_term(self):
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_arithmetic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      code_index = self.current_code_index()
      # Aqui entra um ponto de melhoria futuro: Suporte a listas [1,2] exigiria alteração no TokenEnum primeiro
      raise SyntacticError(f'Esperado identificador ou valor na expressão, linha {code_index}')

  def grammar_logic_expression(self):
    self.grammar_logic_comparison()
    while self.check_token_any([TokenEnum.E, TokenEnum.OU]):
      self.pos += 1
      self.grammar_logic_comparison()

  def grammar_logic_comparison(self):
    if self.check_token(TokenEnum.NAO):
      self.expect_token(TokenEnum.NAO)
      self.grammar_logic_comparison()
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_logic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      self.grammar_logic_operand()
      if self.check_token_any([
        TokenEnum.LOGIGUAL, TokenEnum.LOGDIFF,
        TokenEnum.LOGMENOR, TokenEnum.LOGMENORIGUAL,
        TokenEnum.LOGMAIOR, TokenEnum.LOGMAIORIGUAL
      ]):
        self.pos += 1
        self.grammar_logic_operand()
      else:
        code_index = self.current_code_index()
        raise SyntacticError(f'Faltando operador de comparação na linha {code_index}')

  def grammar_logic_operand(self):
    if self.check_token(TokenEnum.ID):
      self.expect_token(TokenEnum.ID)
    elif self.check_token(TokenEnum.NUMINT):
      self.expect_token(TokenEnum.NUMINT)
    elif self.check_token(TokenEnum.STRING):
      self.expect_token(TokenEnum.STRING)
    elif self.check_token(TokenEnum.PARAB):
      self.expect_token(TokenEnum.PARAB)
      self.grammar_logic_expression()
      self.expect_token(TokenEnum.PARFE)
    else:
      code_index = self.current_code_index()
      raise SyntacticError(f'Operando lógico inválido na linha {code_index}')