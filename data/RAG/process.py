import json
import os 
import pandas as pd
import re

def process_rag(path1,path2):
    with open(path1, 'r', encoding='utf-8') as f:
        json_list = [json.loads(line) for line in f.readlines()]
    with open(path2, 'r', encoding='utf-8') as f:
        json_list2 = [json.loads(line) for line in f.readlines()]
    instruction = '''请根据商品的有关介绍回答商品,简要相关问题，
    商品介绍为：
    {context}
    问题为：
    {question}
    你的回答为：
    '''
    f = open('rag.json','a+',encoding='utf-8')
    for js,js2 in zip(json_list,json_list2):
        js_new = {}
        js_new['instruction'] = instruction.format(context=js['contexts'], question=js['question'])
        js_new['answer'] = js2['回答']
        f.write(json.dumps(js_new, ensure_ascii=False) + '\n')
    f.close()
    print('process gen done')


if __name__ == "__main__":
    process_rag('/data4/kaisi/ecom-eval/data/RAG/rag_data/baichuan_title_gpt4.json','/data4/kaisi/ecom-eval/data/RAG/rag_data/gpt4_ground_regen.json')