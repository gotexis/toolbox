from typing import Union


def block_replace(source, find, replace_with: Union[callable, str]): # todo: function type?
    """
    example to be removed:

    interface ISomething {
        name: string
        type: number
    }

    :param source: file content
    :param find:           `enum`
    :param replace_with:   either a callable or a string. (`class`)
    :return: file content without interface
    """
    while source.find(find) != -1:
        position_interface_start = source.find(find)
        position_interface = position_interface_start
        open_count = 0
        close_count = 0
        while open_count == 0 or close_count != open_count:
            character = source[position_interface]
            if character == '{':  # block start
                open_count += 1
            if character == '}':
                close_count += 1

            position_interface += 1

        shard = source[position_interface_start:position_interface]

        if callable(replace_with):
            # if replace_with is a function, call that on the code shard
            new_shard = replace_with(shard)
        elif type(replace_with) == str:
            new_shard = replace_with
        else:
            raise AttributeError(f'type of replace_with is {type(replace_with)}')
        # do the actual replace
        source = source.replace(shard, new_shard)
    return source


def block_remove(source, find):
    """
    above, replace with empty, effectively deleting it.
    :param source:
    :param find:
    :return:
    """
    return block_replace(source, find, '')
