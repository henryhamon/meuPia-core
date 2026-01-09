import pytest
from analyzers.code_generator import CodeGenerator
from analyzers.syntax_analyzer import Parser
from analyzers.lexical_analyzer import scan_line

def compile_snippet(portugol_code):
    lines = portugol_code.split('\n')
    all_lexemes = []
    
    # Simula o Lexer
    for i, line in enumerate(lines):
        line_clean, lexemes = scan_line(line, i+1)
        all_lexemes.extend(lexemes)
        
    # Simula Parse (opcional para gerar, mas bom para garantir consistencia)
    parser = Parser(all_lexemes)
    parser.parse()
    
    # Gera Codigo
    generator = CodeGenerator(all_lexemes)
    python_code = generator.generate()
    
    return python_code

def test_gen_assignment():
    code = """algoritmo "Attrib"
    var x: inteiro
    inicio
    x <- 10
    fimalgoritmo"""
    
    output = compile_snippet(code)
    assert "x = 10" in output

def test_gen_multidimensional_array_fix():
    # Este teste verifica especificamente o bug de adjacencia ][
    code = """algoritmo "Matrix"
    var m: inteiro
    inicio
    m <- [[1, 2], [3, 4]]
    escreva(m[0][1])
    fimalgoritmo"""
    
    output = compile_snippet(code)
    assert "m = [[1, 2], [3, 4]]" in output
    assert "print(m[0][1])" in output

def test_gen_conditional():
    code = """algoritmo "Cond"
    var x: inteiro
    inicio
    se x > 0 entao
        escreva(x)
    fim_se
    fimalgoritmo"""
    
    output = compile_snippet(code)
    assert "if x>0:" in output
    assert "    print(x)" in output

def test_gen_loop_para():
    code = """algoritmo "Loop"
    var i: inteiro
    inicio
    para i de 1 ate 10 faca
        escreva(i)
    fim_para
    fimalgoritmo"""
    
    output = compile_snippet(code)
    # Range é inclusive no portugol, entao 1 ate 10 vira range(1, 10 + 1, 1)
    assert "for i in range(1, 10 + 1, 1):" in output
    assert "    print(i)" in output

def test_gen_function_call_ia():
    code = """algoritmo "IA"
    var dados: inteiro
    inicio
    ia_treinar(dados)
    fimalgoritmo"""
    
    output = compile_snippet(code)
    assert "ia_treinar(dados)" in output

def test_gen_enquanto():
    code = """algoritmo "While"
    var x: inteiro
    inicio
    enquanto x < 10 faca
        x <- x + 1
    fimenquanto
    fimalgoritmo"""
    output = compile_snippet(code)
    assert "while x<10:" in output

def test_gen_leia_typing():
    code = """algoritmo "LeiaType"
    var n: inteiro
    s: string
    inicio
    leia(n)
    leia(s)
    fimalgoritmo"""
    
    # We need to ensure var types are registered in the generator for this test
    # compile_snippet creates a new Generator each time, so it's fresh.
    output = compile_snippet(code)
    
    # Inteiro deve ser int(input())
    assert "n = int(input())" in output
    # String deve ser input()
    assert "s = input()" in output

def test_gen_boolean_logic():
    code = """algoritmo "Bool"
    var x, y, z: inteiro
    inicio
    se (x > 0) e (y < 10) ou (nao (z > 0)) entao
        escreva("Boolean")
    fim_se
    fimalgoritmo"""
    
    output = compile_snippet(code)
    # Check translation of operators
    assert "if (x>0) and (y<10) or ( not (z>0)):" in output
