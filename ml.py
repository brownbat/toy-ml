import statistics
import random


def run_several_tests(f_test, g_samples, n_samples):
    """Applies test to samples and outputs iterable of results."""
    # TODO needs better name
    # TODO if n_samples == None then ignore it
    for s, i in zip(g_samples, range(n_samples)):
        yield f_test(s)


def compare_results(case_results, category_results):
    """Scores similarity of case_results to category_results.

    Averages difference between each case result and average category
    result measured by standard deviations for that particular test.
    """
    # TODO use actual confidence interval forumla after figuring out how
    # statisticians actually do this, instead of just making up my own
    deviations = []
    for test in case_results.keys():
        category_result = category_results[test]
        case_result = case_results[test]
        m = statistics.mean(category_result)
        sd = statistics.stdev(category_result, m)
        # TODO fix this hack. how can i calculate a CI if my sample is all
        # exactly the same? how unexpected would a new result be?
        if sd == 0:
            sd = 0.00001
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
    case_results = {}
    for c in categories:
        results[c] = {}
    for t in tests:
        for c in categories:
            # TODO make these generators that can be run later
            results[c][t] = list(run_several_tests(t, c, n_samples=PRECISION))
        case_results[t] = t(case)

    # TODO score case against category results using compare_results
    category_scores = []
    for c in categories:
        # TODO breaks here -- make sure data structures are
        # consistent
        score = compare_results(case_results, results[c])
        category_scores.append(score)
    best_fit_idx = category_scores.index(min(category_scores))
    if verbose:
        return category_scores
    else:
        return best_fit_idx  # Or return categories[best_fit_index] ?


def cat_1():
    """Returns a five-character string of sequential capital letters."""
    while True:
        c = random.randint(0, 21)
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


def test_3(a, normalized=True):
    """Returns number of simple vowels."""
    count = 0
    for i in a:
        if i in 'AEIOU':
            count += 1
    if normalized:
        return count // len(a)
    else:
        return count


def main():
    # Here it correctly identifies 'BCDEF' as an example in the category of
    # words that are sequentially alphabetic, as opposed to random letters.
    case = 'BCDEF'
    print(classify(case, [cat_1(), cat_2()], [test_1, test_2, test_3],
          verbose=True))
    print(classify(case, [cat_1(), cat_2()], [test_1, test_2, test_3]))


if __name__ == '__main__':
    main()
