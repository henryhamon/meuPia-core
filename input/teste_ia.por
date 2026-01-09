algoritmo "TesteIA"
var
    entrada, saida : inteiro
    i : inteiro
    modelo : string

inicio
    escreva("Iniciando treinamento de IA...")
    
    modelo <- "modelo_v1"
    entrada <- 10
    saida <- 20
    
    ia_definir_dados(entrada, saida)
    ia_treinar(entrada, saida)
    
    escreva("Modelo treinado: ")
    escreva(modelo)
    
    se entrada > 5 entao
        escreva("Entrada é maior que 5")
    fim_se
    
    para i de 1 ate 3 faca
        escreva("Iteração de teste")
    fim_para
    
    escreva("Altitude KSP:")
    escreva(ksp_obter_altitude())
    
fimalgoritmo
