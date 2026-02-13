
# Organizador de Fotos Didáticas

Este projeto é um sistema de gestão de ativos digitais focado na organização automatizada de imagens. Ele utiliza metadados EXIF para classificar fotos cronologicamente, elimina duplicatas e gera galerias de visualização.

## Funcionalidades

*   **Organização Cronológica**: Move fotos para uma estrutura de pastas `Ano/Mês/Dia` baseada na data original da foto (EXIF) ou data de modificação do arquivo.
*   **Deduplicação Inteligente**: Identifica arquivos duplicados (mesmo conteúdo) usando hash MD5 e os move para uma pasta `Quarantine`, evitando redundância.
*   **Monitoramento em Tempo Real**: Um serviço "Watchdog" que monitora uma pasta de entrada e organiza/deduplica novos arquivos automaticamente assim que são adicionados.
*   **Galeria Web**: Gera uma galeria HTML estática com thumbnails para facilitar a navegação e visualização das fotos organizadas.
*   **Skill Antigravity**: Lógica encapsulada como uma "Skill" reutilizável para agentes de IA.

## Pré-requisitos

*   Python 3.12+
*   Bibliotecas Python: `Pillow`, `watchdog`

## Instalação

1.  Clone o repositório:
    ```bash
    git clone <url-do-repositorio>
    cd "Organizador de fotos"
    ```

2.  Crie e ative um ambiente virtual (recomendado):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  Instale as dependências:
    ```bash
    pip install Pillow watchdog
    ```

## Como Usar

### 1. Organização e Deduplicação Automática (Monitor)

Para iniciar o serviço que monitora uma pasta e organiza os arquivos automaticamente:

```bash
python src/monitor.py <pasta_origem> <pasta_destino> <pasta_quarentena>
```

Exemplo:
```bash
python src/monitor.py "C:\Fotos\Entrada" "C:\Fotos\Organizadas" "C:\Fotos\Quarentena"
```

### 2. Organização Manual de Diretório Existente

Você pode usar o script `organizer.py` diretamente via Python:

```python
from src.organizer import process_directory
process_directory("caminho/para/fotos_brutas", "caminho/para/fotos_organizadas")
```

### 3. Gerar Galeria Web

Para criar uma galeria HTML das fotos já organizadas:

```bash
python src/gallery_generator.py <pasta_fotos_organizadas> <pasta_saida_galeria>
```

Abra o arquivo `index.html` gerado na pasta de saída para visualizar suas fotos.

## Estrutura do Projeto

*   `src/`: Código fonte dos scripts principais.
    *   `deduplicator.py`: Lógica de detecção de duplicatas (MD5).
    *   `exif_extractor.py`: Extração de datas via EXIF.
    *   `gallery_generator.py`: Gerador de galeria HTML.
    *   `monitor.py`: Serviço de monitoramento de diretório.
    *   `organizer.py`: Lógica de movimentação e organização de arquivos.
*   `tests/`: Testes unitários para todos os módulos.
*   `skills/organizer/`: Versão encapsulada do projeto como uma Skill Antigravity.

## Testes

Para executar a suite de testes automatizados:

```bash
python -m unittest discover tests
```

---
Desenvolvido com o protocolo Ralph de agentes autônomos.

## 🤝 Apoie o Projeto

Se este projeto foi útil para você, considere fazer uma doação para apoiar o desenvolvimento contínuo!

### 🇧🇷 Pix
<img src="assets/qrcode_pix.jpg" alt="QR Code Pix" />

**Chave Pix**: `539.370.071-72`

### 🟩 Wise
<img src="assets/qrcode_wise.jpg" alt="QR Code Wise" />

[Clique aqui para doar via Wise](https://wise.com/pay/r/sxi6xirdFOblxUE)

### ₿ Criptomoedas
<img src="assets/qrcode_btc.png" alt="QR Code Bitcoin" />

**Bitcoin (BTC)**: `bc1q0rxcdtch7ak5rqzls5a23xlvr2fl5ll3szd40x`

### 🔹 Ethereum
<img src="assets/qrcode_eth.jpg" alt="QR Code Ethereum" />

**Ethereum (ETH)**: `0x54B8AE351a513866B39c753d9a08B1465e3aD01C`
