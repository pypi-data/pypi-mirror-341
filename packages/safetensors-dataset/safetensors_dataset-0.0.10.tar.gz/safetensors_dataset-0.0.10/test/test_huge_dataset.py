import time
from unittest import TestCase

import torch

from safetensors_dataset import SafetensorsDataset, load_safetensors


class HugeDatasetTestCase(TestCase):
    dataset: SafetensorsDataset
    sharded_dataset: SafetensorsDataset

    def setUp(self):
        # self.inputs = torch.randint(32000, (3_000_000, 512))
        self.dataset = load_safetensors("negatives_sred_train_feat_2,13,20,22.safetensors")
        print("sharding dataset ...")
        self.sharded_dataset = self.dataset.shard()
        print("done")

    def test_access_speed(self):
        for pos in {0, 42, 10000, 100000, 1000000, -1}:
            t_start = time.time()
            a = self.dataset.__getitems__([pos] * 32)
            t_end = time.time()
            print(t_end - t_start)
            t_start = time.time()
            for _ in range(32):
                b = self.sharded_dataset[pos]
                assert torch.equal(a[0]["input_ids"], b["input_ids"])
            t_end = time.time()
            print(t_end - t_start)
