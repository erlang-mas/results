import os, sys, re

CONSOLE_REGEX = re.compile('\Aconsole\.log\.\d+\Z')


for root, _dirs, fnames in os.walk(sys.argv[1]):
    part_names = sorted([fn for fn in fnames if CONSOLE_REGEX.match(fn)])
    if not part_names:
        continue
    part_names = list(reversed(part_names))
    part_names.append('console.log')

    dest_path = os.path.join(root, 'console.log.tmp')
    with open(dest_path, 'a') as dest:
        for part_name in part_names:
            part_path = os.path.join(root, part_name)
            with open(part_path, 'r') as part:
                data = part.read()
            dest.write(data)
            os.remove(part_path)
    os.rename(dest_path, dest_path[:-4])
