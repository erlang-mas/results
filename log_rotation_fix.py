import os, sys, re

CONSOLE_REGEX = re.compile('\Aconsole\.log\.\d+\Z')


for root, _dirs, filenames in os.walk(sys.argv[1]):
    part_names = sorted([fn for fn in filenames if CONSOLE_REGEX.match(fn)])
    if not any(part_names):
        continue
    dst_path = os.path.join(root, 'console.log')
    print root, dst_path
    with open(dst_path, 'a') as dst_file:
        for part_name in part_names:
            part_path = os.path.join(root, part_name)
            with open(part_path, 'r') as part_file:
                entries = part_file.read()
            dst_file.write(entries)
            os.remove(part_path)
