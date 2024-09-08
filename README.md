# EcomEval: A Ecommerce Domain Evaluation for Large Language Models

## 📃Table of Contents

How to build EcomEval

How to use EcomEval

Related Works

Citation

## 🛠 How to build EcomEval

### E-commerce domain Information Extraction task

For the information extraction task, we choose name entity recognition and attribute value extraction as subtasks. We have 1293 questions for ner task and 629 questions for ave task .

Here are some examples for this NER and ACE task.

NER task:

```
{"instruction": "请在以下句子中，进行命名实体识别任务，请你提取出<商品类别>,只输出一个词语，不要输出多余的内容，句子为<素面功夫竹骨一尺单面,舞蹈武术团体表演响扇黄蓝黑红太极图>，你的输出为：", "answer": ["响扇", "竹骨"]}

```

AVE task:

```
{"instruction": "请在以下句子中，提取关于<图案>的属性，只输出一个词语，不要输出多余的内容，句子为：<黑色为主的包身上还用撞色印花图案做成点缀>，属性为：", "answer": "撞色印花"}

```

### E-commerce domain Classification task

For the classification task, we have structured subtasks such as product match, product relevance prediction, and product title match into multiple-choice or true/false questions. This format adjustment aims to simplify the accuracy calculation process. We have 9000 multi-choice questions and 4750 True/False questions.

True/False question: 

```
{"instruction": "\n    请你判断货物item1和item2是否属于同一商品，如果是请回答“相同”，否则请回答“不相同”。\n    Item 1: 兰芝隔离霜正品官方旗舰店保湿提亮肤色防晒遮瑕妆前乳打底女大牌, 功效#:#遮瑕#;#功效#:#提亮肤色#;#妆前乳单品#:#隔离霜#;#是否防晒#:#是#;#产地#:#韩国#;#适合肤质#:#任何肤质#;#是否为特殊用途化妆品#:#否#;#功效#:#保湿#;#品牌#:#Laneige/兰芝#;#功效#:#隐形毛孔#;#功效#:#隔离#;#限期使用日期范围#:#2023-11-01至2023-12-15#;#规格类型#:#正常规格#;#质地分类#:#乳霜,\nItem 2: 兰芝雪纱隔离霜防晒妆前乳紫色打底遮瑕三合一旗舰店官网官方正品, 功效#:#妆前打底#;#品牌#:#Laneige/兰芝#;#功效#:#修饰肤色#;#是否防晒#:#是#;#是否为特殊用途化妆品#:#否#;#限期使用日期范围#:#2023-05-01至2023-05-01#;#规格类型#:#正常规格#;#功效#:#隔离#;#妆前乳单品#:#雪纱丝柔防晒隔离霜SPF25/PA++#;#产地#:#韩国\n你的回答是:", "answer": "相同"}
```

Multi-choice question

```
{"instruction": "Compare the query and the product title to determine if the product fully meets the query specifications. Choose the option that best describes the relevance between them.\n{\"query\": \"powerhouse gym t shirt\", \"product title\": \"T Shirt Jerks - Lifting Things - Funny Gym T Shirt, Bodybuilding T Shirt, Gym Shirt, Parody Shirt(White, Small)\"}\n[\"A: The product is relevant to the query, and satisfies all the query specifications.\", \"B: The product is somewhat relevant. It fails to fulfill some aspects of the query but the product can be used as a functional substitute.\", \"C: The product does not fulfill the query, but could be used in combination with a product exactly matching the query.\", \"D: The product is irrelevant to the query.\"]\nYour answer is:", "answer": "B"}
```



### E-commerce domain Generation task

We choose three subtask for evaluating E-commerce domain ability. Title generation, price calculation and Question answer task.

For each task, we have 500 questions.

Title Generation

```
{"instruction": "\n    以下是商品信息，请跟据商品信息填写商品标题。\n    \n颜色分类#:#黑色#;#成分含量#:#51%(含)-70%(含)#;#上市年份季节#:#2022年春季#;#风格#:#通勤#;#腰型#:#高腰#;#面料#:#其他#;#廓形#:#A型#;#图案#:#纯色#;#裙长#:#短裙#;#适用年龄#:#25-29周岁#;#货号#:#L#;#材质#:#其他#;#通勤#:#韩版#;#裙型#:#A字裙\n商品标题为：", "answer": "小个子冬裙半身裙女高腰a字裙黑色裙子秋冬防走光包臀裙开叉短裙"}
```

Price calculate

```
{"instruction": "以下是商品信息，请你根据商品的数量以及总价等信息加算出商品的单价，单价=总价/数量，保留两位小数。\n    商品信息：瑞惠佳品纸杯一次性纸杯200ml加厚款100只装家用办公商用RH-0002，\n    商品总价为：8.30元，\n    商品单价为：\n    ", "answer": "0.08"}

```

