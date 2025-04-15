"""
Image formation models simulated from gaussian noise distributions.
"""

from abc import abstractmethod
from typing import Optional
from typing_extensions import override

import jax.numpy as jnp
import jax.random as jr
from equinox import AbstractVar, field
from jaxtyping import Array, Complex, Float, PRNGKeyArray

from ...image import rfftn
from ...image.operators import Constant, FourierOperatorLike
from ...internal import error_if_not_positive
from ...simulator import AbstractImageModel
from ._base_distribution import AbstractDistribution


class AbstractGaussianDistribution(AbstractDistribution, strict=True):
    r"""An `AbstractDistribution` where images are formed via additive
    gaussian noise.

    Subclasses may compute the likelihood in real or fourier space and
    make different assumptions about the variance / covariance.
    """

    image_model: AbstractVar[AbstractImageModel]
    signal_scale_factor: AbstractVar[Float[Array, ""]]
    signal_offset: AbstractVar[Float[Array, ""]]

    normalizes_signal: AbstractVar[bool]

    @override
    def sample(
        self, rng_key: PRNGKeyArray, *, outputs_real_space: bool = True
    ) -> (
        Float[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim}",
        ]
        | Complex[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim//2+1}",
        ]
    ):
        """Sample from the gaussian noise model."""
        return self.compute_signal(
            outputs_real_space=outputs_real_space
        ) + self.compute_noise(rng_key, outputs_real_space=outputs_real_space)

    @override
    def compute_signal(
        self, *, outputs_real_space: bool = True
    ) -> (
        Float[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim}",
        ]
        | Complex[
            Array,
            "{self.image_model.instrument_config.y_dim}"
            " {self.image_model.instrument_config.x_dim//2+1}",
        ]
    ):
        """Render the image formation model."""
        simulated_image = self.image_model.render(
            outputs_real_space=True, applies_mask=False
        )
        if self.image_model.mask is None:
            if self.normalizes_signal:
                mean, std = jnp.mean(simulated_image), jnp.std(simulated_image)
                simulated_image = (simulated_image - mean) / std
            simulated_image = (
                self.signal_scale_factor * simulated_image + self.signal_offset
            )
        else:
            if self.normalizes_signal:
                is_signal = self.image_model.mask.array == 1.0
                mean, std = (
                    jnp.mean(simulated_image, where=is_signal),
                    jnp.std(simulated_image, where=is_signal),
                )
                simulated_image = (simulated_image - mean) / std
            simulated_image = self.image_model.mask(
                self.signal_scale_factor * simulated_image + self.signal_offset
            )
        return simulated_image if outputs_real_space else rfftn(simulated_image)

    @abstractmethod
    def compute_noise(
        self, rng_key: PRNGKeyArray, *, outputs_real_space: bool = True
    ) -> (
        Float[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim}",
        ]
        | Complex[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim//2+1}",
        ]
    ):
        """Draw a realization from the gaussian noise model and return either in
        real or fourier space.
        """
        raise NotImplementedError


class IndependentGaussianPixels(AbstractGaussianDistribution, strict=True):
    r"""A gaussian noise model, where each pixel is independently drawn from
    a zero-mean gaussian of fixed variance (white noise).

    This computes the likelihood in real space, where the variance is a
    constant value across all pixels.
    """

    image_model: AbstractImageModel
    variance: Float[Array, ""]
    signal_scale_factor: Float[Array, ""]
    signal_offset: Float[Array, ""]

    normalizes_signal: bool = field(static=True)

    def __init__(
        self,
        image_model: AbstractImageModel,
        variance: float | Float[Array, ""] = 1.0,
        signal_scale_factor: float | Float[Array, ""] = 1.0,
        signal_offset: float | Float[Array, ""] = 0.0,
        normalizes_signal: bool = False,
    ):
        """**Arguments:**

        - `image_model`:
            The image formation model.
        - `variance`:
            The variance of each pixel.
        - `signal_scale_factor`:
            A scale factor for the underlying signal simulated
            from `image_model`.
        - `signal_offset`:
            An offset for the underlying signal simulated from `image_model`.
        - `normalizes_signal`:
            Whether or not the signal is normalized before applying the `signal_scale_factor`
            and `signal_offset`.
            If an `AbstractMask` is given to `image_model.mask`, the signal is normalized
            within the region where the mask is equal to `1`.
        """  # noqa: E501
        self.image_model = image_model
        self.variance = error_if_not_positive(variance)
        self.signal_scale_factor = error_if_not_positive(signal_scale_factor)
        self.signal_offset = jnp.asarray(signal_offset)
        self.normalizes_signal = normalizes_signal

    @override
    def compute_noise(
        self, rng_key: PRNGKeyArray, *, outputs_real_space: bool = True
    ) -> (
        Float[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim}",
        ]
        | Complex[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim//2+1}",
        ]
    ):
        pipeline = self.image_model
        n_pixels = pipeline.instrument_config.padded_n_pixels
        freqs = pipeline.instrument_config.padded_frequency_grid_in_angstroms
        # Compute the zero mean variance and scale up to be independent of the number of
        # pixels
        std = jnp.sqrt(n_pixels * self.variance)
        noise = pipeline.postprocess(
            std
            * jr.normal(rng_key, shape=freqs.shape[0:-1])
            .at[0, 0]
            .set(0.0)
            .astype(complex),
            outputs_real_space=outputs_real_space,
        )

        return noise

    @override
    def log_likelihood(
        self,
        observed: Float[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim}",
        ],
    ) -> Float[Array, ""]:
        """Evaluate the log-likelihood of the gaussian noise model.

        **Arguments:**

        - `observed` : The observed data in real space.
        """
        variance = self.variance
        # Create simulated data
        simulated = self.compute_signal(outputs_real_space=True)
        # Compute residuals
        residuals = simulated - observed
        # Compute standard normal random variables
        squared_standard_normal_per_pixel = jnp.abs(residuals) ** 2 / (2 * variance)
        # Compute the log-likelihood for each pixel.
        log_likelihood_per_pixel = -1.0 * (
            squared_standard_normal_per_pixel - jnp.log(2 * jnp.pi * variance) / 2
        )
        # Compute log-likelihood, summing over pixels
        log_likelihood = jnp.sum(log_likelihood_per_pixel)

        return log_likelihood


