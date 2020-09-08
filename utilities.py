import discord

def clean_string(content):
    return content.strip().lower()

def clean_message(message):
    return clean_string(message.clean_content)

def format_regex(phrase):
    return '`' + phrase + '`'
