import os
import re

base_dir = '/Users/exiszhang/proj-exis/openvidu/openvidu-node-client/src/'

file_name = os.path.join(base_dir, 'OpenVidu.ts')

with open(file_name) as f:
    source = f.read()

# for protection of certain characters. replace them back at the end of the pipe.
special_characters = {
    '[CURLY_BRACKET_START]': '{',
    '[CURLY_BRACKET_END]': '}',
}

regex_remove = [
    r'Promise<.*?>',
]

regexs = [
    # (regex_pattern (with capture group), replace_to),
    (r"import {?\s?(\w+)\s?}? from '(.*)';", 'from \\2 import \\1'),
    (r"let (.*);", '\\1 = None'),
    (r"if \((.*)\)", 'if \\1:'),
]

for regex in regex_remove:
    source = re.sub(regex, '', source)

for regex in regexs:
    source = re.sub(regex[0], regex[1], source)

# finding the first re, then within it , find the second re, then replace

regex_findall = [
    # handle js objects (python dicts)
    (r"= {[\s\S]*?}", r"(\w*): ", '"\\1": ')
]

for regex in regex_findall:
    found = re.findall(regex[0], source)
    for f in found:
        f_to = re.sub(regex[1], regex[2], f)
        # protect special characters
        f_to = f_to\
            .replace(special_characters['[CURLY_BRACKET_START]'], '[CURLY_BRACKET_START]')\
            .replace(special_characters['[CURLY_BRACKET_END]'], '[CURLY_BRACKET_END]')

        source = source.replace(f, f_to)

# remove necessary keywords
unnecessary_kw = [
    # python doesnt need export, new, const, let, var
    'export ',
    'new ',
    '{',
    '}',
    # ts keywords
    'private ',
    # 'public ',
    'static ',
    'readonly ',
    'const ',
    'let ',
    'var ',
]

replaces = [
    # comment start
    ('/**', '"""'),
    ('/*', '"""'),
    # comment end
    (' */', '"""'),
    ('*/', '"""'),
    # comment middle
    ('*', ''),
    ('//', '#'),
    # class identifier
    ('this', 'self'),
    ('constructor', 'def __init__'),
    # unnecessary question mark
    ('?:', ':'),
    # incorrect import syntax (relative)
    ('from ./', 'from .'),
    # different types
    ('number', 'int'),
    ('!', ' not '),
    ('else if', 'elif'),
    (': string', ': str'),
]

for replace in replaces:
    source = source.replace(replace[0], replace[1])

for bad_word in unnecessary_kw:
    source = source.replace(bad_word, '')

# line by line iteration
lines = source.splitlines()
for (index, line) in enumerate(lines):

    def

    # remove trailing spaces
    lines[index] = lines[index].rstrip()
    # append colon for classes
    if line.lstrip().startswith(('class', 'def', 'else')) and not line.rstrip().endswith(':'):
        lines[index] = line + ':'

    # trim irregular indentation
    extra_space = (len(lines[index]) - len(lines[index].lstrip())) % 4
    lines[index] = lines[index].replace(' ', '', extra_space)

    # handle function definition or prop declare in class
    if lines[index].lstrip().startswith('public'):
        if lines[index].rstrip().endswith(';'):
            # not function
            lines[index] = lines[index].replace('public', '')
        else:
            # function
            lines[index] = lines[index].replace('public', 'def')

    # remove triling comma at the last because it was still useful before
    lines[index] = lines[index].rstrip(';')

result = "\n".join(lines)


# reset protected characters to their original ones
for char_from, char_to in special_characters.items():
    result = result.replace(char_from, char_to)

with open(os.path.join('./example/out/', 'OpenVidu.py'), 'w+') as out:
    out.write(result)


