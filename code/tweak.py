#!/usr/local/bin/python

import os
import re
import sys

summary_pat = re.compile(r'^\s*#+\s*Summary\s*$', re.M)

def split_file(fname):
    with open(fname, 'rt') as f:
        txt = f.read()
    m = summary_pat.search(txt)
    if m:
        i = m.start()
        prefix = txt[:i]
        rest = txt[i:]
        return prefix, rest
    return None, None


bad_line_pats = '|'.join([
    r"\[[-A-Za-z0-9' ]+\s*\]\s*:\s*#[-a-z0-9]+",
    r"-\s*((?:HIPE )?PR|Name|Jira Issue)\s*:\s.*?"
])
remove_pat = re.compile(r"^(\s*(X)\s*)\n".replace('X', bad_line_pats), re.M)

status_block = '''

## Status
- Status: [PROPOSED](/README.md#hipe-lifecycle)
- Status Date: (date of first submission or last status change)
- Status Note: (explanation of current status; if adopted, 
  links to impls or derivative ideas; if superseded, link to replacement)

'''

def tweak(prefix, rest, fname):
    prefix = re.sub(remove_pat, '', prefix.lstrip())
    block = status_block
    if 'moved to github.com/hyperledger/aries-rfcs' in prefix:
        block = block.replace('PROPOSED', 'SUPERSEDED')
    prefix = prefix.rstrip() + block
    rest = re.sub(remove_pat, '', rest.lstrip())
    with open(fname + '.tmp', 'wt') as f:
        f.write(prefix)
        f.write(rest)
    os.remove(fname)
    os.rename(fname + '.tmp', fname)


def main(fname):
    print(fname)
    prefix, rest = split_file(fname)
    if not prefix:
        print('  Does not match pattern')
    else:
        tweak(prefix, rest, fname)


if __name__ == '__main__':
    for root, folders, files in os.walk(sys.argv[1]):
        for f in files:
            if f == 'README.md':
                main(os.path.join(root, f))
