import io

def last_lines(file_path, buffer_size=io.DEFAULT_BUFFER_SIZE):
    """
    Reads a file in reverse line order, starting from the end, using a generator.

    Parameters
    ----------
    file_path : str
        Path to the file to be read.
    buffer_size : int, optional
        Size of the buffer in bytes (default: io.DEFAULT_BUFFER_SIZE).
        Must be at least 4 to handle UTF-8 decoding.

    Yields
    ------
    str
        Lines from the file in reverse order, including newline characters.

    Raises
    ------
    ValueError
        If `buffer_size` is less than 4.
    """
    
    if buffer_size < 4:
        raise ValueError('buffer_size must be at least 4')
    
    with open(file_path, 'rb') as file:
        file.seek(0, io.SEEK_END)
        position = file.tell()
        residual = b''

        while position > 0:
            read_size = min(buffer_size, position)
            position -= read_size
            file.seek(position)
            buffer = file.read(read_size) + residual
            residual = b''

            while True:
                try:
                    buffer = buffer.decode('utf-8')
                    break
                except UnicodeDecodeError:
                    residual += buffer[:1]
                    buffer = buffer[1:]  
                    
            lines = buffer.splitlines(keepends=True)
            for line in reversed(lines):
                yield line
                