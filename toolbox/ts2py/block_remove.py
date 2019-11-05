def block_remove(source, find):
    # block remove all interface block <TS>
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

        to_replace = source[position_interface_start:position_interface]
        source = source.replace(to_replace, '')
    return source
