# list-comparator

Ferramenta simples para comparar duas listas (arquivos linha-a-linha) e gerar relatórios de itens adicionados, removidos e em comum.

## Recursos
- Comparação de duas listas texto (linha por linha).
- Formatos de saída: texto, JSON e CSV.
- Opções: ignorar maiúsculas/minúsculas, remover espaços, ordenação, chave por coluna.
- Pode ser usada como CLI e como biblioteca em scripts.

## Instalação
Prerequisitos: Node.js (ou adapte para sua stack).
Exemplo usando npm:
```bash
npm install -g list-comparator
```
Ou clone o repositório e instale dependências:
```bash
git clone <repo-url>
cd list-comparator
npm install
```

## Uso (CLI)
Comparar dois arquivos:
```bash
list-comparator path/to/old.txt path/to/new.txt
```
Opções comuns:
```
--json           saída em JSON
--csv            saída em CSV
--ignore-case    ignora diferenças de maiúsculas/minúsculas
--trim           remove espaços em torno das linhas
--key <n>        usa a coluna n (base 0) como chave ao usar delimitador
--delimiter <c>  delimitador de colunas (ex: , ou ;)
--sort           ordena as listas antes de comparar
```
Exemplo com saída JSON e ignorando case:
```bash
list-comparator old.txt new.txt --json --ignore-case > diff.json
```

## Uso (API — exemplo em Node.js)
Exemplo mínimo como biblioteca:
```js
const Comparator = require('list-comparator');

const a = ['alice', 'bob', 'carol'];
const b = ['bob', 'dave', 'carol'];

const result = Comparator.compare(a, b, { ignoreCase: true });
// result = { added: ['dave'], removed: ['alice'], common: ['bob','carol'] }
```

## Formato de saída
- Texto (padrão): seções "Added", "Removed", "Common".
- JSON:
```json
{
    "added": ["..."],
    "removed": ["..."],
    "common": ["..."]
}
```
- CSV: três colunas ou arquivos separados conforme desejado.

## Boas práticas
- Normalizar entradas (trim, lower-case) para comparações previsíveis.
- Usar chave por coluna ao comparar arquivos CSV com múltiplas colunas.
- Para listas grandes, habilitar streaming ou processamento por lotes para reduzir uso de memória.

## Testes
Exemplo de comando de teste (se houver suíte):
```bash
npm test
```

## Contribuição
1. Fork do repositório
2. Crie uma branch com a feature/bugfix
3. Abra PR com descrição e testes

## Licença
Licença MIT — ver arquivo LICENSE para detalhes.

## Contato
Abra uma issue no repositório para reportar bugs ou solicitar recursos.
