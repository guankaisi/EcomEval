from tasks.ie_task import Information_Extract_Task
from tasks.cls_task import Classification_Task
from tasks.gen_task import Generation_Task
from tasks.rag_task import RAG_Task
import torch
from vllm import LLM, SamplingParams
from typing import List, Optional, Tuple, Union, Dict, Any
from tqdm import tqdm
import time
import random
import argparse
import jieba
from nltk.translate.bleu_score import sentence_bleu
from rouge_chinese import Rouge

def load_model(args):
    if args.model_path == 'chatgpt' or args.model_path == 'gpt4':
        pass
    else:
        model = LLM(
            model=args.model_path,
            tokenizer=args.model_path,
            trust_remote_code=True,
            dtype=args.dtype,
            enable_lora=args.enable_lora,
        )
    return model

def evaluate_ie_task(model, args, tasks):
    task = Information_Extract_Task()
    task.dataset_load(task=tasks)
    task.evaluate(model, args, tasks)
def evaluate_cls_task(model, args):
    task = Classification_Task()
    task.dataset_load()
    task.evaluate(model, args)
def evaluate_gen_task(model, args, tasks):
    task = Generation_Task()
    task.dataset_load(task=tasks)
    task.evaluate(model, args, task=tasks)
def evaluate_rag_task(model, args):
    task = RAG_Task()
    task.dataset_load()
    task.evaluate(model, args)
def evaluate(model, args):
    print("Start evaluating")
    if 'ie' in args.tasks:
        print("Start evaluating Information Extraction task")
        tasks = ['ner','ave']
        for task in tasks:
            evaluate_ie_task(model, args, task)
    if 'cls' in args.tasks:
        print("Start evaluating Classification task")
        evaluate_cls_task(model, args)
    if 'gen' in args.tasks:
        print("Start evaluating Generation task")
        tasks = ['content', 'qa','price']
        for task in tasks:
            evaluate_gen_task(model, args, task)
        
    if 'rag' in args.tasks:
        print("Start evaluating RAG task")
        evaluate_rag_task(model, args)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', type=str, default='chatgpt')
    parser.add_argument('--dtype', type=str, default='bfloat16')
    # parser.add_argument('--enable_lora', type=bool, default=False)
    parser.add_argument('--save_result', type=bool, default=False)
    parser.add_argument('--batch_size', type=int, default=4)
    parser.add_argument('--tasks', type=List[str], default=['ie', 'cls', 'gen', 'rag'])
    args = parser.parse_args()
    model = load_model(args)
    # evaluate_ie_task(model, args)
    # evaluate_cls_task(model, args)
    # evaluate_gen_task(model, args)
    # evaluate_rag_task(model, args)
    evaluate(model, args)