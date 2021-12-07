## **Facebook의 Poly-Encoder 논문 리뷰** (12월 7일~🏃‍♀️)

### [📄**Paper**](https://openreview.net/pdf?id=SkxgnnNFvH)  
Humeau, S., Shuster, K., Lachaux, M. A., and Weston, J., “Poly-encoders: architectures and pre-training strategies for fast and accurate multi-sentence scoring,” _Proc. of the 8th International Conference on Learning Representations (ICLR 2020)_, Addis Ababa, Ethiopia, 2020.

### **📌 목차** 

1. Introduction
2. Related work  
3. Tasks
4. Methods  
    4.1 Transformers and Pre-training Strategies  
    4.2 Bi-encoder  
    4.3 Cross-encoder  
    4.4 Poly-encoder
5. Experiments  
    5.1 Bi-encoders and Cross-encoders     
    5.2 Poly-encoders  
    5.3 Domain-specific pre-training  
    5.4 Inference speed  
6. Conclusion  

---

### **1. Introduction**

기존의 pairwise comparision task를 해결하기 위한 Cross-encoder, Bi-encoder 접근방식의 성능 개선한 new Transformer architecture _Poly-encoder_ 제안  

**Poly-enocder**
- Cross-encoder의 추론 시간 개선
- Bi-encoder의 prediction quality 개선

**4가지 데이터셋에서의 Poly-encoder성능 검증**  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dialogue 및 Information Retrieval (IR) 도메인에 대한 데이터셋에서 성능 검증  

### **2. Related work**

1. Bi-encoder  
Input과 candidate label을 같은 공간 상에 매핑한 후 유사도를 비교함으로써 scoring  
vector space model, LSI, supervised embeddings, classical siamese networks 등이 있음  
<br>
**next utterance prediction**에도 Memory Networks, Transformer Memory networks, LSTMs, CNNs와 같이   
input과 candidate label을 따로 인코딩하는 Bi-encoder approach가 사용되었다.   
<br>
input과 candidates를 각각 따로 임베딩하기 때문에, candidates를 저장하여 재사용할 수 있다는 장점이 있다.  
→ candidate를 다시 임베딩할 필요가 없기 때문에 추론 시간이 빨라짐

2. Cross-encoder  
Input과 candidate를 이어붙여(concatenation) 하나의 입력으로 사용하며, non-linear function에 의해 scoring 된다.  
Sequential Matching Network CNN-based architecture, Deep Matching Networks, Gated Self-Attention 등이 있다.    
<br>
가장 최신 transformer를 이용한 Cross-encoder approach는 각 layer에 self-attention을 적용한 결과를 내며,   
input과 candidate 간의 interaction을 극대화한다. (candidate 내 word는 input 내 모든 word에 attend 할 수 있음)  

> Urbanek et al. (2019)의 연구에서는 사전학습된 BERT를 통한 Cross-encoder와 Bi-encoder의 성능을 비교했으며,  
Cross-encoder의 접근 방식이 성능이 더 뛰어나지만 추론 시간 면에서는 뒤쳐졌다.

<br>

### **3. Tasks**

다음 두 가지 도메인에서 사용되는 데이터셋을 통해 본 연구에서 제안하는 Poly-encoder 성능을 검증하였다.  

**Sentence Selection in Dialogue**

- ConvAI2 dataset  
대화 데이터로, 각 발화자에 대한 페르소나의 정보가 함께 담겨있다.
<div align=center>
<img src="../img/PolyEncoder/conv2ai_dataset.png" width=500/>
</div>
<br>

- DSTC7 dataset (Track 1)  
Ubuntu Chat log로부터 추출한 대화 데이터   
DSTC7 challenge에서 우승한 팀은 64.5% R@1를 달성하였다.  

- Ubuntu V2  
위와 비슷하지만 더 큰 사이즈의 corpus를 가짐    

**Article search in Information Retrieval**  
- Wiki Article Search   
약 5M의 article을 포함하며, 어떤 article 내 sentence가 주어지면 article을 찾는 task를 수행하는 데이터셋이다  
다른 1만개의 기사들 사이에서 실제 기사의 순위를 통해 검증한다.    

<div align=center>
데이터셋 비교<br>
<img src="../img/PolyEncoder/table_1.png" width=800/>
</div>
<br>

### **4. Methods**

#### **4.1 Transformer and pre-training strategies**
#### **4.2 Bi-encoder**
#### **4.3 Cross-encoder**
#### **4.4 Poly-encoder**


### **5. Experiments**

### **6. Conclusion**

---

### **Appendix**  

#### **A. Training time**  

#### **B. Reduction layer in Bi-encoder**  

#### **C. Alternative choices for context vectors**