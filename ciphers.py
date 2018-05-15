import fnmatch
import os
import random
import string
#  ~ import test-ml
# To resolve ModuleNotFound Error
import sys
sys.path.append('../')
import ml  # noqa

PG_DIR = os.path.abspath(os.path.join(".", "corpora"))
W_DIR = os.path.abspath(".")


def simplify(text, keep_spaces=False):
    """Strips non-letter characters and returns uppercase text."""
    return ''.join([letter.upper() if (letter in string.ascii_letters
                   or (keep_spaces and letter == ' '))
                   else '' for letter in text])


def get_all_frequencies(text, simplify_first=True, skip_bigraphs=False):
    """Gets all frequencies of letters, bigraphs, and trigraphs.

    Gets frequencies of letters 'A', bigraphs 'AB', trigraphs 'ABC',
    and skip bigraphs, 'A_C'
    Returns a dictionary mapping each graph to its frequency."""
    if simplify_first:
        text = simplify(text)
    text_counts = {}
    for idx, letter in enumerate(text):
        text_counts[letter] = text_counts.get(letter, 0) + 1
        if idx < (len(text) - 1):
            bigraph = text[idx:idx+2]
            text_counts[bigraph] = text_counts.get(bigraph, 0) + 1
            if idx < (len(text) - 2):
                trigraph = text[idx:idx+3]
                text_counts[trigraph] = text_counts.get(trigraph, 0) + 1
                if skip_bigraphs:
                    skip_bigraph = trigraph[0] + '?' + trigraph[2]
                    text_counts[skip_bigraph] = text_counts.get(skip_bigraph,
                                                                0) + 1
    text_frequencies = {}
    text_len = len(text)
    for graph in text_counts.keys():
        text_frequencies[graph] = (text_counts[graph] / (text_len
                                   - (len(graph) - 1)))
    return text_frequencies


def get_gutenberg_filenames(directory):
    filenames = fnmatch.filter(os.listdir(directory), 'pg*.txt')
    outval = []
    for fn in filenames:
        outval.append(os.path.join(directory, fn))
    return outval


def random_english_text(length, simplified=True):
    """Grabs random English line from random Proj Gutenberg book."""
    fns = get_gutenberg_filenames(PG_DIR)
    book_fn = random.choice(fns)
    book_len = os.path.getsize(book_fn)
    with open(book_fn, 'r') as book:
        # find an index far enough from the end to satisfy length, even if
        # simplified (skipping non-letters). doubling length is a bit hacky
        # could catch reading to the end and expand forward, but that would
        # bias the random choice
        idx = random.randint(0, book_len - (2*length))
        book.seek(idx)
        rnd_text = ''
        while len(rnd_text) < length:
            tmp_letter = book.read(1)
            if tmp_letter == '':
                book.seek(0)
                tmp_letter = book.read(1)
            if tmp_letter in string.ascii_letters or not simplified:
                rnd_text += tmp_letter
    if simplified:
        rnd_text = rnd_text.upper()
    return rnd_text


def garble(in_string, letter=None):
    """Replaces a random character in_string with another letter.

    Could complicate naive cryptanalysis, so useful for generating test
    cases."""
    if letter is None:
        letter = random.choice(string.ascii_uppercase)
    idx = random.randint(0, len(in_string) - 1)
    return in_string[:idx] + letter + in_string[idx+1:]


def garble_repeatedly(in_string, n):
    """Replaces random characters in in_string with random letters.

    Could complicate naive cryptanalysis, so useful for generating test
    cases."""
    tmp_txt = in_string
    for i in range(n):
        tmp_txt = garble(tmp_txt)
    return tmp_txt


def skip(message, val, offset=None):  # offset=0):
    if offset is None:
        offset = val-1
    out_msg = ""
    for i in range(len(message)):
        idx = (((i * val) + offset) % len(message))
        out_msg += message[idx]
    return out_msg


def random_skip_text(length, skipval=None):
    if skipval is None:
        skipval = random.randint(2, length - 2)
    t = random_english_text(length)
    return skip(t, skipval)


def index_of_coincidence(ct):
    running_sum = 0
    counts = {}
    for letter in ct:
        if letter in counts.keys():
            counts[letter] += 1
        else:
            counts[letter] = 1
    for letter in counts.keys():
        count = counts[letter]
        running_sum += (count*(count-1))
    return (running_sum / (len(ct) * (len(ct)-1)))


def header(key):
    h = []
    for l in (key.upper() + string.ascii_uppercase):
        if l not in h and l in string.ascii_uppercase:
            h.append(l)
    return ''.join(h)


def encipher(pt, key, header_key=""):
    hdr = header(header_key)
    ct = ""
    for count in range(len(pt)):
        pt_idx = hdr.find(pt[count])
        key_idx = hdr.find(key[count % len(key)])
        ct += hdr[(pt_idx + key_idx) % 26]
    return ct


def random_enciphered_text(length, k1='ABCISSA', k2='KRYPTOS'):
    t = random_english_text(length)
    return encipher(t, k1, k2)


def random_english_or_noise(length=97, english=None, noise_type=None):
    """Generates either english or noise.

    Randomly chooses English or noise to generate, then generates a string
    of length "l" You can specify english as True or False for seeding and
    testing. You can specify three noise types: VIGENERE, SKIP, and RANDOM
    Where VIGENERE and SKIP randomly encipher some block of english text
    and RANDOM just generates a string of characters selected randomly one
    at a time This module is useful for generating test data for functions
    that detect whether or not something is English or encrypted or just
    random noise."""
    if noise_type is None:
        noise_type = "VIGENERE"  # SKIP, RANDOM
    if english is None:
        english = random.choice((True, False))
    assert english in [True, False]
    if english:
        return random_english_text(length)
    elif noise_type == "RANDOM":
        out = ''
        for i in range(length):
            out += random.choice(string.ascii_uppercase)
        return out
    elif noise_type == "VIGENERE":
        return random_enciphered_text(length)
    elif noise_type == "SKIP":
        sv = random.randint(length//3, 2*length//3)
        return random_skip_text(length, sv)


# SAMPLE IMPLEMENTATION
def cat_1():
    while True:
        yield random_english_text(97)
def cat_2():
    while True:
        yield random_enciphered_text(97)
def cat_3():
    while True:
        yield random_skip_text(97)
def test_1(in_string):
    return in_string.count('E')
def test_2(in_string):
    return in_string.count('TH')
def test_3(in_string):
    return index_of_coincidence(in_string)


while True:
    # ERROR - often classifies english as transposition
    case_eng = random_english_text(97)
    case_vig = random_enciphered_text(97)
    case_skp = random_skip_text(97)
    case = random.choice([case_eng, case_vig, case_skp])
    print(case)
    classified_idx = ml.classify(case, [cat_1(), cat_2(), cat_3()], [test_1,
                                 test_2, test_3])
    print("APPEARS TO BE...")
    d_categories = {0: 'ENGLISH', 1:'VIGNERE', 2:'TRANSPOSITION'}
    print(d_categories[classified_idx])
    input()
