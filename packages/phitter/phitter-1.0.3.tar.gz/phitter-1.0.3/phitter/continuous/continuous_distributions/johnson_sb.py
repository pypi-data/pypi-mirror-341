import numpy
import scipy.integrate
import scipy.stats


class JohnsonSB:
    """
    Johnson SB distribution
    - Parameters JohnsonSB Distribution: {"xi": *, "lambda": *, "gamma": *, "delta": *}
    - https://phitter.io/distributions/continuous/johnson_sb
    """

    def __init__(
        self,
        parameters: dict[str, int | float] = None,
        continuous_measures=None,
        init_parameters_examples=False,
    ):
        """
        - Initializes the JohnsonSB Distribution by either providing a Continuous Measures instance [ContinuousMeasures] or a dictionary with the distribution's parameters.
        - Parameters JohnsonSB Distribution: {"xi": *, "lambda": *, "gamma": *, "delta": *}
        - https://phitter.io/distributions/continuous/johnson_sb
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

        self.xi_ = self.parameters["xi"]
        self.lambda_ = self.parameters["lambda"]
        self.gamma_ = self.parameters["gamma"]
        self.delta_ = self.parameters["delta"]

    @property
    def name(self):
        return "johnson_sb"

    @property
    def parameters_example(self) -> dict[str, int | float]:
        return {"xi": 102, "lambda": 794, "gamma": 4, "delta": 1}

    def cdf(self, x: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Cumulative distribution function
        """
        # z = lambda t: (t - self.xi_) / self.lambda_
        # result = scipy.stats.norm.cdf(self.gamma_ + self.delta_ * numpy.log(z(x) / (1 - z(x))))
        result = scipy.stats.johnsonsb.cdf(x, self.gamma_, self.delta_, loc=self.xi_, scale=self.lambda_)
        return result

    def pdf(self, x: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Probability density function
        """
        # z = lambda t: (t - self.xi_) / self.lambda_
        # result = (self.delta_ / (self.lambda_ * numpy.sqrt(2 * numpy.pi) * z(x) * (1 - z(x)))) * numpy.exp(-(1 / 2) * (self.gamma_ + self.delta_ * numpy.log(z(x) / (1 - z(x)))) ** 2)
        result = scipy.stats.johnsonsb.pdf(x, self.gamma_, self.delta_, loc=self.xi_, scale=self.lambda_)
        return result

    def ppf(self, u: float | numpy.ndarray) -> float | numpy.ndarray:
        """
        Percent point function. Inverse of Cumulative distribution function. If CDF[x] = u => PPF[u] = x
        """
        # result = (self.lambda_ * numpy.exp((scipy.stats.norm.ppf(u) - self.gamma_) / self.delta_)) / (1 + numpy.exp((scipy.stats.norm.ppf(u) - self.gamma_) / self.delta_)) + self.xi_
        result = scipy.stats.johnsonsb.ppf(u, self.gamma_, self.delta_, loc=self.xi_, scale=self.lambda_)
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
        f = lambda x: x**k * (self.delta_ / (numpy.sqrt(2 * numpy.pi) * x * (1 - x))) * numpy.exp(-(1 / 2) * (self.gamma_ + self.delta_ * numpy.log(x / (1 - x))) ** 2)
        return scipy.integrate.quad(f, 0, 1)[0]

    def central_moments(self, k: int) -> float | None:
        """
        Parametric central moments. µ'[k] = E[(X - E[X])ᵏ] = ∫(x-µ[k])ᵏ∙f(x) dx
        """
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        µ3 = self.non_central_moments(3)
        µ4 = self.non_central_moments(4)

        if k == 1:
            return 0
        if k == 2:
            return µ2 - µ1**2
        if k == 3:
            return µ3 - 3 * µ1 * µ2 + 2 * µ1**3
        if k == 4:
            return µ4 - 4 * µ1 * µ3 + 6 * µ1**2 * µ2 - 3 * µ1**4

        return None

    @property
    def mean(self) -> float:
        """
        Parametric mean
        """
        µ1 = self.non_central_moments(1)
        return self.xi_ + self.lambda_ * µ1

    @property
    def variance(self) -> float:
        """
        Parametric variance
        """
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        return self.lambda_ * self.lambda_ * (µ2 - µ1**2)

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
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        central_µ3 = self.central_moments(3)
        return central_µ3 / (µ2 - µ1**2) ** 1.5

    @property
    def kurtosis(self) -> float:
        """
        Parametric kurtosis
        """
        µ1 = self.non_central_moments(1)
        µ2 = self.non_central_moments(2)
        central_µ4 = self.central_moments(4)
        return central_µ4 / (µ2 - µ1**2) ** 2

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
        return None

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
        v1 = self.delta_ > 0
        v2 = self.lambda_ > 0
        return v1 and v2

    def get_parameters(self, continuous_measures) -> dict[str, float | int]:
        """
        Calculate proper parameters of the distribution from sample continuous_measures.
        The parameters are calculated with the method proposed in [1].

        Parameters
        ==========
        continuous_measures: MEASUREMESTS
            attributes: mean, std, variance, skewness, kurtosis, median, mode, min, max, size, num_bins, data

        Returns
        =======
        parameters: {"xi": *, "lambda": *, "gamma": *, "delta": *}
            {"xi": * , "lambda": * , "gamma": * , "delta": * }

        References
        ==========
        .. [1] George, F., & Ramachandran, K. M. (2011).
               Estimation of parameters of Johnson's system of distributions.
               Journal of Modern Applied Statistical Methods, 10(2), 9.
        """
        # ## Percentiles
        # z = 0.5384

        # # Usar numpy para calcular percentiles
        # percentiles = scipy.stats.norm.cdf(z * numpy.array([-3, -1, 1, 3]))
        # scores = numpy.percentile(continuous_measures.data, 100 * percentiles)

        # x1, x2, x3, x4 = scores

        # ## Cálculo de m, n, p
        # m = x4 - x3
        # n = x2 - x1
        # p = x3 - x2

        # ## Cálculo de los parámetros de distribución
        # p_squared = p ** 2
        # m_n_product = m * n
        # term = (p_squared / m_n_product - 1)

        # lambda_ = (p * numpy.sqrt((((1 + p / m) * (1 + p / n) - 2) ** 2 - 4))) / term
        # xi_ = 0.5 * (x3 + x2) - 0.5 * lambda_ + p * (p / n - p / m) / (2 * term)
        # delta_ = z / numpy.arccosh(0.5 * numpy.sqrt((1 + p / m) * (1 + p / n)))
        # gamma_ = delta_ * numpy.arcsinh((p / n - p / m) * numpy.sqrt((1 + p / m) * (1 + p / n) - 4) / (2 * term))

        # parameters = {"xi": xi_, "lambda": lambda_, "gamma": gamma_, "delta": delta_}

        ## Scipy parameters
        scipy_parameters = scipy.stats.johnsonsb.fit(continuous_measures.data_to_fit)
        parameters = {"xi": scipy_parameters[2], "lambda": scipy_parameters[3], "gamma": scipy_parameters[0], "delta": scipy_parameters[1]}
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
    path = "../continuous_distributions_sample/sample_johnson_sb.txt"
    data = get_data(path)
    continuous_measures = ContinuousMeasures(data)
    distribution = JohnsonSB(continuous_measures=continuous_measures)

    print(f"{distribution.name} distribution")
    print(f"Parameters: {distribution.parameters}")
    print(f"CDF: {distribution.cdf(continuous_measures.mean)} {distribution.cdf(numpy.array([continuous_measures.mean, continuous_measures.mean]))}")
    print(f"PDF: {distribution.pdf(continuous_measures.mean)} {distribution.pdf(numpy.array([continuous_measures.mean, continuous_measures.mean]))}")
    print(f"PPF: {distribution.ppf(0.5)} {distribution.ppf(numpy.array([0.5, 0.5]))} - V: {distribution.cdf(distribution.ppf(0.5))}")
    print(f"SAMPLE: {distribution.sample(5)}")
    print(f"\nSTATS")
    print(f"mean: {distribution.mean} - {continuous_measures.mean}")
    print(f"variance: {distribution.variance} - {continuous_measures.variance}")
    print(f"skewness: {distribution.skewness} - {continuous_measures.skewness}")
    print(f"kurtosis: {distribution.kurtosis} - {continuous_measures.kurtosis}")
    print(f"median: {distribution.median} - {continuous_measures.median}")
    print(f"mode: {distribution.mode} - {continuous_measures.mode}")
