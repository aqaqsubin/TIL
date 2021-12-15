## **DeBERTa 논문 리뷰** (12월 15일~🏃‍♀️)

### [📄**Paper**](https://openreview.net/pdf?id=XPZIaotutsD)  
P. He, X. Liu, J. Gao, W. Chen, "Deberta: decoding-enhanced bert with disentangled attention," _Proc. of the 9th International Conference on Learning Representations (ICLR 2021)_, Online, 2021.

### **📌 목차** 

1. Introduction
2. Background   
    2.1 Transformer   
    2.2 Masked language model    
3. The DeBERTa architecture  
    3.1 Disentangled attention: A two-vector approach to content and position embedding   
    3.2 Enhanced mask decoder accounts for absolute word positions    
4. Scale invariant fine-tuning   
5. Experiment
    5.1 Main results on NLU tasks     
    5.2 Model analysis  
    5.3 Scale up to 1.5 billion parameters  
6. Conclusions  

---

### **1. Introduction**

트랜스포머에 기반한 Pretrained Language Model(PLM)이 많은 NLP task에서 SOTA를 달성하고 있다.  

본 논문에서는 *Disentangled Attention mechanism*과 *Enhanced Mask Decoder*를 통해 새로운 SOTA를 달성한 DeBERTa 모델을 제안하였다.      

- **✨ Disentangled Attention mechanism**  
단어 간 attention weight는 내용 뿐만 아니라 위치 정보도 상당한 영향을 끼치기 때문에   
Content와 Relative Position 정보를 2개의 벡터로 분리하여 Cross Attention 수행  

- **✨ Enhanced Mask Decoder**  
문법적 뉘앙스는 단어의 상대적 위치 정보가 아닌 절대적 위치 정보에 영향을 받는다.  
문법적 뉘앙스를 파악하기 위해 디코딩 시, absolute position embedding을 취합하여 사용한다.    

또한 본 논문에서는 perturbation에 대한 robustness를 개선하면서 안정된 성능을 보이는 *SiFT algorithm*도 함께 제안하였다.  

<div align=center>
<img src="../img/DeBERTa/position.jpeg" width=500/><br>
Relative position vs Absolute position</div>
<br>

#### **☀️ 개선한 내용**
1. 사전학습 효율  
사전 학습 데이터가 적어도 성능 우수 

2. NLU, NLG task에서의 SOTA

<br>

### **2. Background**

#### **2.1 Transformer**  
기존의 Transformer는 입력 sentence가 matrix로 들어가기 때문에, 순차 정보를 포함하지 않는다.  
따라서 Positional Embedding을 통해 위치 정보를 포함시키는데, 
이러한 위치 정보는 다음 두 가지로 구분될 수 있다.  
- Absolute Position  
- Relative Position 

Shaw et al. (2018)의 연구에 따르면 Relative position 정보가 NLU/NLG task에 더 효과적이라고 밝혀졌다.


#### **2.2 Masked language model**

Transformer에 기반한 PLM은 대부분 MLM task로 사전학습을 수행한다.  
전체 시퀀스의 15%를 마스킹한 $\tilde{X}$가 주어졌을 때, 이를 복원한 $X$를 예측하도록 학습한다

$$
\max_\theta \log{p_\theta(X|\tilde{X})} = \max_\theta \sum_{i\in \mathcal{C}} \log{p_\theta (\tilde{x_i}= x_i|\tilde{X})}
$$
where $\mathcal{C}$는 masking 된 단어의 index 리스트 


### **3. The DeBERTa architecture**  

#### **3.1 Disentangled attention: A two-vector approach to content and position embedding**

<br>

$\{H_i\}$ : i번쩨 token에 대한 content vector   
$\{P_{i|j}\}$ : i번째 token에서 j번째 token에 대한 relative position vector 


content와 position에 대한 벡터를 분리했을 때 Cross attention score 계산은 아래와 같이 4개의 컴포넌트에 대한 덧셈으로 분리될 수 있다.

$$
A_{i,j} = \{H_i, P_{i|j}\} \times  \{H_j, P_{j|i}\}^\intercal
$$
$$
= H_iH^\intercal_j + H_iP^\intercal_{j|i} + P_{i|j}H^\intercal_j + P_{i|j}P^\intercal_{j|i}
$$

각각을 *content-to-content*, *content-to-position*, *position-to-content*, *position-to-position* 로 나타낼 수 있다

> 💡 본 논문에서는 상대적인 위치 정보를 사용하기 때문에, position-to-position term은 필요 없어 제외하여 계산하였다.


아래는 relative position 정보를 임베딩하여 attention을 적용한 기존 Shaw et al. (2018) 연구에서의 Attention score 계산 식으로,   
*content-to-content*, *content-to-position*로 구성되어 있다. 

<div align=center>
<img src="../img/DeBERTa/shaw_attn_score.jpeg" width=500/></div>

본 논문에서는 relative position 정보를 저장하기 위해 $\delta$ 함수를 사용했는데,  
$N$개의 시퀀스에 대해 모든 상대적 위치 정보를 저장하지 않고 상한선을 두어 $k$ 거리까지만 저장한다 

<div align=center>
<img src="../img/DeBERTa/eq_3.jpeg" width=500/></div>
<br>

> 💡 **공간 복잡도(Space Complexity) 감소**    
> 
> 위와 같이 $\delta$ 함수를 통해 모든 relative position을 0~$2k$로 매핑했기 때문에 $Q, K$을 재사용할 수 있으며,  
N개의 query 시퀀스에 대한 relative position embedding을 새로 할당하지 않아도 되기 때문에 space complexity가 $O(N^2d)$에서 $O(kd)$로 감소하였다.
> 

<br>

<div align=center>
<img src="../img/DeBERTa/eq_4.jpeg" width=900/><br>
Attention Output 계산 과정</div>
<br>

> 💡 **$\delta(i,j)$가 아닌 $\delta(j,i)$인 이유**  
>
> 해당 term은 position-to-content term이며,   
> 주어진 query position i에 대한 j번째 token의 key content의 attention weight를 연산해야 한다    
> ***content-j, position-i***

Attention score 연산이 끝나면 scaling 수행    
→ large scale의 PLM을 안정적으로 학습시킬 수 있다

<br>

#### **3.2 Enhanced mask decoder accounts for absolute word positions**

위의 Disentangled Attention mechanism은 absolute position을 고려하지 않는다.  
하지만 절대 위치 정보는 문법적 측면에서 필요한 요소이기 때문에, EMD (Enhanced Mask Decoder)에서 Absolute position embedding을 취합한다. 




### **4. Scale invariant fine-tuning**

### **5. Experiment**

#### **⑴ Neural Abstractive Summarization**   

#### **⑵ Guidance**   


### **6. Conclusions**

----

### **Appendix**