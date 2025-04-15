# Copyright 2024 The Meridian Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Defines model specification parameters for Meridian."""

import dataclasses

from meridian import constants
from meridian.model import prior_distribution
import numpy as np


__all__ = [
    "ModelSpec",
]


def _validate_roi_calibration_period(
    array: np.ndarray | None,
    array_name: str,
    media_channel_dim_name: str,
):
  if array is not None and (len(array.shape) != 2):
    raise ValueError(
        f"The shape of the `{array_name}` array {array.shape} should be"
        f" 2-dimensional (`n_media_times` x `{media_channel_dim_name}`)."
    )


@dataclasses.dataclass(frozen=True)
class ModelSpec:
  """Model specification parameters for Meridian.

  This class contains all model parameters that do not change between the runs
  of Meridian.

  Attributes:
    prior: A `PriorDistribution` object specifying the prior distribution of
      each set of model parameters. The distribution for a vector of parameters
      (for example, `alpha_m`) can be passed as either a scalar distribution or
      a vector distribution. If a scalar distribution is passed, it is broadcast
      to the actual shape of the parameter vector. See `paid_media_prior_type`
      for related details.
    media_effects_dist: A string to specify the distribution of media random
      effects across geos. This attribute is not used with a national-level
      model. Allowed values: `'normal'` or `'log_normal'`. Default:
      `'log_normal'`.
    hill_before_adstock: A boolean indicating whether to apply the Hill function
      before the Adstock function, instead of the default order of Adstock
      before Hill. This argument does not apply to RF channels. Default:
      `False`.
    max_lag: An integer indicating the maximum number of lag periods (≥ `0`) to
      include in the Adstock calculation. Can also be set to `None`, which is
      equivalent to infinite max lag. Default: `8`.
    unique_sigma_for_each_geo: A boolean indicating whether to use a unique
      residual variance for each geo. If `False`, then a single residual
      variance is used for all geos. Default: `False`.
    paid_media_prior_type: A string to specify the prior type for the media
      coefficients. Allowed values: `'roi'`, `'mroi'`, `'coefficient'`. Default:
      `'roi'`. The `PriorDistribution` contains distributions `roi_m`, `mroi_m`,
      and`beta_m`, but only one of these is used depending on the
      `paid_media_prior_type`. Likewise, the `PriorDistribution` contains
      distributions `roi_rf`, `mroi_rf`, and`beta_rf`, but only one of these is
      used depending on the `paid_media_prior_type`. When
      `paid_media_prior_type` is `'roi'`, the `PriorDistribution.roi_m` and
      `PriorDistribution.roi_rf` parameters are used to specify a prior on the
      ROI. When `paid_media_prior_type` is `'mroi'`, the
      `PriorDistribution.mroi_m` and `PriorDistribution.mroi_rf` parameters are
      used to specify a prior on the mROI. When `paid_media_prior_type` is
      `'coefficient'`, the `PriorDistribution.beta_m` and
      `PriorDistribution.beta_rf` parameters are used to specify a prior on the
      coefficient mean parameters.
    roi_calibration_period: An optional boolean array of shape `(n_media_times,
      n_media_channels)` indicating the subset of `time` that the ROI value of
      the `roi_m` prior (or mROI value of the `mroi_m` prior) applies to. If
      `None`, all times are used. Default: `None`.
    rf_roi_calibration_period: An optional boolean array of shape
      `(n_media_times, n_rf_channels)` indicating the subset of `time` that the
      ROI value of the `roi_rf` prior (or mROI value of the `mroi_rf` prior)
      applies to. If `None`, all times are used. Default: `None`.
    knots: An optional integer or list of integers indicating the knots used to
      estimate time effects. When `knots` is a list of integers, the knot
      locations are provided by that list. Zero corresponds to a knot at the
      first time period, one corresponds to a knot at the second time period,
      ..., and `(n_times - 1)` corresponds to a knot at the last time period).
      Typically, we recommend including knots at `0` and `(n_times - 1)`, but
      this is not required. When `knots` is an integer, then there are knots
      with locations equally spaced across the time periods, (including knots at
      zero and `(n_times - 1)`. When `knots` is` 1`, there is a single common
      regression coefficient used for all time periods. If `knots` is set to
      `None`, then the numbers of knots used is equal to the number of time
      periods in the case of a geo model. This is equivalent to each time period
      having its own regression coefficient. If `knots` is set to `None` in the
      case of a national model, then the number of knots used is `1`. Default:
      `None`.
    baseline_geo: An optional integer or a string for the baseline geo. The
      baseline geo is treated as the reference geo in the dummy encoding of
      geos. Non-baseline geos have a corresponding `tau_g` indicator variable,
      meaning that they have a higher prior variance than the baseline geo. When
      set to `None`, the geo with the biggest population is used as the
      baseline. Default: `None`.
    holdout_id: Optional boolean tensor of dimensions `(n_geos, n_times)` for a
      geo-level model or `(n_times,)` for a national model, indicating which
      observations are part of the holdout sample, which are excluded from the
      training sample. Only KPI data is excluded from the training sample. Media
      data is still included as it can affect Adstock for subsequent weeks. If
      "ROI priors" are used, then the `roi_m` parameters correspond to the ROI
      of all geos and times, even those in the holdout sample.
    control_population_scaling_id: An optional boolean tensor of dimension
      `(n_controls,)` indicating the control variables for which the control
      value will be scaled by population. If `None`, no control variables are
      scaled by population. Default: `None`.
    non_media_population_scaling_id: An optional boolean tensor of dimension
      `(n_non_media_channels,)` indicating the non-media variables for which the
      non-media value will be scaled by population. If `None`, then no non-media
      variables are scaled by population. Default: `None`.
  """

  prior: prior_distribution.PriorDistribution = dataclasses.field(
      default_factory=prior_distribution.PriorDistribution,
  )
  media_effects_dist: str = constants.MEDIA_EFFECTS_LOG_NORMAL
  hill_before_adstock: bool = False
  max_lag: int | None = 8
  unique_sigma_for_each_geo: bool = False
  paid_media_prior_type: str = constants.PAID_MEDIA_PRIOR_TYPE_ROI
  roi_calibration_period: np.ndarray | None = None
  rf_roi_calibration_period: np.ndarray | None = None
  knots: int | list[int] | None = None
  baseline_geo: int | str | None = None
  holdout_id: np.ndarray | None = None
  control_population_scaling_id: np.ndarray | None = None
  non_media_population_scaling_id: np.ndarray | None = None

  def __post_init__(self):
    # Validate media_effects_dist.
    if self.media_effects_dist not in constants.MEDIA_EFFECTS_DISTRIBUTIONS:
      raise ValueError(
          f"The `media_effects_dist` parameter '{self.media_effects_dist}' must"
          f" be one of {sorted(list(constants.MEDIA_EFFECTS_DISTRIBUTIONS))}."
      )
    # Validate roi_prior_type.
    if self.paid_media_prior_type not in constants.PAID_MEDIA_PRIOR_TYPES:
      raise ValueError(
          "The `paid_media_prior_type` parameter"
          f" '{self.paid_media_prior_type}' must be one of"
          f" {sorted(list(constants.PAID_MEDIA_PRIOR_TYPES))}."
      )
    _validate_roi_calibration_period(
        self.roi_calibration_period,
        "roi_calibration_period",
        "n_media_channels",
    )
    _validate_roi_calibration_period(
        self.rf_roi_calibration_period,
        "rf_roi_calibration_period",
        "n_rf_channels",
    )

    # Validate knots.
    if isinstance(self.knots, list) and not self.knots:
      raise ValueError("The `knots` parameter cannot be an empty list.")
    if isinstance(self.knots, int) and self.knots == 0:
      raise ValueError("The `knots` parameter cannot be zero.")
