import os
import re

DEBUG = False

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
    r': [A-Z]\w*<.*?>',  # remove Typescript complex types like Promise<S, T>
]

regexs = [
    # (regex_pattern (with capture group), replace_to),
    (r"import {?\s?(\w+)\s?}? from '(.*)';?", 'from \\2 import \\1'),
    (r"let (.*);", '\\1 = None'),
    # if block
    (r"if \((.*)\)", 'if \\1:'),
    # forEach block
    (r"(\S*)\.forEach\(?(.*)=> {", 'for \\2 in \\1:'),  # will leave closing bracket
]

print(f'Running re.remove')
for regex in regex_remove:
    source = re.sub(regex, '', source)

print(f'Running re.sub')
for r in regexs:
    print(f'running [regex] {r[0]} [sub] {r[1]}')
    source = re.sub(r[0], r[1], source)
    if DEBUG:
        print('[result]')
        print(source)

# finding the first re, then within it , find the second re, then replace
regex_findall = [
    # handle js objects (python dicts)
    (r"= {[\s\S]*?}", r"(\w*): ", '"\\1": ')
]

print(f'Running nested re.sub')
for regex in regex_findall:
    found = re.findall(regex[0], source)
    for f in found:
        f_to = re.sub(regex[1], regex[2], f)
        # protect special characters
        f_to = f_to\
            .replace(special_characters['[CURLY_BRACKET_START]'], '[CURLY_BRACKET_START]')\
            .replace(special_characters['[CURLY_BRACKET_END]'], '[CURLY_BRACKET_END]')

        source = source.replace(f, f_to)

# block remove

position_interface = source.find('interface')
open_count = 0
close_count = 0
while open_count != 0 and close_count != open_count:
    for character in source[position_interface:]:  # starting from that position
        if character == '{':  # block start
            open_count += 1
        if character == '}':
            close_count += 1



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
    ('===', '=='),
    ('axios', 'requests'),
]

for replace in replaces:
    source = source.replace(replace[0], replace[1])

for bad_word in unnecessary_kw:
    source = source.replace(bad_word, '')

# line by line iteration
lines = source.splitlines()
for (index, line) in enumerate(lines):

    def current():
        # return the current version of the line
        return lines[index]

    def become(val):
        # mutate the line to something else
        lines[index] = val

    # remove trailing spaces
    become(current().rstrip())

    # append colon for [class, def, else]
    if current().strip().startswith(('class', 'def', 'else')):
        if not current().strip().endswith(':'):
            become(current() + ':')

    # handle function definition or prop declare in class
    if current().lstrip().startswith('public'):
        if current().rstrip().endswith(';'):
            # not function
            become(current().replace('public', ''))
        else:
            # function
            become(current().replace('public', 'def'))

    # remove line completely if it satisfy certain criteria
    if current().strip() == ')':  # dangling enclosing ) from if/for
        become('')

    # remove triling comma at the last because it was still useful before
    become(current().rstrip(';'))

    # trim irregular indentation
    extra_space = (len(current()) - len(current().lstrip())) % 4
    become(current().replace(' ', '', extra_space))

result = "\n".join(lines)


# reset protected characters to their original ones
for char_from, char_to in special_characters.items():
    result = result.replace(char_from, char_to)

with open(os.path.join('./example/out/', 'OpenVidu.py'), 'w+') as out:
    out.write(result)


