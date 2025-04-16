import numpy
import scipy.stats


class Binomial:
    """
    Binomial distribution
    - Parameters Binomial Distribution: {"n": *, "p": *}
    - https://phitter.io/distributions/discrete/binomial
    """

    def __init__(
        self,
        parameters: dict[str, int | float] = None,
        discrete_measures=None,
        init_parameters_examples=False,
    ):
        """
        - Initializes the Binomial Distribution by either providing a Discrete Measures instance [DiscreteMeasures] or a dictionary with the distribution's parameters.
        - Parameters Binomial Distribution: {"n": *, "p": *}
        - https://phitter.io/distributions/continuous/binomial
        """
        if discrete_measures is None and parameters is None and init_parameters_examples == False:
            raise Exception("You must initialize the distribution by either providing the Discrete Measures [DiscreteMeasures] instance or a dictionary of the distribution's parameters.")
        if discrete_measures != None:
            self.parameters = self.get_parameters(discrete_measures=discrete_measures)
        if parameters != None:
            self.parameters = parameters
        if init_parameters_examples:
            self.parameters = self.parameters_example

        self.n = self.parameters["n"]
        self.p = self.parameters["p"]

    @property
    def name(self):
        return "binomial"

    @property
    def parameters_example(self) -> dict[str, int | float]:
        return {"n": 10, "p": 0.6994}

    def cdf(self, x: int | numpy.ndarray) -> float | numpy.ndarray:
        """
        Cumulative distribution function
        """
        result = scipy.stats.binom.cdf(x, self.n, self.p)
        return result

    def pmf(self, x: int | numpy.ndarray) -> float | numpy.ndarray:
        """
        Probability mass function
        """
        # result = scipy.special.comb(self.n, x) * (self.p**x) * ((1 - self.p) ** (self.n - x))
        result = scipy.stats.binom.pmf(x, self.n, self.p)
        return result

    def ppf(self, u: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Percent point function. Inverse of Cumulative distribution function. If CDF[x] = u => PPF[u] = x
        """
        result = scipy.stats.binom.ppf(u, self.n, self.p)
        return result

    def sample(self, n: int, seed: int | None = None) -> numpy.ndarray:
        """
        Sample of n elements of ditribution
        """
        if seed:
            numpy.random.seed(seed)
        return self.ppf(numpy.random.rand(n))

    def non_central_moments(self, k: int) -> float | None:
        """
        Parametric no central moments. µ[k] = E[Xᵏ] = ∫xᵏ∙f(x) dx
        """
        return None

    def central_moments(self, k: int) -> float | None:
        """
        Parametric central moments. µ'[k] = E[(X - E[X])ᵏ] = ∫(x-µ[k])ᵏ∙f(x) dx
        """
        return None

    @property
    def mean(self) -> float:
        """
        Parametric mean
        """
        return self.n * self.p

    @property
    def variance(self) -> float:
        """
        Parametric variance
        """
        return self.n * self.p * (1 - self.p)

    @property
    def standard_deviation(self) -> float:
        """
        Parametric standard deviation
        """
        return numpy.sqrt(self.variance)

    @property
    def skewness(self) -> float:
        """
        Parametric skewness
        """
        return (1 - self.p - self.p) / numpy.sqrt(self.n * self.p * (1 - self.p))

    @property
    def kurtosis(self) -> float:
        """
        Parametric kurtosis
        """
        return (1 - 6 * self.p * (1 - self.p)) / (self.n * self.p * (1 - self.p)) + 3

    @property
    def median(self) -> float:
        """
        Parametric median
        """
        return self.ppf(0.5)

    @property
    def mode(self) -> float:
        """
        Parametric mode
        """
        return numpy.floor(self.p * (self.n + 1))

    @property
    def num_parameters(self) -> int:
        """
        Number of parameters of the distribution
        """
        return len(self.parameters)

    def parameter_restrictions(self) -> bool:
        """
        Check parameters restrictions
        """
        v1 = 0 < self.p < 1
        v2 = self.n > 0
        v3 = type(self.n) == int
        return v1 and v2 and v3

    def get_parameters(self, discrete_measures) -> dict[str, float | int]:
        """
        Calculate proper parameters of the distribution from sample discrete_measures.
        The parameters are calculated by formula.

        Parameters
        ==========
        discrete_measures: MEASUREMESTS
            attributes: mean, std, variance, skewness, kurtosis, median, mode, min, max, size, num_bins, data

        Returns
        =======
        parameters: {"n": *, "p": *}
        """
        p = 1 - discrete_measures.variance / discrete_measures.mean
        n = int(round(discrete_measures.mean / p, 0))
        parameters = {"n": n, "p": p}
        return parameters


if __name__ == "__main__":
    import sys

    sys.path.append("../")
    from discrete_measures import DiscreteMeasures

    ## Import function to get discrete_measures
    def get_data(path: str) -> list[int]:
        sample_distribution_file = open(path, "r")
        data = [int(x) for x in sample_distribution_file.read().splitlines()]
        sample_distribution_file.close()
        return data

    ## Distribution class
    path = "../discrete_distributions_sample/sample_binomial.txt"
    data = get_data(path)
    discrete_measures = DiscreteMeasures(data)
    distribution = Binomial(discrete_measures=discrete_measures)

    print(f"{distribution.name} distribution")
    print(f"Parameters: {distribution.parameters}")
    print(f"CDF: {distribution.cdf(int(discrete_measures.mean))} {distribution.cdf(numpy.array([int(discrete_measures.mean), int(discrete_measures.mean)]))}")
    print(f"PMF: {distribution.pmf(int(discrete_measures.mean))} {distribution.pmf(numpy.array([int(discrete_measures.mean), int(discrete_measures.mean)]))}")
    print(f"PPF: {distribution.ppf(0.5)} {distribution.ppf(numpy.array([0.5, 0.5]))} - V: {distribution.cdf(distribution.ppf(0.5))}")
    print(f"SAMPLE: {distribution.sample(5)}")
    print(f"\nSTATS")
    print(f"mean: {distribution.mean} - {discrete_measures.mean}")
    print(f"variance: {distribution.variance} - {discrete_measures.variance}")
    print(f"skewness: {distribution.skewness} - {discrete_measures.skewness}")
    print(f"kurtosis: {distribution.kurtosis} - {discrete_measures.kurtosis}")
    print(f"median: {distribution.median} - {discrete_measures.median}")
    print(f"mode: {distribution.mode} - {discrete_measures.mode}")
