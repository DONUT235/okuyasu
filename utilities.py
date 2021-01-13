import discord

def clean_string(content, lower=True):
    content = content.strip()
    if lower:
        content = content.lower()
    return content

def clean_message(message):
    return clean_string(message.clean_content)

def format_regex(phrase):
    return '`' + phrase + '`'
