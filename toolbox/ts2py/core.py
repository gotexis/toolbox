import os
import re
from toolbox.ts2py.block_remove import block_remove, block_replace
from toolbox.ts2py.transfomers import enum_transformer

DEBUG = False


def main(filename, out_dir):
    output_name = os.path.basename(filename).replace('.ts', '.py')
    with open(filename) as f:
        source = f.read()

    # for protection of certain characters. replace them back at the end of the pipe.
    special_characters = {
        '[CURLY_BRACKET_START]': '{',
        '[CURLY_BRACKET_END]': '}',
    }

    regex_remove = [
        r': [A-Z]\w*<.*?>',  # remove Typescript complex types like Promise<S, T>
        r': \w{1,}\[\]',  # remove Typescript List type such as ISomething[]
        # note: this can be changed to using python union type, but not worth the trouble
    ]

    regexs = [
        # (regex_pattern (with capture group), replace_to),
        # import syntax
        (r"import {?\s?(\w+)\s?}? from '(.*)';?", 'from \\2 import \\1'),
        # let declare (can make include var)
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
            f_to = f_to \
                .replace(special_characters['[CURLY_BRACKET_START]'], '[CURLY_BRACKET_START]') \
                .replace(special_characters['[CURLY_BRACKET_END]'], '[CURLY_BRACKET_END]')

            source = source.replace(f, f_to)

    # block remove all interface block <TS>
    source = block_remove(source, 'interface')
    source = block_replace(source, 'enum', enum_transformer)

    # remove necessary keywords
    unnecessary_kw = [
        # python doesnt need export, new, const, let, var
        'export ',
        'new ',
        '{',
        '}',
        # ts keywords
        'private ',
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
        ('constructor(', 'def __init__(self, '),
        ('equalTo(', 'def __eq__(self, '),
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

    # remove starting empty lines
    while not lines[0].strip():
        lines.pop(0)

    for (index, line) in enumerate(lines):

        def current():
            # return the current version of the line
            return lines[index]

        def previous():
            # return the current version of the line
            return lines[index - 1]

        def become(val):
            # mutate the line to something else
            lines[index] = val

        # remove trailing spaces
        become(current().rstrip().rstrip(';'))

        # append colon for [class, def, else]
        if current().strip().startswith(('class', 'def', 'else')):
            if not current().strip().endswith(':'):
                become(current() + ':')

        # handle function definition or prop declare in class
        if current().lstrip().startswith('public'):
            if current().rstrip().endswith('{') or '(' in current():
                # is function
                become(current().replace('public', 'def'))
                if not current().rstrip().endswith(':'):
                    become(current() + ':')
                if previous().lstrip().startswith('def'):
                    become(' ' * (len(previous()) - len(previous().lstrip()) + 4)
                           + 'pass' + '\n' + current())
            else:
                # function
                become(current().replace('public', '') + ' = None')

                # stll not valid yet

        # remove line completely if it satisfy certain criteria
        if current().strip() == ')':  # dangling enclosing ) from if/for
            become('')

        # remove triling comma at the last because it was still useful before
        become(current().rstrip(';'))

        # trim irregular indentation
        extra_space = (len(current()) - len(current().lstrip())) % 4
        become(current().replace(' ', '', extra_space))

    # from this point source become result (or can still use source word)

    result = "\n".join(lines)

    # reset protected characters to their original ones
    for char_from, char_to in special_characters.items():
        result = result.replace(char_from, char_to)

    # tokenize the whole thing to migrate pascalCase to snake_case
    # caveat: indentation is not preserved, multispace is not handled
    # tokenized = result.splitlines()
    # for (index, token_line) in enumerate(tokenized):
    #     tokenized[index] = token_line.split()
    # print(tokenized)

    # save
    with open(os.path.join(out_dir, output_name), 'w+') as out:
        out.write(result)
