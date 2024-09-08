import random
from abc import ABC, abstractmethod
from typing import Any, Dict, Sequence
import numpy as np
import torch
class AbstractTask(ABC):
    def __init__(self, seed: int = 42, **kwargs: Any):
        self.dataset = None
        self.data_loaded = False
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    def dataset_load(self):
        pass

    def evaluate(self):
        pass
    
    

    