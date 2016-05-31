# -*- coding: utf-8 -*-

import os


class FileTree():
    """Holds project file tree.

    """
    def __init__(self, root_folder, skip_dirs=[], extensions=['f', 'f77']):
        self.files = []
        self.root_folder = os.path.abspath(root_folder)
        self.skip_dirs = skip_dirs
        self.extensions = extensions

        s_skip_dirs = set(skip_dirs)
        s_extensions = set([ext.lower() for ext in extensions])

        for dirpath, dirnames, filenames in os.walk(self.root_folder):
            for directory in s_skip_dirs:
                if directory in dirnames:
                    dirnames.remove(directory)

            if extensions == []:
                self.files.extend([
                    os.path.join(dirpath, filename) for filename in filenames
                ])
            else:
                self.files.extend([
                    os.path.join(dirpath, filename)
                    for filename in filenames
                    if os.path.splitext(filename)[1][1:].lower() in s_extensions
                ])

    def __str__(self):
        previous_folder = self.root_folder
        text = previous_folder + '\n'
        depth = 0

        for file_name in self.files:

            current_folder = os.path.dirname(file_name)
            relpath = os.path.relpath(
                current_folder, previous_folder).split('/')

            for it in relpath:
                if it == '.':
                    pass
                elif it == '..':
                    depth -= 1
                else:
                    text += '\n{0}>{1}:'.format('  '*depth, it)
                    depth += 1

            text += '\n{0}{1}'.format('  '*depth, os.path.basename(file_name))

            previous_folder = current_folder

        return text


if __name__ == '__main__':
    ft = FileTree(
        '/home/jure/programming/mc_shms_single',
        skip_dirs=['infiles', 'outfiles', 'workfiles', '.git'],
        extensions=['f']
    )

    print(ft)