Question answer task

```
{"instruction": "Context: How to retexture with GIMP. Hello everybody I am following a retexture tutorial on the Creation Kit website (LINKREMOVED) and have reached the part where I load up the texture in GIMP to edit it. That worked as expected but I have a problem with the following step \"A saving dialogue box will open, where it says Compression select BC1/DXT1 then check the flag next to Generate Mipmaps then click save\". This is where I'm stuck, I can't seem to find the compression selection on the Save As pop up window all I see is this LINKREMOVED . Has anybody come across this problem? Thanks in advance.\nQuestion: What program are they using to load up the texture?\n    Extract spans from context to answer the question. You are only allowed to extract information from the context, and are not allowed to add additional content.\n    Your answer is:\n    ", "answer": "GIMP"}

```

### E-commerce domain Retrieval Augmented Generation task

In practical applications, LLMs often face challenges such as hallucinations and difficulties in updating knowledge. Therefore, external searches are frequently necessary to address these issues. Similarly, the ability to perform Retrieval-Augmented Generation (RAG), which involves answering questions by incorporating external text, is also crucial.

```
{"instruction": "请根据商品的有关介绍回答商品,简要相关问题，\n    商品介绍为：\n    来自“职业家庭煮妇”的菜板选择攻略！ : 选购菜板时要根据材质、品牌、尺寸和厚度等因素进行综合考虑，选择适合自己需求和使用习惯的菜板。\t砧板越大越好，千万别选错，今天聊聊砧板那些事 : 说起砧板，其实还是很有门道的，也用过很多材质的砧板，下面就来聊聊砧板的那些事。目前市面上的砧板种类比较多，材质也各异。从不同材质砧板分析，其实都有优势，但如果要考虑到健康，那即使是相同材质，品质也会不同。比如竹子砧板，如果使用的胶水品质过硬，后期使用注意保养，也不会有什么问题。塑料砧板和原木砧板，也都是用料问题。而个人更喜欢原木砧板，只要木料选择的好，后续省心不少，防止霉变不会有异味，硬度好不会产生碎屑等等。但因为国产品牌里很少有大牌背景的砧板，这样也造成用户对于品质的担忧。而随着用户品质需求的提高，其实也不乏优质品牌。\t家里的菜板用着还顺心吧😄😄 : 菜板是加厚的，面板平滑，没有裂缝，邻居用这个剁鸡剁肉的都挺好。尺寸可以随自己选择。\n    问题为：\n    菜板的选择应该考虑哪些因素？\n    你的回答为：\n    ", "answer": "选择菜板应该考虑以下因素：首先是菜板的材质，不同材质的菜板有不同的特点和适用场景，如木质菜板柔软不伤刀，树脂菜板有良好的弹性和形变恢复率，而钢质和玻璃质菜板由于硬度过高容易伤刀，故不建议购买。其次是品牌，要选择有信誉的品牌，以确保菜板的材质安全、无有害残留物。然后是尺寸和厚度，这需要根据个人的需求来选择，大尺寸的菜板适合处理大量食材，小尺寸的菜板适合小家庭使用，厚度一般在1.5-2.5厘米之间。最后，还要考虑菜板的加工工艺和胶水使用，这关系到菜板的质量和耐用性。同时，正确使用和保养菜板也可以延长其使用寿命，提高使用体验。"}

```



## 🔍How to use EcomEval

### 1. installation

```
git clone https://github.com/guankaisi/EcomEval
cd EcomEval
pip install -r requirements.txt
```

### 2. Start Eval 

```bash
bash run_eval.sh
```

For the `run_eval.sh` ,

```
CUDA_VISIBLE_DEVICES=0 python ecom_eval.py \
    --model_path model_path \
    --dtype bfloat16 \
    --save_result True \
    --batch_size 4 \
    --tasks ['ie','cls','gen','rag']
```

## 📋Related Works

[EcomGPT AAAI 2024]([Alibaba-NLP/EcomGPT: An Instruction-tuned Large Language Model for E-commerce (github.com)](https://github.com/Alibaba-NLP/EcomGPT))

[Ecellm ICML 2024]([eCeLLM (ninglab.github.io)](https://ninglab.github.io/eCeLLM/))

[BSharedRAG]([BSharedRAG: Backbone Shared Retrieval-Augmented Generation for the E-commerce Domain](https://bsharedrag.github.io/index.html))

[OpenBG：Large Scale Open Business Knowledge Graph]([OpenBGBenchmark/OpenBG: Datasets for Evaluation on Domain Knowledge Graph (github.com)](https://github.com/OpenBGBenchmark/OpenBG))

## 👀Citation

