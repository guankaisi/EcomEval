import json
import os 

def process_mpc(path):
    with open(path, 'r', encoding='utf-8') as f:
        json_list = [json.loads(line) for line in f.readlines()]
    f = open('ecellm-prp.json','a+',encoding='utf-8')
    for js in json_list:
        js_new = {}
        js_new['instruction'] = js['instruction'] + '\n' + js['input'] + '\n' + js['options'] + '\n' + "Your answer is:"
        js_new['answer'] = js['output'][0]
        f.write(json.dumps(js_new, ensure_ascii=False) + '\n')
    f.close()
    print('process mpc done')
def process_pm(path):
    with open(path, 'r', encoding='utf-8') as f:
        json_list = [json.loads(line) for line in f.readlines()]
    f = open('ecellm-psi.json','a+',encoding='utf-8')
    for js in json_list:
        js_new = {}
        js_new['instruction'] = js['instruction'] + '\n' + js['input'] +  "Your answer is:"
        js_new['answer'] = js['output']
        f.write(json.dumps(js_new, ensure_ascii=False) + '\n')
    f.close()
    print('process pm done')

def process_openbg(path):
    instruction = '''
    请你判断货物的标题Title和属性Attritute是否匹配？如果匹配请回答“匹配”，如果不匹配请回答“不匹配”。
    '''
    with open(path, 'r', encoding='utf-8') as f:
        json_list = [json.loads(line) for line in f.readlines()]
    f = open('openbg-2.json','a+',encoding='utf-8')
    for js in json_list:
        js_new = {}
        js_new['instruction'] = instruction + js['sentences'] + '\n' + "你的回答是:"
        js_new['answer'] = js['labels']['zh'][0]
        f.write(json.dumps(js_new, ensure_ascii=False) + '\n')
    f.close()
    print('process openbg done')

if __name__ == "__main__":
    process_openbg('/data4/kaisi/ecom-eval/data/CLS/ZH-OpenBG_Align-CLS-title_attribute_matching/test.json')