class IndependentGaussianFourierModes(AbstractGaussianDistribution, strict=True):
    r"""A gaussian noise model, where each fourier mode is independent.

    This computes the likelihood in Fourier space,
    so that the variance to be an arbitrary noise power spectrum.
    """

    image_model: AbstractImageModel
    variance_function: FourierOperatorLike
    signal_scale_factor: Float[Array, ""]
    signal_offset: Float[Array, ""]

    normalizes_signal: bool = field(static=True)

    def __init__(
        self,
        image_model: AbstractImageModel,
        variance_function: Optional[FourierOperatorLike] = None,
        signal_scale_factor: float | Float[Array, ""] = 1.0,
        signal_offset: float | Float[Array, ""] = 0.0,
        normalizes_signal: bool = False,
    ):
        """**Arguments:**

        - `image_model`:
            The image formation model.
        - `variance_function`:
            The variance of each fourier mode. By default,
            `cryojax.image.operators.Constant(1.0)`.
        - `signal_scale_factor`:
            A scale factor for the underlying signal simulated from `image_model`.
        - `signal_offset`:
            An offset for the underlying signal simulated from `image_model`.
        - `normalizes_signal`:
            Whether or not the signal is normalized before applying the `signal_scale_factor`
            and `signal_offset`.
            If an `AbstractMask` is given to `image_model.mask`, the signal is normalized
            within the region where the mask is equal to `1`.
        """  # noqa: E501
        self.image_model = image_model
        self.variance_function = variance_function or Constant(1.0)
        self.signal_scale_factor = error_if_not_positive(jnp.asarray(signal_scale_factor))
        self.signal_offset = jnp.asarray(signal_offset)
        self.normalizes_signal = normalizes_signal

    def compute_noise(
        self, rng_key: PRNGKeyArray, *, outputs_real_space: bool = True
    ) -> (
        Float[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim}",
        ]
        | Complex[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim//2+1}",
        ]
    ):
        pipeline = self.image_model
        n_pixels = pipeline.instrument_config.padded_n_pixels
        freqs = pipeline.instrument_config.padded_frequency_grid_in_angstroms
        # Compute the zero mean variance and scale up to be independent of the number of
        # pixels
        std = jnp.sqrt(n_pixels * self.variance_function(freqs))
        noise = pipeline.postprocess(
            std
            * jr.normal(rng_key, shape=freqs.shape[0:-1])
            .at[0, 0]
            .set(0.0)
            .astype(complex),
            outputs_real_space=outputs_real_space,
        )

        return noise

    @override
    def log_likelihood(
        self,
        observed: Complex[
            Array,
            "{self.image_model.instrument_config.y_dim} "
            "{self.image_model.instrument_config.x_dim//2+1}",
        ],
    ) -> Float[Array, ""]:
        """Evaluate the log-likelihood of the gaussian noise model.

        **Arguments:**

        - `observed` : The observed data in fourier space.
        """
        pipeline = self.image_model
        n_pixels = pipeline.instrument_config.n_pixels
        freqs = pipeline.instrument_config.frequency_grid_in_angstroms
        # Compute the variance and scale up to be independent of the number of pixels
        variance = n_pixels * self.variance_function(freqs)
        # Create simulated data
        simulated = self.compute_signal(outputs_real_space=False)
        # Compute residuals
        residuals = simulated - observed
        # Compute standard normal random variables
        squared_standard_normal_per_mode = jnp.abs(residuals) ** 2 / (2 * variance)
        # Compute the log-likelihood for each fourier mode.
        log_likelihood_per_mode = (
            squared_standard_normal_per_mode - jnp.log(2 * jnp.pi * variance) / 2
        )
        # Compute log-likelihood, throwing away the zero mode. Need to take care
        # to compute the loss function in fourier space for a real-valued function.
        log_likelihood = (
            -1.0
            * (
                jnp.sum(log_likelihood_per_mode[1:, 0])
                + 2 * jnp.sum(log_likelihood_per_mode[:, 1:])
            )
            / n_pixels
        )

        return log_likelihood
