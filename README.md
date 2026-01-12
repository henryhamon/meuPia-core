# meuPiá Core – O Compilador Modular de Portugol Inteligência Artificial

![meuPia](assets/meuPia.png)

## 📖 Overview

> **Nota:** Este projeto é um *fork* evolutivo do [`portugol-compiler`](https://www.google.com/search?q=%5Bhttps://github.com/LuanContarin/portugol-compiler%5D(https://github.com/LuanContarin/portugol-compiler)), focado em interoperabilidade e modularização.

**meuPiá Core** é o motor central do ecossistema meuPiá. Ele é um compilador (transpilador) de Portugol para Python projetado para ser **extensível**.

Diferente de ferramentas educacionais fechadas, o meuPiá permite que você instale **plugins** para expandir as capacidades da linguagem. O Core fornece a infraestrutura de análise, geração de código e o gerenciador de pacotes, enquanto as funcionalidades específicas (como IoT ou Foguetes) são instaladas sob demanda.

**meuPiá Core** fornece:

* **O Compilador:** Analisadores léxico, sintático e semântico que traduzem Portugol para Python otimizado.
* **mPGP (meuPiá Gerenciador de Pacotes):** Uma ferramenta de linha de comando integrada para instalar e gerenciar extensões oficiais.
* **Sistema de Plugins:** Suporte nativo à diretiva `usar "nome_do_plugin"`, permitindo importação dinâmica de bibliotecas.

## ⚙️ How It Works

A arquitetura foi modernizada para suportar extensões:

### 1. Analysis & Validation

O compilador realiza a análise léxica e sintática completa, garantindo a integridade lógica do algoritmo escrito em Portugol.

### 2. Plugin-Aware Code Generation

O `CodeGenerator` identifica as diretivas `usar "..."` e injeta automaticamente as dependências corretas no código Python final, otimizando os imports para o ambiente de destino (seja PC ou Microcontrolador).

### 3. Runtime Modular

O Core mantém apenas as bibliotecas essenciais. Funcionalidades complexas foram movidas para pacotes externos instaláveis via mPGP.

## 🚀 Installation

Para começar, instale o núcleo do sistema:

```bash
# Clone o repositório
git clone https://github.com/henryhamon/meuPia-core.git
cd meuPia-core

# Instale em modo editável (recomendado para dev)
pip install -e .

```

Isto instalará dois comandos no seu terminal:

* `meupia`: O compilador.
* `mpm`: O gerenciador de pacotes.

## 📦 mPGP – Gerenciador de Pacotes

O **mPGP** (meuPiá Package Manager) facilita a instalação de módulos adicionais sem que o aluno precise lidar com URLs complexas ou configurações de ambiente.

### Comandos Básicos

```bash
# Listar plugins disponíveis
mpm list

# Instalar um plugin
mpm install <nome_do_plugin>

# Remover um plugin
mpm remove <nome_do_plugin>

```

### Módulos Oficiais Disponíveis

| Módulo | Comando de Instalação | Descrição |
| --- | --- | --- |
| **Maker** | `mpm install maker` | Adiciona suporte a **IoT e Robótica**. Permite compilar Portugol para **ESP32/Pico** (MicroPython). |
| **Espacial** | `mpm install espacial` | Adiciona suporte ao **Kerbal Space Program**. Permite controlar foguetes via kRPC. |

---

## 🛠️ Usage Examples

### 1. Compilando um Algoritmo Básico

```bash
# Compila o arquivo e gera o Python equivalente na pasta output/
meupia input/ola_mundo.por

```

### 2. Usando Plugins (Ex: IoT/Maker)

Após instalar o módulo maker (`mpm install maker`), você pode utilizá-lo no seu código:

```portugol
algoritmo "PiscaLed"
usar "maker"  // <--- Carrega o plugin instalado via mPGP

var led: inteiro
inicio
    led <- 2
    iot_configurar_pino(led, "saida")
    
    enquanto verdadeiro faca
        iot_ligar(led)
        iot_esperar(1000)
        iot_desligar(led)
        iot_esperar(1000)
    fimenquanto
fimalgoritmo

```

### 3. Exemplo: Inteligência Artificial (Nativo)

O suporte básico a IA continua integrado para facilitar o ensino de lógica de dados:

```portugol
algoritmo "classificador_simples"
var dados: inteiro
inicio
    // O Core suporta vetores e matrizes nativamente
    ia_definir_dados([[150, 0], [170, 0]], [0, 0])
    ia_criar_knn(3)
    ia_treinar()
fimalgoritmo

```

## 🙌 Credits

> **meuPiá** é desenvolvido com ❤️ por **[@henryhamon](https://github.com/henryhamon)**.

Este projeto é um *hard fork* e evolução do projeto [portugol-compiler](https://github.com/LuanContarin/portugol-compiler), criado originalmente por **Luan Contarin**. A estrutura de análise léxica e sintática é mantida como a fundação sólida deste compilador.