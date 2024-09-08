import json
instruction = "请在以下句子中，提取关于<{entity}>的属性，只输出一个词语，不要输出多余的内容，句子为：<{sentence}>，属性为："
def process_json(path):
    with open(path, 'r',encoding='utf-8') as f:
        json_list = [json.loads(line) for line in f.readlines()]
    f = open('ave.json','a+',encoding='utf-8')
    for js in json_list:
        for span in js['spans']:
            js_new = {}
            instruction_new = instruction.replace('{entity}', span['type']).replace('{sentence}', js['sentences'])
            js_new['instruction'] = instruction_new
            js_new['answer'] = span['term']
            f.write(json.dumps(js_new, ensure_ascii=False) + '\n')
    f.close()
    
process_json('ave_test.json')
