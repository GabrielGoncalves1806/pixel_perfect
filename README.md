# Pixel Perfect Overlay

Pixel Perfect Overlay é um utilitário simples feito em PyQt6 para ajudar designers e desenvolvedores a testar se uma interface em desenvolvimento está fiel ao layout original. Ele exibe uma imagem (mockup ou screenshot de referência) em uma janela sempre no topo com controles de opacidade e escala, permitindo sobrepor a imagem enquanto se valida a implementação.

## Funcionalidades principais

- **Seleção rápida de imagem:** ao abrir o app, basta escolher o arquivo PNG/JPG/BMP que servirá como referência.
- **Janela flutuante:** a janela permanece acima das demais para facilitar a comparação com a aplicação em teste.
- **Controle de opacidade:** ajuste a transparência para enxergar o app por trás do mockup e comparar alinhamentos.
- **Escala precisa:** controle deslizante de 10% a 300% com suporte a valores decimais via campo de texto para ajustes finos.
- **Área rolável:** caso o mockup seja maior que a janela, use o scroll para navegar pela imagem.

## Como usar

1. Execute `python application/pixel_perfect.py` (com o ambiente virtual ativado, se houver).
2. Selecione a imagem de referência quando o diálogo de arquivos abrir.
3. Use os controles no painel superior:
   - Ajuste a **opacidade** para revelar ou esconder partes da interface real.
   - Defina a **escala** com o slider ou digite um valor decimal no campo abaixo.
4. Posicione a janela sobre a aplicação que deseja verificar e ajuste conforme necessário.

## Casos de uso

- Verificar se espaçamentos, fontes e ícones seguem o design aprovado.
- Conferir responsividade e proporções quando a aplicação escala em diferentes resoluções.
- Comparar variações de layout sem precisar abrir ferramentas pesadas de design.

## Próximos passos sugeridos

- Adicionar suporte a múltiplas imagens e troca rápida entre versões.
- Permitir salvar presets de opacidade/escala por projeto.
- Implementar atalhos de teclado para ajustes ainda mais rápidos.

> Este repositório foi pensado para auxiliar na rotina de QA visual e garantir entregas com fidelidade ao layout original.