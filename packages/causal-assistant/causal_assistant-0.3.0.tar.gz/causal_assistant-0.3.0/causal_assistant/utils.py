"""A set of methods to somewhat simplify the process of causal bootstrapping"""
import re
import inspect
import warnings

from typing import Any, Literal, TypeAlias

import numpy as np
import pandas as pd

import causalBootstrapping as cb
from distEst_lib import MultivarContiDistributionEstimator as MCDE


FeatureType: TypeAlias = np.ndarray | pd.DataFrame | pd.Series
BinFeatureType: TypeAlias = np.ndarray | pd.DataFrame | pd.Series | \
                            tuple[np.ndarray | pd.DataFrame | pd.Series, int | list[int]]


def _find_primed_features(function_string):
    """
    Finds features which exist in a 'primed' state (typically just the cause var?)
    :param function_string: The probability function string derived from causal analysis
    :return: A dictionary mapping unprimed to primed features
    """
    primed_features = set(re.compile("([A-z]+'+)").findall(function_string))
    primed_feature_map = {p.replace("'", ""): p for p in primed_features}
    return primed_feature_map


def make_data_map(function_string, kernel_used: bool, features: dict[str, FeatureType]) -> dict[str, FeatureType]:
    """
    Creates the 'data' parameter for general causal bootstrapping
    :param function_string: The probability function string derived from causal analysis
    :param kernel_used: Set to true if a kernel is included as part of the data map (subtly changes entries)
    :param features: All features to be included in the data map. Dataframes will have index inserted for preservation
    :return: The 'data' argument, properly formatted
    """
    for feature in features:
        if isinstance(features[feature], pd.DataFrame):
            # insert the index as a value, so it doesn't get lost in the deconfound
            features[feature] = features[feature].reset_index().values

    primed_features = _find_primed_features(function_string)

    for feature, primed_feature in primed_features.items():
        features[primed_feature] = features[feature]

    return features


def _find_required_distributions(function_string) -> tuple[set[str], dict[str, list[str]]]:
    """
    Extracts distributions from the function string
    :param function_string: The probability function string derived from causal analysis
    :return: A dictionary mapping distribution names to required variables
    """
    # work out the required distributions. This is quite easy, as the estimation only returns probabilies of one shape
    dist_matcher = re.compile(r"P\(([A-z',]*)\)")
    distributions = dist_matcher.findall(function_string)

    # two simplification stages here:
    #  1. remove 's (as we ignore them for distribution estimation purposes?)
    #  2. split by comma to find individual parameters we need - note that these might be duplicated
    required_dists = {d: d.replace("'", "_prime").split(",") for d in distributions}

    # find all required features
    required_features = set(var for dist in required_dists.values() for var in dist)

    return required_features, required_dists


def _make_dist(required_values: list[str], bins: dict[str, list[int]], features: dict[str, FeatureType],
               fit_method: Literal['kde', 'hist'], estimator_kwargs: dict[str, Any] | None = None):
    """
    Make a distribution
    :param required_values: the features to include in the distribution
    :param bins: dictionary mapping feature names to a bin count
    :param features: dictionary mapping feature names to features
    :param fit_method: The fitting method to use ('kde' or 'hist')
    :param estimator_kwargs: extra kwargs for the estimator
    :return: The distribution method
    """
    data_bins = [v for r in required_values for v in bins[r.replace("_prime", "")]]
    if len(required_values) == 1:
        data_fit = features[required_values[0].replace("_prime", "")]
    else:
        data_fit_values = [features[r.replace("_prime", "")] for r in required_values]
        data_fit = np.hstack(data_fit_values)
    # create the estimator
    estimator = MCDE(data_fit=data_fit, n_bins=data_bins)
    # fit the estimator
    if fit_method == "kde":
        pdf, probs = estimator.fit_kde(**estimator_kwargs)
    elif fit_method == "hist":
        pdf, probs = estimator.fit_histogram(**estimator_kwargs)
    else:
        raise ValueError("Unrecognised fit method")

    # make the lambda function as per the specification
    pdf_method = lambda **kwargs: pdf(list(kwargs.values())[0]) \
        if len(kwargs) == 1 else pdf(list(kwargs.values()))

    # unfortunately, because the inspection method used is a little annoying, we have to make sure that we fix
    #  the signature as well
    params = [inspect.Parameter(name=r, kind=inspect.Parameter.POSITIONAL_OR_KEYWORD) for r in required_values]
    pdf_method.__signature__ = inspect.Signature(parameters=params)

    return pdf_method


