import os
import re
from toolbox.ts2py.block_remove import block_remove, block_replace
from toolbox.ts2py.transfomers import enum_transformer

DEBUG = False


def main(filename, out_dir):
    output_name = os.path.basename(filename).replace('.ts', '.py')

    # handle index naming convention
    if output_name == 'index.py':
        output_name = '__init__.py'

    with open(filename) as f:
        source = f.read()

    # for protection of certain characters. replace them back at the end of the pipe.
    special_characters = {
        '[CURLY_BRACKET_START]': '{',
        '[CURLY_BRACKET_END]': '}',
    }

    regex_remove = [
        r': [A-Z]\w*<.*?>',  # remove Typescript complex types like Promise<S, T>
        r'[A-Z]\w*<.*?>',  # remove Typescript complex types like Promise<S, T>
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
        (r"export (.*) from '(.*)'", "from \\2 import \\1"),
        # ? : short if else
        (r"(\=|\:) (.*) \? (.*) \: (.*)", '\\1 \\3 if \\2 else \\4'),
        (
            r"axios\.(post|get|put|delete)([\s\S]*?)\.then\((.*) => {([\s\S]*?).catch",
            "\\3 = requests.\\1\\2\n\\4"
        ),
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
        # todo: problem with below not handling nested object.
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
        'not  not',
    ]

    replaces = [
        # comment start
        ('/**', '"""'),
        ('/*', '"""'),
        # comment end
        (' */', '"""'),
        ('*/', '"""'),
        # comment middle
        ('* ', ''),
        ('//', '#'),
        # class identifier
        ('namespace', 'class'),
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
        ('||', 'or'),
        # library
        ('&&', 'and'),
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

        def current_strip():
            # return the current version of the line
            return current().strip()

        def previous():
            # return the current version of the last line
            return lines[index - 1]

        def become(val):
            # mutate current line to something else
            lines[index] = val

        def find_indentation(val=current()):
            return len(current()) - len(current().lstrip())

        # remove trailing spaces
        become(current().rstrip().rstrip(';'))

        # append colon for [class, def, else]
        if current_strip().startswith(('class', 'def', 'else')):
            if not current_strip().endswith(':'):
                become(current() + ':')

        # handle function definition or prop declare in class
        if current_strip().startswith('public'):
            if current_strip().endswith('{') or '(' in current():
                # is function
                become(current().replace('public', 'def'))
                if not current().rstrip().endswith(':'):
                    become(current() + ':')
                if previous().lstrip().startswith('def'):
                    become(' ' * (find_indentation(previous()) + 4)
                           + 'pass' + '\n' + current())
            else:
                # not function, but a type declaration
                become(current().replace('public', '') + ' = None')

        # special case for functions like `someFunction()`
        if current_strip().endswith('()'):
            if not current_strip().startswith('def'):
                become(" " * find_indentation() + 'def ' + current_strip() + ':')

        # stll not valid yet

        # remove line completely if it satisfy certain criteria
        # if current().strip() == ')':  # dangling enclosing ) from if/for
        #     become('')

        # remove triling comma at the last because it was still useful before
        become(current().rstrip(';'))

        # trim irregular indentation
        extra_space = find_indentation() % 4
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
