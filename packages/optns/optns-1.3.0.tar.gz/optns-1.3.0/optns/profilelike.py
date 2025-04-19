"""Profile likelihoods."""
import numpy as np
from numpy import exp, log
from scipy.optimize import minimize
from scipy.stats import multivariate_normal, norm
from sklearn.linear_model import LinearRegression


def unique_components(X, tol=1e-12):
    """Identify components.

    Returns a boolean mask where each entry is True if the corresponding column
    in X is different from all previous columns.

    Parameters
    ----------
    X: array
        transposed list of the model component vectors.
    tol: float
        tolerance for comparing components

    Returns
    -------
    mask: array
        boolean mask of shape X.shape[1]
    """
    n_cols = X.shape[1]
    mask = np.ones(n_cols, dtype=bool)
    for i in range(1, n_cols):
        for j in range(i):
            if mask[j] and np.allclose(X[:, i], X[:, j], atol=tol, rtol=0):
                mask[i] = False
                break
    return mask


def poisson_negloglike(lognorms, X, counts):
    """Compute negative log-likelihood of a Poisson distribution.

    Parameters
    ----------
    lognorms: array
        logarithm of normalisations
    X: array
        transposed list of the model component vectors.
    counts: array
        non-negative integers giving the observed counts.

    Returns
    -------
    negloglike: float
        negative log-likelihood, neglecting the `1/fac(counts)` constant.
    """
    lam = exp(lognorms) @ X.T
    loglike = counts * log(lam) - lam
    return -loglike.sum()


def poisson_negloglike_grad(lognorms, X, counts):
    """Compute gradient of negative log-likelihood of a Poisson distribution.

    Parameters
    ----------
    lognorms: array
        logarithm of normalisations
    X: array
        transposed list of the model component vectors.
    counts: array
        non-negative integers giving the observed counts.

    Returns
    -------
    grad: array
        vector of gradients
    """
    norms = np.exp(lognorms)
    lam = norms @ X.T
    diff = 1 - counts / lam
    grad = (diff @ X) * norms
    return grad


def poisson_laplace_approximation(lognorms, X):
    """Compute mean and covariance corresponding to Poisson likelihood.

    Parameters
    ----------
    lognorms: array
        logarithm of normalisations
    X: array
        transposed list of the model component vectors.

    Returns
    -------
    grad: array
        vector of gradients
    """
    mean = exp(lognorms)
    lambda_hat = mean @ X.T
    D = np.diag(1 / lambda_hat)
    # Compute the Fisher Information Matrix
    FIM = X.T @ D @ X
    covariance = np.linalg.inv(FIM)
    return mean, covariance


def poisson_initial_guess(X, counts, epsilon=0.1, minnorm=1e-50):
    """Guess component normalizations from counts.

    Based on weighted least squares, with zero counts adjusted.

    Parameters
    ----------
    X: array
        transposed list of the model component vectors.
    counts: array
        non-negative integers giving the observed counts.
    epsilon: float
        small number to add to counts to avoid zeros.
    minnorm: float
        smallest allowed normalisation

    Returns
    -------
    lognorms: array
        logarithm of normalisations
    """
    y = counts + epsilon
    W = np.diag(1.0 / y)
    # Weighted least squares: N = (X^T W X)^(-1) X^T W y
    XtW = X.T @ W
    A = XtW @ X
    b = XtW @ y
    # least-squares solve
    N0 = np.linalg.lstsq(A, b, rcond=None)[0]
    return np.log(np.clip(N0, 0, None) + minnorm)


