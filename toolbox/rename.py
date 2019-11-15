import os, re

"""
Batch renaming files
"""


def search_replace(path: str, find: str, replace: str) -> None:
    """
    Case insensitive find and replace in a folder, recursively.
    :param path:
    :param find:
    :param replace:
    :return:
    """
    for root, dirs, files in os.walk(path):
        for filename in files:
            insensitive_rep = re.compile(re.escape(find), re.IGNORECASE)
            new_filename = insensitive_rep.sub(replace, filename)
            if filename != new_filename:
                # Print which file will be changed
                print(root + os.sep + filename, ' => ', new_filename)
                # do the rename
                os.rename(root + os.sep + filename, root + os.sep + new_filename)


def rename_to_sequential(path: str, ext: str = 'jpg', prefix: str = '') -> None:
    """
    Case insensitive find and replace in a folder, recursively.
    :param ext:
    :param path:
    :return:
    """
    counter = 1

    for root, dirs, files in os.walk(path):
        for filename in files:
            new_filename = f'{prefix}{counter}.{ext}'
            if filename != new_filename:
                # Print which file will be changed
                print(root + os.sep + filename, ' => ', new_filename)
                # do the rename
                os.rename(root + os.sep + filename, root + os.sep + new_filename)
                counter += 1
