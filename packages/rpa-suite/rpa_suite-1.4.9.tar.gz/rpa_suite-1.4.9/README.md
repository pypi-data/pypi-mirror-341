![RPA Suite](https://raw.githubusercontent.com/CamiloCCarvalho/rpa_suite/db6977ef087b1d8c6d1053c6e0bafab6b690ac61/logo-rpa-suite.svg)

<h1 align="left">
    RPA Suite
</h1>
<br>

![PyPI Latest Release](https://img.shields.io/pypi/v/rpa-suite.svg)
![PyPI Downloads](https://img.shields.io/pypi/dm/rpa-suite.svg?label=PyPI%20downloads)

---

## O que é?

**RPA Suite:** um conjunto abrangente de ferramentas projetadas para simplificar e otimizar o desenvolvimento de projetos de automação RPA com Python. Embora nossa suíte seja um conjunto de Ferramentas de RPA especializado, sua versatilidade a torna igualmente útil para uma ampla gama de projetos de desenvolvimento. Esta desenvolvendo com Selenium, Botcity ou Playwright? Experimente a RPA Suite e descubra como podemos facilitar seu projeto, ou qualquer projeto de Robôs de Software.

## Sumário do conteudo

- [O que é?](#o-que-é)
- [Sumário do conteudo](#sumário-do-conteudo)
- [Destaque](#destaque)
- [Objetivo](#objetivo)
- [Instalação](#instalação)
- [Exemplo](#exemplo)
- [Dependências](#dependências)
- [Estrutura do módulo](#estrutura-do-módulo)
- [Release](#release)
  - [Notas da atualização: 1.4.9](#notas-da-atualização-149)
- [Mais Sobre](#mais-sobre)

## Destaque

**Versátil**: Além da Automação de Processos e criação de BOT em RPA, mas também para uso geral podendo  ser aplicadas em outros modelos de projeto, *além do RPA*.

**Simples**: Construímos as ferramentas de maneira mais direta e assertiva possível, utilizando apenas bibliotecas conhecidas no mercado para garantir o melhor desempenho possível.

## Objetivo

Nosso objetivo é se tornar a Biblioteca Python para RPA referência. Tornando o desenvolvimento de RPAs mais produtivo, oferecendo uma gama de funções para tal:

- Envio de emails (já configurado e personalizavel)
- Validação de emails (limpeza e tratamento)
- Busca por palavras, strings ou substrings (patterns) em textos.
- Criação e deleção de pasta/arquivo temporário com um comando
- Console com mensagens de melhor visualização com cores definidas para alerta, erro, informativo e sucesso.
- E muito mais

## Instalação

Para **instalar** o projeto, utilize o comando:

```python
>>> python -m pip install rpa-suite
```

ou no conda:

```python
conda install -c conda-forge rpa-suite
```

Após instalação basta fazer a importação do modulo rpa que ja tera um objeto instanciado de ``suite``:

```python
from rpa_suite import rpa
```

Feito isso já estará pronto para o uso:

```python
# function send mail by SMTP 
rpa.email.send_mail(...)
```

> [!NOTE]
>
> Para **desinstalar** o projeto, utilize o comando abaixo.
> **Obs.:** como usamos algumas libs no projeto, lembre-se de desinstar elas caso necessário.

```python
>>> python -m pip uninstall rpa-suite
```

> [!IMPORTANT]
>
> Opcionalmente você pode querer desinstalar as libs que foram inclusas no projeto, sendo assim:

```python
>>> python -m pip uninstall loguru mail_validator colorama pillow pyautogui
```

## Exemplo

Do módulo principal, importe a suite. Ela retorna uma instância do Objeto de classe Rpa_suite, onde possui variáveis apontando para todas funções dos submódulos:

    from rpa_suite import rpa

    # Exemplo com função de execução em horario especifico
    rpa.clock.exec_at_hour('13:53', my_function, param_a, param_b)

    # Usando submódulo clock para aguardar 30(seg) para executar minha função
    time = 30
    rpa.clock.wait_for_exec(time, my_function, param1, param2)

    # Usando submódulo email para envio de email por smtp comum
    rpa.email.send_smtp(...)

## Dependências

No setup do nosso projeto já estão inclusas as dependências, só será necessário instalar nossa **Lib**, mas segue a lista das libs usadas:

- colorama
- loguru
- email-validator
- colorlog
- pillow
- pyautogui
- typing
- setuptools

  opcionalmente para automação de navegador:

  - selenium
  - webdriver_manager

[!IMPORTANT]
No caso da função de screenshot é necessario ter as libs 'pyautogui' 'pillow' e 'pyscreeze' instalados, geralmente a instalação de pyautogui já instala as demais dependências deste caso.

## Estrutura do módulo

O módulo principal do rpa-suite é dividido em categorias. Cada categoria contém módulos com funções destinadas a categoria:

- **rpa_suite**
  
  - **clock**
    - **exec_at_hour** - Função que executa uma função no horário especificado "xx:yy", permitindo agendamento de tarefas com precisão.
    - **wait_for_exec** - Função que aguarda um tempo em segundos antes de executar a função passada como argumento.
    - **exec_and_wait** - Função que executa uma função e, em seguida, aguarda um tempo em segundos antes de continuar.
  
  - **date**
    - **get_hms** - Função que retorna hora, minuto e segundo formatados como strings.
    - **get_dmy** - Função que retorna dia, mês e ano formatados como strings.
  
  - **email**
    - **send_smtp** - Função para envio de emails via SMTP com suporte a anexos e mensagens HTML, configurável e personalizável.

  - **file**
    - **screen_shot** - Função para capturar screenshots, criando diretórios e arquivos com nomes e caminhos personalizáveis.
    - **flag_create** - Função para criar arquivos de flag indicando execução de processos.
    - **flag_delete** - Função para deletar arquivos de flag após a execução de processos.
    - **count_files** - Função para contar arquivos em diretórios, com suporte a extensões específicas.

  - **directory**
    - **create_temp_dir** - Função para criar diretórios temporários com nomes e caminhos personalizáveis.
    - **delete_temp_dir** - Função para deletar diretórios temporários, com opção de remover arquivos contidos.

  - **log**
    - **config_logger** - Função para configurar logs com suporte a arquivos e streams, utilizando a biblioteca Loguru.
    - **log_start_run_debug** - Função para registrar logs de início de execução em nível de depuração.
    - **log_debug** - Função para registrar logs em nível de depuração.
    - **log_info** - Função para registrar logs em nível informativo.
    - **log_warning** - Função para registrar logs em nível de aviso.
    - **log_error** - Função para registrar logs em nível de erro.
    - **log_critical** - Função para registrar logs em nível crítico.

  - **printer**
    - **success_print** - Função para imprimir mensagens de sucesso com destaque em verde.
    - **alert_print** - Função para imprimir mensagens de alerta com destaque em amarelo.
    - **info_print** - Função para imprimir mensagens informativas com destaque em ciano.
    - **error_print** - Função para imprimir mensagens de erro com destaque em vermelho.
  - **regex**
    - **check_pattern_in_text** - Função para verificar a presença de padrões em textos, com suporte a case-sensitive.
  
  - **validate**
    - **emails** - Função para validar listas de emails, retornando listas de emails válidos e inválidos.
    - **word** - Função para buscar palavras ou padrões específicos em textos, com suporte a contagem de ocorrências.
  
  - **browser**
    - **start_browser** - Função para iniciar o navegador Chrome com suporte a depuração remota.
    - **find_ele** - Função para localizar elementos na página utilizando estratégias de localização do Selenium.
    - **get** - Função para navegar para URLs específicas.
    - **close_browser** - Função para fechar o navegador e encerrar processos relacionados.

  - **parallel**
    - **run** - Função para iniciar um processo em paralelo.
    - **is_running** - Função para capturar o status atual do processo que esta rodando em paralelo.
    - **get_result** - Função para coletar o retorno da execução em paralelo junto com resultado da função ou funções que foram enviadas a este processo com retorno em forma de dict.
    - **terminate** - Função para finalizar o processo paralelo mantendo apenas o processo principal do seu código, também é chamada de forma automatica esta função ao final de um procesos paralelo ou no final da função "get_result".

  - **async**
    - **run** - Função para iniciar a execução assíncrona de uma função mantendo o fluxo principal da aplicação.
    - **is_running** - Função para verificar se a tarefa assíncrona ainda está em execução.
    - **get_result** - Função para obter o resultado da execução assíncrona, incluindo tempo de execução e status, com suporte a timeout.
    - **cancel** - Função para cancelar a tarefa assíncrona em execução.

## Release

Versão: **Beta 1.4.9**

Lançamento: *20/02/2024*

Última atualização: *12/04/2025*

Status: Em desenvolvimento.

### Notas da atualização: 1.4.9

- Mudança dos submodulos para Objetos, agora Rpa_suite é um Objeto de Suite que compoe diversos sub-objetos separados pelas mesmas categorias anteriormente ja definidas
- Reformulada a arquitetura do projeto para melhor coeção e menos subpastas e arquivos, agora a estrutura é mais simples e de melhor manutenção contendo apenas uma pasta core para o nucleo de nossos modulos, e uma pasta utils com ferramentas utilitarias que vamos adicionar varias novidades
- Adicionado SubModulo Parallel com função dedicada a rodar um processo em paralelo com seu fluxo principal podendo recuperar o resultado da execução em paralelo a qualquer momento e setando timeout ou deixando o tempo indefinido para aguardar a resposta.
- Adicionado SubModulo AsyncRunnner com função dedicada a facilitar uso de funções assincronas podendo recuperar seus resultados usando menos código, é um modulo simples porem poupa-nos tempo. 
- Adicionado setor utils com funcionalidade de tornar o diretorio atual em um importavel relativo para o python
- Adicionado Automação de Navegadores! Sim estamos devendo esta feature a bastante tempo, porem estamos com a primeira versão disponivel, em breve teremos mais recursos e disponibilidade para outros navegadores, atualmente suporte apenas para *Chrome.*
- Mantemos o alerta! **get_dma** atualizada e **renomeada** para **get_dmy** para manter o padrão em ingles
- Função *send_email* atualizada para simplificar seu uso e funcionalidade em uma maior variedade de maquinas
- Melhoria nas descrições das funções e adicionado docstring (documentação explicativa) de todos Objetos e respectivas funções
- Sub-modulos agora como são Objetos internos do Objeto principal Suite pode ser acessado de duas formas, ex1: " from rpa_suite import rpa ; rpa.modulo.function() " ou então ex2: "from rpa_suite.core.Submodulo import NomeModulo ; meu_obj = NomeModulo() ; meu_obj.function()",
- Funções de regex e busca em textos foi simplificada e em breve estaremos adicionando funcionalidades mais interessantes.
- Correção e melhoria do Submodulo de Log. Tinhamos dois formatos de Log com duas bibliotecas e decidimos optar apenas pela Loguru para podermos dedicar mais atenção e fornecer recursos de Log mais completos, agora possui funcionalidade para indicar o caminho da pasta, nome da pasta, e também nome do arquivo, realizando stream tanto para o console (terminal) como também para o arquivo com todos levels já configurados e personalizados para ter distinção e facilitar o reconhecimento visual do que esta acontecendo no seu projeto.

## Mais Sobre

Para mais informações, visite nosso projeto no Github ou PyPi:

[Ver no GitHub](https://github.com/CamiloCCarvalho/rpa_suite)

[Ver projeto publicado no PyPI](https://pypi.org/project/rpa-suite/)

<hr>
