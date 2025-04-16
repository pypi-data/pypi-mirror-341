import os
import random

import pytest

import phitter


def get_data(path: str) -> list[float | int]:
    sample_distribution_file = open(path, "r", encoding="utf-8-sig")
    data = [float(x.replace(",", ".")) for x in sample_distribution_file.read().splitlines()]
    sample_distribution_file.close()
    return data


@pytest.fixture
def random_file_path():
    base_path = "./datasets_test/discrete/"
    files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
    random_file = random.choice(files)
    return os.path.join(base_path, random_file)


def test_phitter_analysis(random_file_path):
    data = get_data(random_file_path)

    ## Fit dataset
    phi = phitter.Phitter(data=data, fit_type="discrete")
    phi.fit(n_workers=2)

    assert len(phi.sorted_distributions_sse) > 0, "sorted_distributions_sse should not be empty"
