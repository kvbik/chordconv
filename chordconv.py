"""
merge chord lines with lyrics
"""

# all over the place
# https://stackoverflow.com/questions/4628290/pairs-from-single-list

# chords
# https://pisnicky-akordy.cz/greenhorns/kdyz-nas-tata-hral

import sys
import re

def normalize_indeces(indeces):
    """
    (1,2,3,4,5) => (0,1),(1,2),(2,3),(3,4),(4,5),(5,None)
    """
    l = [0] + indeces + [None]
    return zip(l, l[1:])

def split_line(line, indeces):
    slices = normalize_indeces(indeces)
    return [ line[s[0]:s[1]] for s in slices ]

def merge_two_lines(chords_line, lyrics_line):
    matches = re.finditer(r'\S+', chords_line)
    chords = []
    indeces = []
    for m in matches:
        chords.append('[%s]' % m.group(0))
        indeces.append(m.start())
    chords.append('')
    splits = split_line(lyrics_line, indeces)
    output = ''
    for s,c in zip(splits, chords):
        output += s
        output += c
    return output

def merge_chords(lines):
    for chords, lyrics in zip(lines[::2], lines[1::2]):
        yield merge_two_lines(chords, lyrics)

def test():
    assert [(0,0), (0,4), (4,14), (14,None)] == list(normalize_indeces([0, 4, 14]))

    assert ['', 'hello', ' mrs magi', 'cal'] == split_line('hello mrs magical', [0, 5, 14])

    chords = 'A7   V8/10    M'
    lyrics = 'hello mrs magical'
    assert '[A7]hello[V8/10] mrs magi[M]cal' == merge_two_lines(chords, lyrics)

    # empty assert
    assert ['', ''] == list(merge_chords(['', '', '', '']))
    # integration test
    input_lines = [
        '    D',
        'Kdyz jsem byl chlapec malej, tak metr nad zemi,',
        '   G                    D',
        'schazeli se farmari tam u nas v prizemi.',
    ]
    expected_lines = [
        'Kdyz[D] jsem byl chlapec malej, tak metr nad zemi,',
        'sch[G]azeli se farmari tam [D]u nas v prizemi.',
    ]
    assert expected_lines == list(merge_chords(input_lines))

def main():
    # https://en.wikibooks.org/wiki/Python_Programming/Input_and_Output
    for line in merge_chords(sys.stdin.readlines()):
        print(line, end="")

if __name__ == "__main__":
    test()
    main()

