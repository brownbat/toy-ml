def run_several_tests(f_test, g_samples, n_samples):
    """Applies test to samples and outputs iterable of results."""
    # TODO needs better name
    for i in range(n_samples):
        for s in g_samples:
            yield f_test(s)

def compare_results(case_results, category_results):
    """Scores similarity of case_results to category_results.

    Averages difference between each case result and average category
    result measured by standard deviations for that particular test.
    """
    pass

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
    PRECISION = 1000
    results = {}
    case_results = []
    for t in tests:
        for c in categories:
            results[c] = {}
            results[c][t] = list(run_several_tests(t, c, n_samples=PRECISION))
        case_results.append(t(case))

    # TODO score case against category results using compare_results
    # return list of scores if verbose
    # or if not verbose just return highest rated match


def main():
    pass


if __name__ == '__main__':
    main()
