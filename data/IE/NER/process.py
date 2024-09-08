import json
entity_set = {'I-MISC', 'I-XH', 'B-MISC', 'B-XH', 'I-HPPX', 'I-HCCX', 'B-HCCX', 'B-HPPX'}
def process_ner(path):
    with open(path,'r',encoding='utf-8') as f:
        lines = f.read().split('\n\n')
    f = open('ner_test.json','a+',encoding='utf-8')
    for line in lines:
        line_json = {"sentence":"","label":[]}
        line_list = line.split('\n')
        if len(line_list) <= 1:
            continue
        sentence = ""
        for en in line_list:
            if len(en)>=1:
               sentence += en.split(' ')[0]
            else:
                continue
            tag = en.split(' ')[1]
            if tag in entity_set and tag[0] == 'B':
                line_json['label'].append({"entity":en.split(' ')[0], "type":tag.split('-')[1]})
            if tag in entity_set and tag[0] == 'I':
                leng = len(line_json['label'])
                line_json['label'][leng-1]['entity']+= en.split(' ')[0]

        line_json['sentence'] = sentence
        print(line_json)
        f.write(json.dumps(line_json,ensure_ascii=False)+'\n')
    print(len(lines))
    
    
    # print(lines)
if __name__ == "__main__":
    process_ner('test.txt')