import statistics
import random


# TODO machine that invents new properties to test

def run_several_tests(f_test, g_samples, n_samples = 1000):
    """Applies test to samples and outputs iterable of results."""
    # TODO needs better name
    # n_samples works as a cutoff for infinite generators
    # TODO if n_samples == None then ignore it?
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
        # TODO fix this hack. how should we calculate a CI if the sample is all
        # exactly the same? how unexpected should a new result be?
        EPSILON = 0.001
        if sd == 0:
            sd += EPSILON
        deviation = abs(m - case_result) / sd
        deviations.append(deviation)
    return statistics.mean(deviations)


def classify(case, categories, tests, verbose=False):
    """Estimates which category a particular case falls in.

    Takes a sample of data (case) and applies functions in iterable
    (tests), comparing those results to the results of applying the same
    tests to the generators found in iterable of generators
    (categories), returning either the most likely category, or in
    verbose mode, a list of tuples with (generator, normalized rating)
    for each.
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

    # score case against category results using compare_results
    category_scores = []
    for c in categories:
        score = compare_results(case_results, results[c])
        category_scores.append(score)
    best_fit_idx = category_scores.index(min(category_scores))
    if verbose:
        return category_scores
    else:
        return best_fit_idx  # Or return categories[best_fit_index] ?


def main():
    pass


if __name__ == '__main__':
    main()
