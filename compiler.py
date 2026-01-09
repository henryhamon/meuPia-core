import os
import analyzers.lexical_analyzer as lexical_analyzer
import analyzers.syntax_analyzer as syntax_analyzer
import analyzers.semantic_analyzer as semantic_analyzer
from analyzers.code_generator import CodeGenerator

INPUT_FILE_NAME = 'input/missao_ia.por'

def main():
  try:
    full_path = INPUT_FILE_NAME
    filename_only = os.path.basename(INPUT_FILE_NAME)

    print(f'Compilando {full_path}...')
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Arquivo {full_path} não encontrado.")

    # Lexer
    lexeme_pairs = lexical_analyzer.compile(filename_only)

    # Parser
    parser = syntax_analyzer.Parser(lexeme_pairs)
    parser.parse()
    print('✅ Syntax is valid.')

    # Semantic Analyzer
    semantic = semantic_analyzer.SemanticAnalyzer(lexeme_pairs)
    semantic.validate()
    print('✅ Semantic is valid.')

    # Code Generator (NEW)
    print('Generating Python code...')
    generator = CodeGenerator(lexeme_pairs)
    python_code = generator.generate()
    
    # Save Output
    os.makedirs('output', exist_ok=True)
    base_name = os.path.splitext(os.path.basename(INPUT_FILE_NAME))[0]
    output_path = f'output/{base_name}.py'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_code)
        
    print(f'✅ Code generated successfully at {output_path}')
    print('[COMPILED SUCCESSFULLY]')

  except Exception as e:
    print(f'[COMPILATION ERROR]:\n\t{e}')


if __name__ == "__main__":
  main()