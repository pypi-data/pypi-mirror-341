

def add_deps(dst):
    """
    Copy python.7z contents to dst.
    """
    import platform
    # detect os and make folder
    system = platform.system()

    if system == 'Darwin':
        system = 'darwin'
        delim = '/'
    elif system == 'Linux':
        system = 'linux'
        delim = '/'
    else:
        system = 'win'
        folder = 'windows'
        delim = '\\'

    import py7zr
    import os
    # Get the directory path to the current gupy.py file without the filename
    file_path = os.path.dirname(os.path.abspath(__file__))
    archive_path = file_path + delim + 'python.7z'

    with py7zr.SevenZipFile(archive_path, mode='r') as archive:
        archive.extractall(path=dst)


def main():
    print('Script run complete.')

if __name__ == '__main__':
    main()
    
