from gtts import gTTS, gTTSError
from os import path
from logging import error, info


def vocalize(output: str, content: str, lang: str = 'en', accent: str = 'co.uk') -> bool:
    if path.exists(output):
        if input(f"File already exists: {output}, would you like to replace it? [y/n]").lower() == 'y':
            return False
    
    acontent = gTTS(content, lang=lang, tld=accent)

    with open(output, 'wb') as awriter:
        try:
            acontent.write_to_fp(awriter)
            info(f"Written audiobook to: {output}")
        except gTTSError as exp:
            error(f"Failed to write text to speech content, {str(exp)}")
            return False


def generate_audiobook(novel: str, source: str, audifiy: str) -> None:
    pass
