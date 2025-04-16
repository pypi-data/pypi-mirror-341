import numpy
import scipy.special
import scipy.stats


class TStudent3P:
    """
    T distribution
    - Parameters TStudent3P Distribution: {"df": *, "loc": *, "scale": *}
    - https://phitter.io/distributions/continuous/t_student_3p
    """

    def __init__(
        self,
        parameters: dict[str, int | float] = None,
        continuous_measures=None,
        init_parameters_examples=False,
    ):
        """
        - Initializes the TStudent3P Distribution by either providing a Continuous Measures instance [ContinuousMeasures] or a dictionary with the distribution's parameters.
        - Parameters TStudent3P Distribution: {"df": *, "loc": *, "scale": *}
        - https://phitter.io/distributions/continuous/t_student_3p
        """
        if continuous_measures is None and parameters is None and init_parameters_examples == False:
            raise ValueError(
                "You must initialize the distribution by providing one of the following: distribution parameters, a Continuous Measures [ContinuousMeasures] instance, or by setting init_parameters_examples to True."
            )
        if continuous_measures != None:
            self.parameters = self.get_parameters(continuous_measures=continuous_measures)
        if parameters != None:
            self.parameters = parameters
        if init_parameters_examples:
            self.parameters = self.parameters_example

        self.df = self.parameters["df"]
        self.loc = self.parameters["loc"]
        self.scale = self.parameters["scale"]

    @property
    def name(self):
        return "t_student_3p"

    @property
    def parameters_example(self) -> dict[str, int | float]:
        return {"df": 15, "loc": 100, "scale": 3}

    def cdf(self, x: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Cumulative distribution function
        """
        # z = lambda t: (t - self.loc) / self.scale
        # result = scipy.special.betainc(self.df / 2, self.df / 2, (z(x) + numpy.sqrt(z(x) ** 2 + self.df)) / (2 * numpy.sqrt(z(x) ** 2 + self.df)))
        result = scipy.stats.t.cdf(x, self.df, loc=self.loc, scale=self.scale)
        return result

    def pdf(self, x: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Probability density function
        """
        # z = lambda t: (t - self.loc) / self.scale
        # result = (1 / (numpy.sqrt(self.df) * scipy.special.beta(0.5, self.df / 2))) * (1 + z(x) * z(x) / self.df) ** (-(self.df + 1) / 2)
        result = scipy.stats.t.pdf(x, self.df, loc=self.loc, scale=self.scale)
        return result

    def ppf(self, u):
        # result = self.loc + self.scale * numpy.sign(u - 0.5) * numpy.sqrt(
        #     self.df * (1 - scipy.special.betaincinv(self.df / 2, 0.5, 2 * numpy.min([u, 1 - u]))) / scipy.special.betaincinv(self.df / 2, 0.5, 2 * numpy.min([u, 1 - u]))
        result = scipy.stats.t.ppf(u, self.df, loc=self.loc, scale=self.scale)
        # )
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
        return self.loc

    @property
    def variance(self) -> float:
        """
        Parametric variance
        """
        return (self.scale * self.scale * self.df) / (self.df - 2)

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
        return 0

    @property
    def kurtosis(self) -> float:
        """
        Parametric kurtosis
        """
        return 6 / (self.df - 4) + 3

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
        return self.loc

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
        v1 = self.df > 0
        v2 = self.scale > 0
        return v1 and v2

    def get_parameters(self, continuous_measures) -> dict[str, float | int]:
        """
        Calculate proper parameters of the distribution from sample continuous_measures.
        The parameters are calculated by solving the equations of the measures expected
        for this distribution.The number of equations to consider is equal to the number
        of parameters.

        Parameters
        ==========
        continuous_measures: MEASUREMESTS
            attributes: mean, std, variance, skewness, kurtosis, median, mode, min, max, size, num_bins, data

        Returns
        =======
        parameters: {"df": *, "loc": *, "scale": *}
        """
        ## Scipy parameters
        scipy_parameters = scipy.stats.t.fit(continuous_measures.data_to_fit)
        parameters = {"df": scipy_parameters[0], "loc": scipy_parameters[1], "scale": scipy_parameters[2]}

        # loc = continuous_measures.mean
        # df = 4 + 6 / (continuous_measures.kurtosis - 3)
        # scale = numpy.sqrt(continuous_measures.variance * (df + 2) / df)
        # parameters = {"df": df, "loc": loc, "scale": scale}
        return parameters


if __name__ == "__main__":
    import sys

    sys.path.append("../")
    from continuous_measures import ContinuousMeasures

    ## Import function to get continuous_measures
    def get_data(path: str) -> list[float]:
        sample_distribution_file = open(path, "r")
        data = [float(x.replace(",", ".")) for x in sample_distribution_file.read().splitlines()]
        sample_distribution_file.close()
        return data

    ## Distribution class
    path = "../continuous_distributions_sample/sample_t_student_3p.txt"
    data = get_data(path)
    continuous_measures = ContinuousMeasures(data)
    distribution = TStudent3P(continuous_measures=continuous_measures)

    print(f"{distribution.name} distribution")
    print(f"Parameters: {distribution.parameters}")
    print(f"CDF: {distribution.cdf(continuous_measures.mean)} {distribution.cdf(numpy.array([continuous_measures.mean, continuous_measures.mean]))}")
    print(f"PDF: {distribution.pdf(continuous_measures.mean)} {distribution.pdf(numpy.array([continuous_measures.mean, continuous_measures.mean]))}")
    print(f"PPF: {distribution.ppf(0.5)} {distribution.ppf(numpy.array([0.3, 0.7]))} - V: {distribution.cdf(distribution.ppf(0.5))}")
    print(f"SAMPLE: {distribution.sample(5)}")
    print(f"\nSTATS")
    print(f"mean: {distribution.mean} - {continuous_measures.mean}")
    print(f"variance: {distribution.variance} - {continuous_measures.variance}")
    print(f"skewness: {distribution.skewness} - {continuous_measures.skewness}")
    print(f"kurtosis: {distribution.kurtosis} - {continuous_measures.kurtosis}")
    print(f"median: {distribution.median} - {continuous_measures.median}")
    print(f"mode: {distribution.mode} - {continuous_measures.mode}")
