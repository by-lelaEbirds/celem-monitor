import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

URL = os.getenv("CELEM_URL", "https://www.cep.pr.gov.br/Pagina/CELEM")
STATE_FILE = Path("celem_state.json")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

KEYWORDS = [
    r"ANO\s+20\d{2}.*Semestre",
    r"Processo\s+Classificat[oó]rio",
    r"CELEM",
]


def send_telegram(text: str) -> None:
    if not TOKEN or not CHAT_ID:
        print("Telegram não configurado. Defina TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID.")
        return

    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )
    response.raise_for_status()


def normalize(text: str) -> str:
    return " ".join(text.split()).strip()


def extract_items(html: str):
    soup = BeautifulSoup(html, "html.parser")
    items = []

    # Links principais, como "ANO 2026 / 1º Semestre..."
    for a in soup.find_all("a"):
        text = normalize(a.get_text(" ", strip=True))
        href = a.get("href", "")
        full_url = urljoin(URL, href)

        if any(re.search(pattern, text, re.I) for pattern in KEYWORDS):
            if text:
                items.append({"text": text, "url": full_url})

    # Remove duplicados mantendo ordem
    seen = set()
    unique = []
    for item in items:
        key = (item["text"], item["url"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


def main() -> None:
    response = requests.get(URL, timeout=30, headers={"User-Agent": "CELEM-CEP-Monitor/1.0"})
    response.raise_for_status()

    current_items = extract_items(response.text)
    current = {"items": current_items}

    if not STATE_FILE.exists():
        STATE_FILE.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
        send_telegram(
            "✅ Monitor CELEM/CEP ativado.\n\n"
            "Estado inicial salvo. A partir de agora eu aviso quando aparecer algo novo.\n"
            f"Página monitorada: {URL}"
        )
        return

    old = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    old_keys = {(item.get("text"), item.get("url")) for item in old.get("items", [])}

    new_items = [
        item for item in current_items
        if (item.get("text"), item.get("url")) not in old_keys
    ]

    if new_items:
        msg = "🚨 NOVA ATUALIZAÇÃO NO CELEM/CEP!\n\n"
        for item in new_items:
            msg += f"• {item['text']}\n{item['url']}\n\n"
        msg += f"Página: {URL}"
        send_telegram(msg)
        STATE_FILE.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print("Nada novo encontrado.")


if __name__ == "__main__":
    main()