class ComponentModel:
    """Generalized Additive Model.

    Defines likelihoods for observed data,
    given arbitrary components which are
    linearly added with non-negative normalisations.
    """

    def __init__(self, Ncomponents, flat_data, flat_invvar=None, positive=True):
        """Initialise.

        Parameters
        ----------
        Ncomponents: int
            number of model components
        flat_data: array
            array of observed data. For the Poisson likelihood functions,
            must be non-negative integers.
        flat_invvar: None|array
            For the Poisson likelihood functions, None.
            For the Gaussian likelihood function, the inverse variance,
            `1 / (standard_deviation)^2`, where standard_deviation
            are the measurement uncertainties.
        positive: bool
            whether Gaussian normalisations must be positive.
        """
        (self.Ndata,) = flat_data.shape
        self.flat_data = flat_data
        if not np.isfinite(self.flat_data).all():
            raise AssertionError("Invalid data, not finite numbers.")
        self.flat_invvar = flat_invvar
        if self.flat_invvar is not None:
            self.invvar_matrix = np.diag(self.flat_invvar)
        self.Ncomponents = Ncomponents
        self.poisson_guess_data_offset = 0.1
        self.poisson_guess_model_offset = 1e-50
        self.minimize_kwargs = dict(method="L-BFGS-B", options=dict(ftol=1e-10, maxfun=10000))
        self.cond_threshold = 1e6
        self.poisson_cov_diagonal = 1e-10
        self.positive = positive
        self.gauss_reg = LinearRegression(positive=self.positive, fit_intercept=False)

    def loglike_poisson_optimize(self, component_shapes):
        """Optimize the normalisations assuming a Poisson Additive Model.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.

        Returns
        -------
        res: scipy.optimize.OptimizeResult
            return value of `scipy.optimize.minimize`
        """
        assert component_shapes.shape == (self.Ndata, self.Ncomponents), (
            component_shapes.shape,
            (self.Ndata, self.Ncomponents),
        )
        X = component_shapes
        assert np.isfinite(X).all()
        if not np.any(X > 0, axis=1).all():
            raise AssertionError("In portions of the data set, all component shapes are zero. Problem is ill-defined.")
        if not np.any(X > 0, axis=0).all():
            raise AssertionError(f"Some components are exactly zero everywhere, so normalisation is ill-defined. Components: {np.any(X > 0, axis=0)}.")
        if self.positive and not np.all(X >= 0):
            raise AssertionError(f"Components must not be negative. Components: {~np.all(X >= 0, axis=0)}")
        y = self.flat_data
        mask_unique = unique_components(X)
        x0 = poisson_initial_guess(X[:,mask_unique], y, self.poisson_guess_data_offset, self.poisson_guess_model_offset)
        assert np.isfinite(x0).all(), (x0, y, X, mask_unique)
        res = minimize(
            poisson_negloglike, x0, args=(X[:,mask_unique], y),
            jac=poisson_negloglike_grad,
            **self.minimize_kwargs)
        xfull = np.zeros(len(mask_unique)) + -1e50
        xfull[mask_unique] = res.x
        res.x = xfull
        return res

    def loglike_poisson(self, component_shapes):
        """Return profile likelihood.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.

        Returns
        -------
        loglike: float
            log-likelihood
        """
        res = self.loglike_poisson_optimize(component_shapes)
        if not res.success:
            # give penalty when ill-defined
            return -1e100
        return -res.fun

    def norms_poisson(self, component_shapes):
        """Return optimal normalisations.

        Normalisations of subsequent identical components will be zero.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.

        Returns
        -------
        norms: array
            normalisations, one value for each model component.
        """
        res = self.loglike_poisson_optimize(component_shapes)
        return exp(res.x)

    def sample_poisson(self, component_shapes, size, rng=np.random):
        """Sample from Poisson likelihood function.

        Sampling occurs with importance sampling,
        so the results need to be weighted by
        `exp(loglike_target-loglike_proposal)`
        or rejection sampled.


        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.
        size: int
            Maximum number of samples to generate.
        rng: object
            Random number generator

        Returns
        -------
        samples: array
            list of sampled normalisations. May be fewer than
            `size`, because negative normalisations are discarded
            if ComponentModel was initialized with positive=True.
        loglike_proposal: array
            for each sample, the importance sampling log-probability
        loglike_target: array
            for each sample, the Poisson log-likelihood
        """
        res = self.loglike_poisson_optimize(component_shapes)
        X = component_shapes
        profile_loglike = -res.fun
        assert np.isfinite(profile_loglike), res
        # get mean
        counts = self.flat_data
        mean, covariance = poisson_laplace_approximation(res.x, X)
        try:
            rv = multivariate_normal(mean, covariance)
            samples_all = rv.rvs(size=size, random_state=rng).reshape((size, len(mean)))
            rv_logpdf = rv.logpdf
        except np.linalg.LinAlgError:
            stdev = np.diag(covariance)**0.5
            rv = norm(mean, stdev)
            samples_all = rng.normal(mean, stdev, size=(size, len(mean))).reshape((size, len(mean)))

            def rv_logpdf(x):
                return rv.logpdf(x).sum(axis=1)
        if self.positive:
            mask = np.all(samples_all > 0, axis=1)
            samples = samples_all[mask, :]
        else:
            samples = samples_all
        # compute Poisson and Gaussian likelihood of these samples:
        # proposal probability: Gaussian
        loglike_gauss_proposal = rv_logpdf(samples) - rv_logpdf(mean.reshape((1, -1)))
        assert np.isfinite(loglike_gauss_proposal).all(), (
            samples[~np.isfinite(loglike_gauss_proposal),:], loglike_gauss_proposal[~np.isfinite(loglike_gauss_proposal)])
        loglike_proposal = loglike_gauss_proposal + profile_loglike
        # print('gauss-poisson importance sampling:', loglike_gauss_proposal, profile_loglike)
        assert np.isfinite(loglike_proposal).all(), (samples, loglike_proposal, loglike_gauss_proposal)
        lam = samples @ X.T
        # print('resampling:', lam.shape)
        # target probability function: Poisson
        loglike_target = np.sum(counts * log(lam) - lam, axis=1)
        # print('full target:', loglike_target, loglike_target - profile_loglike)
        return samples, loglike_proposal, loglike_target

    def loglike_gauss_optimize(self, component_shapes):
        """Optimize the normalisations assuming a Gaussian data model.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.

        Returns
        -------
        gauss_reg: LinearRegression
            Fitted scikit-learn regressor object.
        """
        X = component_shapes
        y = self.flat_data
        self.gauss_reg.fit(X, y, self.flat_invvar)
        return self.gauss_reg

    def loglike_gauss(self, component_shapes):
        """Return profile likelihood.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.

        Returns
        -------
        loglike: float
            log-likelihood
        """
        gauss_reg = self.loglike_gauss_optimize(component_shapes)
        X = component_shapes
        y = self.flat_data
        ypred = gauss_reg.predict(X)
        loglike = -0.5 * np.sum((ypred - y) ** 2 * self.flat_invvar)

        W = self.invvar_matrix
        XTWX = X.T @ W @ X
        cond = np.linalg.cond(XTWX)
        if cond > self.cond_threshold:
            penalty = -1e100 * (1 + self.cond_threshold)
        else:
            penalty = 0
        return loglike + penalty

    def norms_gauss(self, component_shapes):
        """Return optimal normalisations.

        Normalisations of subsequent identical components will be zero.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.

        Returns
        -------
        norms: array
            normalisations, one value for each model component.
        """
        gauss_reg = self.loglike_gauss_optimize(component_shapes)
        return gauss_reg.coef_

    def sample_gauss(self, component_shapes, size, rng=np.random):
        """Sample from Gaussian covariance matrix.

        Parameters
        ----------
        component_shapes: array
            transposed list of the model component vectors.
        size: int
            Number of samples to generate.
        rng: object
            Random number generator

        Returns
        -------
        samples: array
            list of sampled normalisations
        """
        gauss_reg = self.loglike_gauss_optimize(component_shapes)
        loglike_profile = self.loglike_poisson(component_shapes)
        # get mean
        mean = gauss_reg.coef_
        # Compute covariance matrix
        X = component_shapes
        W = self.invvar_matrix
        XTWX = X.T @ W @ X
        covariance = np.linalg.inv(XTWX)
        samples_all = rng.multivariate_normal(mean, covariance, size=size)

        rv = multivariate_normal(mean, covariance)

        if self.positive:
            mask = np.all(samples_all > 0, axis=1)
            samples = samples_all[mask, :]
        else:
            samples = samples_all

        y_pred = samples @ X.T
        loglike_gauss_proposal = rv.logpdf(samples) - rv.logpdf(mean)
        loglike_target = -0.5 * np.sum(
            ((y_pred - self.flat_data) * self.flat_invvar) ** 2,
            axis=1,
        )
        loglike_proposal = loglike_profile + loglike_gauss_proposal

        return samples, loglike_proposal, loglike_target
