import statistics
import random

def run_several_tests(f_test, g_samples, n_samples):
    """Applies test to samples and outputs iterable of results."""
    # TODO needs better name
    for s, i in zip(g_samples, range(n_samples)):
        yield f_test(s)


def compare_results(case_results, category_results):
    """Scores similarity of case_results to category_results.

    Averages difference between each case result and average category
    result measured by standard deviations for that particular test.
    """
    assert len(case_results) == len(category_results)
    deviations = []
    for case_result, category_result in zip(case_results, category_results):
        m = statistics.mean(category_result)
        sd = statistics.stdev(category_result, m)
        deviation = abs(m - case_result) / sd
        deviations.append(deviation)
    return statistics.mean(deviations)

def classify(case, categories, tests, verbose=False):
    """Estimates which category a particular case falls in.

    Takes a sample of data case and applies functions in iterable
    tests comparing results to outcomes of applying tests to generators
    found in iterable of generators categories, returning either the
    most likely category, or in verbose mode, a list of tuples with
    (generator, normalized rating) for each.
    """
    # You might want a label on the individual generators in categories
    # or tests, but these internals don't need that so just have callers
    # track names and strip them for this function.

    # TODO intelligently determine when to stop sampling using optimal
    # stopping theory. For now we just specify number of samples
    # explicitly with PRECISION
    PRECISION = 10
    results = {}
    case_results = []
    for c in categories:
        results[c] = []
    for t in tests:
        for c in categories:
            #TODO make these generators that can be run later
            results[c].append(list(run_several_tests(t, c, n_samples=PRECISION)))
        case_results.append(t(case))

    # TODO score case against category results using compare_results
    category_scores = []
    for c in categories:
        print('case results')
        print(case_results)
        print('cat results ')
        print(results[c])
        input()
        score = compare_results(case_results, results[c])
        category_scores.append(score)
    best_fit_idx = category_scores.index(min(category_scores))
    if verbose:
        return category_scores
    else:
        return best_fit_idx # Or return categories[best_fit_index] ?

def cat_1():
    """Returns a five-character string of sequential capital letters."""
    while True:
        c = random.randint(0,21)
        s = ''
        for i in range(5):
            s += chr(ord('A') + c + i)
        yield s

def cat_2():
    """Returns a five-character string of random capital letters."""
    while True:
        s = ''
        for i in range(5):
            a = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            s += a
        yield s
        
def test_1(a):
    """Returns 1 if second letter is one higher than first."""
    if ord(a[0]) == ord(a[1]) - 1:
        return 1
    else:
        return 0

def test_2(a):
    """Returns 1 if third letter is two higher than first."""
    if ord(a[0]) == ord(a[2]) - 2:
        return 1
    else:
        return 0

def main():
    case = 'BCDEF'
    print(classify(case, [cat_1(), cat_2()], [test_1, test_2], verbose=True))

if __name__ == '__main__':
    main()
