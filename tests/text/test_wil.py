from typing import List, Union

import pytest
from jiwer import wil

from tests.text.helpers import TextTester
from tests.text.inputs import _inputs_error_rate_batch_size_1, _inputs_error_rate_batch_size_2
from torchmetrics.functional.text.wil import word_information_lost
from torchmetrics.text.wil import WordInfoLost
from torchmetrics.utilities.imports import _JIWER_AVAILABLE


def _compute_wil_metric_jiwer(prediction: Union[str, List[str]], reference: Union[str, List[str]]):
    return wil(reference, prediction)


@pytest.mark.skipif(not _JIWER_AVAILABLE, reason="test requires jiwer")
@pytest.mark.parametrize(
    ["preds", "targets"],
    [
        (_inputs_error_rate_batch_size_1.preds, _inputs_error_rate_batch_size_1.targets),
        (_inputs_error_rate_batch_size_2.preds, _inputs_error_rate_batch_size_2.targets),
    ],
)
class TestWordInfoLost(TextTester):
    @pytest.mark.parametrize("ddp", [False, True])
    @pytest.mark.parametrize("dist_sync_on_step", [False, True])
    def test_wil_class(self, ddp, dist_sync_on_step, preds, targets):

        self.run_class_metric_test(
            ddp=ddp,
            preds=preds,
            targets=targets,
            metric_class=WordInfoLost,
            sk_metric=_compute_wil_metric_jiwer,
            dist_sync_on_step=dist_sync_on_step,
        )

    def test_wil_functional(self, preds, targets):

        self.run_functional_metric_test(
            preds,
            targets,
            metric_functional=word_information_lost,
            sk_metric=_compute_wil_metric_jiwer,
        )

    def test_wil_differentiability(self, preds, targets):

        self.run_differentiability_test(
            preds=preds,
            targets=targets,
            metric_module=WordInfoLost,
            metric_functional=word_information_lost,
        )
