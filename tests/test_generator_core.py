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
