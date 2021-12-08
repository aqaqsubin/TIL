## **GPT-3를 이용한 챗봇**

GPT-3는 OpenAI가 발표했던 'Language Models are Few-Shot Learners' 논문에서 제안된 모델이다.  

사전 학습된 모델을 이용한 NLP task가 큰 성과를 거두고 있지만,  
어떤 특정 도메인에 적용하기 위해서는 많은 양의 데이터, fine-tuning strategies 등 최적화된 fine-tuning이 필요하다는 문제점이 있었다.  

GPT-3는 특정 도메인에 대한 데이터, fine-tuning이 따로 없어도 few-shot learning을 통해 특정 task에 적용이 가능하다.  

아래는 inference 시, 수행하려는 task에 대한 description과 예시와 같은 demonstration을 제공함으로써  
Chatbot task를 수행하는 예시이다.  

_본 실험은 kakaobrain 레포에서 공개한 [KoGPT-3](https://github.com/kakaobrain/kogpt) 모델을 사용하였습니다._


```python
# Package Requirements

torch==1.9.0
transformers==4.12.0
```

16개의 직접 생성한 대화 예시를 사용
```python
DESCRIPTION= '한국어 대화 채팅 시스템'


examples = [
        {
            "Q" : "꼬북칩 지금 gs에 있겠지?!? 먹고시포..",
            "R" : "편의점에 백퍼 잇지!!"
        },
        {
            "Q" : "혹시 집에 슈가파우더 있어? 마카롱 만들어줄깡",
            "R" : "그건 있는데 아몬드가루 없어서 불가능"
        },
        {
            "Q" : "너도 내가 한심하다고 생각해..?",
            "R" : "아니!! 절대 한심하다고 생각하지 않아ㅠ"
        },
        {
            "Q" : "이거 개귀엽징ㅠㅠ",
            "R" : "귀엽넹ㅎㅎ"
        },
        {
            "Q" : "나 저녁 뭐먹지 다욧투해야되는데",
            "R" : "음 그냥 샐러드??"
        },
        {
            "Q" : "혹시 뭐 필요한거 없어?",
            "R" : "있어! 마트 들러서 올거야?"
        },
        {
            "Q" : "그래놀라 짱맛있다",
            "R" : "후 맛있다니 다행이구만"
        },
        {
            "Q" : "날씨 왜이래",
            "R" : "오늘 날씨 괜찮다던데??"
        },
        {
            "Q" : "미쳣다미쳣어 뿌링클 개맛있다ㅜㅠ",
            "R" : "맛나게 무라!!!"
        },
        {
            "Q" : "우울하다 우우래",
            "R" : "왜 우우래ㅠㅠ 뭔일 있어~?"
        },
        {
            "Q" : "오늘 무슨일 있었엉?! 왤케 우울해해ㅠ",
            "R" : "그냥 오늘 실수해서 좀 혼나쏘.. 또 넘 바쁘구"
        },
        {
            "Q" : "하 집에가고 싶다~~~야자 시러~~",
            "R" : "나두ㅠㅜ 집이 최고야"
        },
        {
            "Q" : "하 그냥 일하기 싫은건가봐",
            "R" : "맘이 떴구나... 나돈데 허허허"
        },
        {
            "Q" : "배고프당... 배달 시킬까",
            "R" : "먹으려면 빨리시켜~~~"
        },
        {
            "Q" : "다른건 다 괜찮은데 좀 추워",
            "R" : "ㅠㅠ헐... ㅠㅠ 옷 따뜻하게 입엉.."
        },
        {
            "Q" : "어때~! 멋지지?!!!",
            "R" : "참 부럽구만?!"
        }
    ]

```


```python
def chat(model, examples, tokenizer, device):
    def _is_valid(query):
        if not query or query == "c":
            return False
        return True

    query = input("Q: ")
    examples_len = len(examples)

    while _is_valid(query):
        # 16개의 대화 예시와 description을 이어붙여 prompt 생성
        prompt = get_prompt(examples) + f'#Q:{query}#R:'

        tokens = tokenizer.encode(prompt, return_tensors='pt').to(device=device, non_blocking=True)
        gen_tokens = model.generate(tokens, do_sample=True, temperature=0.8, max_length=tokens.size(1)+100)
        generated = tokenizer.batch_decode(gen_tokens)[0]
        
        # reply 파싱
        reply = get_reply(entire_dialogue=generated, examples_len=examples_len)
        print(f"R: {reply}")

        # 대화 예시 업데이트
        cur_turn = {
            "Q" : query,
            "R" : reply
        }
        examples = examples[1:] + [cur_turn]

        query = input("Q: ")
    return
```

대화 생성 결과  
대화 예시로 다이어트를 집어넣었더니 다이어트 얘기만 나온다 🤦‍♀️

```bash

Q: 안녕?
R: 어 안녕~

Q: 배고프당 치킨 땡겨
R: 다욧트하는데 치킨이 왜 나와!!!

Q: 너무해ㅠ 배고픈디...
R: 나도 다요트 한다...

Q: 너가 다이어트를 왜해~!
R: 나도 다요트 하니까

```

## **리뷰 🧐**

GPT는 문어체의 문장을 이어쓰는 데 특화되어 있다고만 생각했는데,  
finetuning이 없이도 task 지정과 예시를 제공하니 구어체로 대화하는게 신기했다 👏👏

위의 reply는 생성된 문장에서 파싱을 통해 추출한 것이고,  
모델에 의해 생성된 결과는 흡사 멀티턴 대화 데이터를 보는 것 같았다  
(max_length를 늘려야 한다)



