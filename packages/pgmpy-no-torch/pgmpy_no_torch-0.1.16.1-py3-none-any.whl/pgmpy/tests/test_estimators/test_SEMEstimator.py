import unittest

import pandas as pd
import numpy as np

from pgmpy.models import SEM
from pgmpy.estimators import IVEstimator

class TestIVEstimator(unittest.TestCase):
    def setUp(self):
        self.model = SEM.from_graph(
            ebunch=[
                ("Z1", "X", 1.0),
                ("Z2", "X", 1.0),
                ("Z2", "W", 1.0),
                ("W", "U", 1.0),
                ("U", "X", 1.0),
                ("U", "Y", 1.0),
                ("X", "Y", 1.0),
            ],
            latents=["U"],
            err_var={"Z1": 1, "Z2": 1, "W": 1, "X": 1, "U": 1, "Y": 1},
        )
        self.generated_data = self.model.to_lisrel().generate_samples(100000)

    def test_fit(self):
        estimator = IVEstimator(self.model)
        param, summary = estimator.fit(X="X", Y="Y", data=self.generated_data)
        self.assertTrue((param - 1) < 0.027)
