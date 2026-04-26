# Monitor CELEM CEP

Bot que monitora a página do CELEM do Colégio Estadual do Paraná e avisa no Telegram quando surgir um novo link/edital/turma.

Página monitorada:
https://www.cep.pr.gov.br/Pagina/CELEM

## Como usar no GitHub

1. Crie um repositório no GitHub.
2. Envie todos os arquivos deste ZIP para o repositório.
3. Vá em `Settings > Secrets and variables > Actions > New repository secret`.
4. Crie estes secrets:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

5. No GitHub, vá em `Actions > Monitor CELEM CEP > Run workflow` para testar.

Depois disso, o GitHub vai verificar a página a cada 30 minutos.

## Como pegar o TELEGRAM_CHAT_ID

1. No Telegram, mande qualquer mensagem para o seu bot.
2. Abra este link no navegador, trocando TOKEN_AQUI pelo token do seu bot:

```text
https://api.telegram.org/botTOKEN_AQUI/getUpdates
```

3. Procure por algo como:

```json
"chat":{"id":123456789
```

Esse número é o seu `TELEGRAM_CHAT_ID`.

## Como testar no seu PC

Crie variáveis de ambiente:

### Windows PowerShell

```powershell
$env:TELEGRAM_BOT_TOKEN="SEU_TOKEN"
$env:TELEGRAM_CHAT_ID="SEU_CHAT_ID"
python monitor.py
```

### Linux/macOS

```bash
export TELEGRAM_BOT_TOKEN="SEU_TOKEN"
export TELEGRAM_CHAT_ID="SEU_CHAT_ID"
python monitor.py
```
