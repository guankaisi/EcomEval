import json
instruction = "请在以下句子中，进行命名实体识别任务，请你提取出<{type}>,输出一个或多个词语,不要输出多余的内容，句子为<{sentence}>，你的输出为："

def process_json(path):
    with open(path, 'r',encoding='utf-8') as f:
        json_list = [json.loads(line) for line in f.readlines()]
    f = open('ner.json','a+',encoding='utf-8')
    for js in json_list:
        count_HPPX = 0
        count_HCCX = 0 
        for span in js['label']:
            if span['type'] == 'HPPX':
                count_HPPX += 1
            if span['type'] == 'HCCX':
                count_HCCX += 1
        if count_HPPX == 0 and count_HCCX == 0:
            continue
        # HPPX
        HPPX = []
        if count_HPPX > 0:
            for span in js['label']:
                if span['type'] == 'HPPX':
                    HPPX.append(span['entity'])
            js_new = {}
            instruction_new = instruction.format(type='商品品牌', sentence=js['sentence'])
            js_new['instruction'] = instruction_new
            js_new['answer'] = HPPX
            f.write(json.dumps(js_new, ensure_ascii=False) + '\n')
        # HCCX
        HCCX = []
        if count_HCCX > 0:
            for span in js['label']:
                if span['type'] == 'HCCX':
                    HCCX.append(span['entity'])
            js_new = {}
            instruction_new = instruction.format(type='商品类别', sentence=js['sentence'])
            js_new['instruction'] = instruction_new
            js_new['answer'] = HCCX
            f.write(json.dumps(js_new, ensure_ascii=False) + '\n')
    f.close()
    

def duplitcate_json(path):
    with open(path, 'r',encoding='utf-8') as f:
        json_list = [json.loads(line) for line in f.readlines()]
    f = open('ner_new.json','a+',encoding='utf-8')
    for js in json_list:
        js['answer'] = list(set(js['answer']))
        f.write(json.dumps(js, ensure_ascii=False) + '\n')
    f.close()
duplitcate_json('ner.json')