def make_dist_map(function_string, features: dict[str, FeatureType], bins: dict[str, list[int]],
                  fit_method: Literal['kde', 'hist'] = "kde", estimator_kwargs: dict | None = None):
    """
    Creates the 'dist_map' parameter for general causal bootstrapping
    :param function_string: The probability function string derived from causal analysis
    :param fit_method: The method to estimate distributions. Can be either 'hist' or 'kde'
    :param features: All features involved in the de-confounding process. These can either be just the raw feature (for
                     categorical data) or a tuple of the data and the number of bins requested (for continuous data).
    :param bins: Bins used for each feature
    :param estimator_kwargs: arguments to be passed to the estimator
    :return: A dictionary mapping probability functions to lambda methods representing their distributions
    """
    required_features, required_dists = _find_required_distributions(function_string)

    # validation: ensure that all required values have been provided
    missing_values = [x for x in required_features if x not in features and not x.endswith("_prime")]
    assert len(missing_values) == 0, f"Not all values provided! {missing_values}"

    # new type of features, now that we have removed all the tuples
    features: dict[str, np.ndarray]

    if estimator_kwargs is None:
        estimator_kwargs = {}

    distributions: dict[str, callable] = {}
    for required_key, required_values in required_dists.items():
        try:
            # note that there may be repetitions here!
            # we are okay with that, it'll just waste a bit of compute
            pdf_method = _make_dist(required_values, bins, features, fit_method, estimator_kwargs)
            distributions[required_key] = pdf_method
        except ValueError:
            print("Required values were", required_values)
            raise

    return distributions


def _calc_weights(function_string: str, weight_func: callable, cause_var: str,
                  features: dict[str, FeatureType], bins: dict[str, list[int]], fit_method: Literal['kde', 'hist'],
                  kernel_used: bool = False):
    """
    Compute causal weights for a given set of distributions
    Adapted from general_causal_bootstrapping_simple in causalBootstrapping
    """
    data_map = make_data_map(function_string, kernel_used=kernel_used, features=features)
    dist_map = make_dist_map(function_string, fit_method=fit_method, features=features, bins=bins)

    intv_cause = f"intv_{cause_var}"
    kernel = eval(f"lambda {intv_cause}, {cause_var}: 1 if {intv_cause}=={cause_var} else 0")
    N = features[cause_var].shape[0]
    w_func = weight_func(dist_map=dist_map, N=N, kernel=kernel)
    unique_causes = np.unique(features[cause_var])
    weights = np.zeros((N, len(unique_causes)), dtype=np.float64)

    primed_features = _find_primed_features(function_string)
    if not kernel_used:
        for feature, _ in primed_features.items():
            features.pop(feature)

    for i, y in enumerate(unique_causes):
        weights[:, i] = cb.weight_compute(weight_func=w_func,
                                          data=data_map,
                                          intv_var={intv_cause if kernel_used else cause_var: [y for _ in range(N)]})

    all_weights_equal = np.std(weights, axis=0).sum() < 1e-10
    if all_weights_equal:
        warnings.warn("All weights are equal! Check your data")

    return weights, data_map, unique_causes


def _bootstrap(weight_func: callable, function_string: str, cause_var: str, effect_var: str,
               fit_method: Literal['kde', 'hist'], steps: int, features: dict[str, FeatureType],
               bins: dict[str, list[int]]):
    # assume effect data will be a dataframe, so will have an index?
    original_df = features[effect_var]
    if not isinstance(original_df, pd.DataFrame):
        # auto-cast
        original_df = features[effect_var] = pd.DataFrame(features[effect_var])

    kernel_used = re.match(rf".*(K\({cause_var},{cause_var}'+\)).*", function_string) is not None
    weights, data_map, _ = _calc_weights(function_string=function_string,
                                         weight_func=weight_func,
                                         cause_var=cause_var,
                                         fit_method=fit_method,
                                         features=features,
                                         bins=bins,
                                         kernel_used=kernel_used)

    if kernel_used:
        ivn = cause_var
    else:
        ivn = next(d for d in data_map.keys() if d.startswith(cause_var))

    bootstraps = []
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore", category=RuntimeWarning)
        for _ in range(steps):
            bootstrap_data, _ = cb.bootstrapper(data=data_map, weights=weights, mode="robust",
                                                intv_var_name_in_data=[ivn])
            bootstraps.append(bootstrap_data)

    cb_data = {}
    for key in bootstraps[0]:
        cb_data[key] = np.vstack([d[key] for d in bootstraps])

    levels = original_df.index.nlevels
    if levels > 1:
        idx = pd.MultiIndex.from_tuples(cb_data[effect_var][:, 0:levels].tolist(),
                                        names=original_df.index.names)
    else:
        idx = pd.Index(cb_data[effect_var][:, 0], name=original_df.index.name)

    X = pd.DataFrame(cb_data[effect_var][:, levels:], index=idx, columns=original_df.columns)
    y = pd.DataFrame(cb_data[cause_var], index=idx)

    return X, y
