from tasks.abstask import AbstractTask
import torch
from vllm import LLM, SamplingParams
from typing import List, Optional, Tuple, Union, Dict, Any
from tqdm import tqdm
import time
import numpy as np
import random
import os
import json
class Information_Extract_Task(AbstractTask):
    def __init__(self, seed: int = 42, **kwargs: Any):
        super().__init__(seed=seed, **kwargs)
        self.dataset = None
        self.data_loaded = False
        self.seed = seed
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    def dataset_load(self, task='ave', **kwargs: Any):
        print(task)
        assert task in ['ave', 'ner']
        if task == 'ave':
            with open('data/IE/AVE/ave.json', 'r') as f:
                self.dataset = [json.loads(line) for line in f.readlines()]
        elif task == 'ner':
            with open('data/IE/NER/ner.json', 'r') as f:
                self.dataset = [json.loads(line) for line in f.readlines()]
        self.data_loaded = True
    def evaluate(self, model: LLM, args: Any, task='ave', **kwargs: Any):
        assert self.data_loaded
        assert task in ['ave', 'ner']
        batch_size = args.batch_size
        self.sampling_params = SamplingParams(temperature=0.7, min_tokens=1, max_tokens=10, repetition_penalty=1.1)
        results = []
        for i in tqdm(range(0, len(self.dataset), batch_size)):
            batch = self.dataset[i:i+batch_size]
            instructions = [js['instruction'] for js in batch]
            answer = [js['answer'] for js in batch]
            if not args.enable_lora:
                outputs = model.generate(
                    instructions,
                    self.sampling_params,
                    use_tqdm=False
                )
                outputs = [output.outputs[0].text for output in outputs]
                results.extend(outputs)
        model_name = args.model_path.split('/')[-1]
        if args.save_result:
            with open('result_'+ task + '_' + model_name +'.json', 'a+', encoding='utf-8') as f:
                for i in range(len(results)):
                    f.write(json.dumps({'instruction': self.dataset[i]['instruction'], 'answer': self.dataset[i]['answer'], 'output': results[i]}, ensure_ascii=False) + '\n')
        if task == 'ave':
            # evaluate accuracy of results
            correct = 0
            for i in range(len(results)):
                if self.dataset[i]['answer'] in results[i]:
                    correct += 1
            accuracy = correct / len(results)
            print('Accuracy:', accuracy)
        elif task == 'ner':
            correct = 0
            for i in range(len(results)):
                for entity in self.dataset[i]['answer']:
                    if entity in results[i]:
                        correct += 1/len(self.dataset[i]['answer'])
        
            accuracy = correct / len(results)
            print('Accuracy:', accuracy)

    

