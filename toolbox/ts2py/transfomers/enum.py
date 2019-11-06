def enum_transformer(source: str):
    source = source.replace('enum', 'class')
    source = source.replace(',', '')
    return source

