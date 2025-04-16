import numpy
import scipy.stats


def evaluate_continuous_test_chi_square(distribution, continuous_measures):
    """
    Chi Square test to evaluate that a sample is distributed according to a probability
    distribution.

    The hypothesis that the sample is distributed following the probability distribution
    is not rejected if the test statistic is less than the critical value or equivalently
    if the p-value is less than 0.05

    Parameters
    ==========
    data: iterable
        data set
    distribution: class
        distribution class initialized whit parameters of distribution and methods
        cdf() and num_parameters()

    Return
    ======
    result_test_chi2: dict
        1. test_statistic(float):
            sum over all classes of the value (expected - observed) ^ 2 / expected
        2. critical_value(float):
            inverse of the distribution chi square to 0.95 with freedom degrees
            n - 1 minus the number of parameters of the distribution.
        3. p-value([0,1]):
            right - tailed probability of the test statistic for the chi - square distribution
            with the same degrees of freedom as for the critical value calculation.
        4. rejected(bool):
            decision if the null hypothesis is rejected. If it is false, it can be
            considered that the sample is distributed according to the probability
            distribution. If it's true, no.
    """

    ## Parameters and preparations
    N = continuous_measures.size
    freedom_degrees = max(continuous_measures.num_bins - 1 - distribution.num_parameters, 1)

    ## Calculation of errors
    expected_values = N * (distribution.cdf(continuous_measures.bin_edges[1:]) - distribution.cdf(continuous_measures.bin_edges[:-1]))
    errors = ((continuous_measures.absolutes_frequencies - expected_values) ** 2) / expected_values

    ## Calculation of indicators
    statistic_chi2 = numpy.sum(errors)
    critical_value = continuous_measures.critical_value_chi2(freedom_degrees)
    p_value = 1 - scipy.stats.chi2.cdf(statistic_chi2, freedom_degrees)
    rejected = statistic_chi2 >= critical_value

    ## Construction of answer
    result_test_chi2 = {
        "test_statistic": statistic_chi2,
        "critical_value": critical_value,
        "p-value": p_value,
        "rejected": rejected,
    }
    return result_test_chi2


if __name__ == "__main__":
    import sys

    sys.path.append("../")
    from continuous_distributions import CONTINUOUS_DISTRIBUTIONS
    from continuous_measures import ContinuousMeasures

    def get_data(path: str) -> list[float]:
        sample_distribution_file = open(path, "r")
        data = [float(x.replace(",", ".")) for x in sample_distribution_file.read().splitlines()]
        sample_distribution_file.close()
        return data

    for id_distribution, distribution_class in CONTINUOUS_DISTRIBUTIONS.items():
        print(id_distribution)
        path = f"../continuous_distributions_sample/sample_{id_distribution}.txt"
        data = get_data(path)

        ## Init a instance of class
        continuous_measures = ContinuousMeasures(data)
        distribution = distribution_class(continuous_measures=continuous_measures)
        print(evaluate_continuous_test_chi_square(distribution, continuous_measures))
