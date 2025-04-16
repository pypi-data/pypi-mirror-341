import numpy as np
import pandas as pd
import statsmodels.api as sm

class IVEstimator:
    """
    Implements Instrumental Variable (IV) based estimator.
    """

    def __init__(self, model):
        """
        Initialize IVEstimator object.

        Parameters
        ----------
        model: pgmpy.models.SEM
            The model for which estimation need to be done.

        Examples
        --------

        """
        self.model = model

    def fit(self, X, Y, data, ivs=None, civs=None):
        """
        Estimates the parameter X -> Y.

        Parameters
        ----------
        X: str
            The covariate variable of the parameter being estimated.

        Y: str
            The predictor variable of the parameter being estimated.

        data: pd.DataFrame
            The data from which to learn the parameter.

        ivs: List (default: None)
            List of variable names which should be used as Instrumental Variables (IV).
            If not specified, tries to find the IVs from the model structure, fails if
            can't find either IV or Conditional IV.

        civs: List of tuples (tuple form: (var, coditional_var))
            List of conditional IVs to use for estimation.
            If not specified, tries to find the IVs from the model structure, fails if
            can't find either IV or Conditional IVs.

        Examples
        --------
        >>> from pgmpy.estimators import IVEstimator # TODO: Finish example.
        """
        if (ivs is None) and (civs is None):
            ivs = self.model.get_ivs(X, Y)
            civs = self.model.get_conditional_ivs(X, Y)

        civs = [civ for civ in civs if civ[0] not in ivs]

        reg_covars = []
        for var in self.model.graph.predecessors(X):
            if var in self.model.observed:
                reg_covars.append(var)

        # Get CIV conditionals
        civ_conditionals = []
        for civ in civs:
            civ_conditionals.extend(civ[1])

        # First stage regression.
        params = (
            sm.OLS(data.loc[:, X], data.loc[:, reg_covars + civ_conditionals])
            .fit()
            .params
        )

        data["X_pred"] = np.zeros(data.shape[0])
        for var in reg_covars:
            data.X_pred += params[var] * data.loc[:, var]

        summary = sm.OLS(
            data.loc[:, Y], data.loc[:, ["X_pred"] + civ_conditionals]
        ).fit()
        return summary.params["X_pred"], summary
