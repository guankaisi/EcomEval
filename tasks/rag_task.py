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
import jieba
import string
from rouge_chinese import Rouge
from nltk.translate.bleu_score import sentence_bleu
class RAG_Task(AbstractTask):
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
    def dataset_load(self, **kwargs: Any):
        data_list = []
        # read all json from the directory
        for file in os.listdir('data/RAG/'):
            if file.endswith('.json'):
                with open('data/RAG/' + file, 'r') as f:
                    data_list.extend([json.loads(line) for line in f.readlines()])
        self.dataset = data_list
        print('Dataset loaded')
        self.data_loaded = True
    def tokenize(self, text: str) -> list:
        tokens = jieba.cut(text)
        punctuations = set(string.punctuation+ "，。、；‘’：“”（）《》&#;``【】！？0123456789")
        filtered_tokens = [token for token in tokens if token.strip() and token not in punctuations and len(token)>1]
        return filtered_tokens
    def calculate_bleu(self, ground_truth, answer):
        tokenized_ground_truth = self.tokenize(ground_truth)
        tokenized_answer = self.tokenize(answer)
        score = sentence_bleu([tokenized_ground_truth],tokenized_answer,weights=(1/4, 1/4, 1/4, 1/4))
        return score
    def calculate_rouge(self, ground_truth, answer):
        rouge = Rouge()
        score = rouge.get_scores(ground_truth, answer)
        return score[0]['rouge-1']['f']
    def evaluate(self, model: LLM, args: Any, task ='rag',**kwargs: Any):
        assert self.data_loaded
        batch_size = args.batch_size
        self.sampling_params = SamplingParams(temperature=0.7, min_tokens=1, max_tokens=200, repetition_penalty=1.1)
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
            with open('result_'+ task + '_' + model_name + '_' +'.json', 'a+', encoding='utf-8') as f:
                for i in range(len(results)):
                    f.write(json.dumps({'instruction': self.dataset[i]['instruction'], 'answer': self.dataset[i]['answer'], 'output': results[i]}, ensure_ascii=False) + '\n')
        Bleu_score = 0.0
        Rouge_score = 0.0
        for i in range(len(results)):
            rouge_score = self.calculate_rouge(self.dataset[i]['answer'], results[i])
            bleu_score = self.calculate_bleu(self.dataset[i]['answer'], results[i])
            Bleu_score += bleu_score
            Rouge_score += rouge_score
        Bleu_score = Bleu_score / len(results)
        Rouge_score = Rouge_score / len(results)
        print('Bleu Score:', Bleu_score)
        print('Rouge Score:', Rouge_score)     
        
    

