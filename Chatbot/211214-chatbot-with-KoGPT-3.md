## **GPT-3를 이용한 챗봇**

_본 실험은 kakaobrain 레포에서 공개한 [KoGPT-3](https://github.com/kakaobrain/kogpt) 모델을 사용하였습니다._


```python
# Package Requirements

torch==1.9.0
transformers==4.12.0
```
8일날 진행했던 KoGPT-3을 이용한 챗봇 구현을 이어서 수행한 내용

**기존의 대화 Prompt**  
```python
examples = [
        {
            "Q" : "친구가 나를 자꾸 놀려..", # 1
            "R" : "뭐?! 뭐라고 놀려!! 가만안둬"
        },
        {
            "Q" : "애들도 자꾸 살쪘다고 놀려ㅠ", # 2
            "R" : "뭐가 살쪄~ 하나도 안쪘어"
        },

        # 생략
        {
            "Q" : "이제 시험 끝났다! 홀가분해", # 33
            "R" : "너무 고생했어~~ 이제 푹 쉬어!"
        },
    ]
```

위는 학교 생활에 대한 대화 예시로 수정한 것이고,  
아래는 그에 대한 대화 예시이다.  

대화가 단조롭고, 응답 생성을 제어할 수 없다는 단점이 있다 

```bash
Query : 나 학교에서 왕따야
Reply : 헐... 어떻게 하지...?

Query : 나도 모르겠어 학교가기 싫어
Reply : 너무 힘드네 어떡하지?

Query : 학교 가지 말까?
Reply : 야 그래도 학교는 가야지~

Query : 너무 힘들어 죽고싶어
Reply : 다들 힘들어하네 우리 힘내자!
```

**Prompt 수정**    

응답의 종류는 질문, 공감, 위로, 조언으로 분류하여 각각의 응답을 생성하도록 prompt 작성   
24개의 직접 생성한 대화 예시를 사용

```python
DESCRIPTION= '# 고민을 들어주고 상대방의 기분을 파악하여 공감해주는 대화 내용'


examples = [
        {
            "Q" : "친구가 나를 자꾸 놀려..", # 1
            "Open-Question" : "뭐라고 놀렸는데??",
            "Empathize" : "왜 놀려!! 속상하게ㅠㅠ",
            "Comporting" : "틀림 없이 별 뜻없이 그런걸거야",
            "Feedback" : "놀리는거 자꾸 받아주지마! 화낼땐 화내야해"

        },
        {
            "Q" : "애들도 자꾸 살쪘다고 놀려ㅠ", # 2
            "Open-Question": "어떻게 놀렸길래ㅠㅠ",
            "Empathize" : "에구 속상했겠다ㅠㅠ",
            "Comporting" : "뭐가 살쪄~ 하나도 안쪘어",
            "Feedback" : "그럼 너도 받아쳐! 무슨 상관이냐고~"

        },

        # 생략
        {
            "Q" : "나 다이어트 끝났어~~~", # 24
            "Open-Question": "몇 키로 빠졌어?",
            "Empathize" : "고생했다ㅠㅠ 다이어트 끝나고 먹는 치킨이 짱이지",
            "Comporting" : "오오 잘했네ㅎㅎ 고생했어~",
            "Feedback" : "이제 맛있는거 많이 먹엉~! "
        }
    ]

```

하나의 질문에 대해 4가지 유형의 응답이 모두 달리도록 prompt 구성
```python
def get_prompt(turns):
    prompt= DESCRIPTION
    for turn in turns:
        turn = f"Q:{turn['Q']}\n질문:{turn['Open-Question']}\n공감:{turn['Empathize']}\n위로:{turn['Comporting']}\n조언:{turn['Feedback']}"
        prompt += "\n@" + turn
    return prompt
```


예시로 작성한 prompt가 너무 길어서 10개의 예시만 사용했다  
아래의 생성 예시와 같이 각각의 목적에 맞지 않는 응답이 나왔다

```bash
Query : 나 학교에서 왕따야

Open-Question : 왜 왕따야??
Empathize : 자꾸 말걸잖아! 너무 속상해졌어
Comporting : 내가 도와줄 수 있는 건 없을까?
Feedback : 친구들한테 먼저 다가가봐~

Query : 내가 친구들한테 먼저 다가가도 애들이 피해

Open-Question : 나는 항상 혼자 있어야해...
Empathize : 무슨 일 있었어?
Comporting : 걱정하지마! 친구들이 나중에 먼저 다가와주지 않을까?
Feedback : 친구들하고 친해질 수 있는 기회가 있을 거야~
```



## **리뷰 🧐**

2021 DEVIEW를 보고 아이디어를 생각해본 것인데, 하나의 질의에 대해 여러가지 목적의  응답을 각각 생성할 수 있지 않을까 했다,  

각각의 포지션에 해당하는 목적을 학습하기 위해서는 더 많은 예시나 각 목적의 feature에 대한 패턴을 모델이 파악할 수 있도록 prompt를 더 정교하게 짜야 할 것 같다


