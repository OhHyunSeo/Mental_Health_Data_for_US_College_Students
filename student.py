#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 21:22:41 2025

@author: oh

대학생의 인구통계학적 정보, 학업과 관련된 요소, 정신 건강과 관련된 요소 등을 분석하여

학생들의 정신 건강에 영향을 미치는 요인을 파악!


대학생들에게 있어 정신 건강은 매우 중요!

특히 익숙했던 생활과는 다르게 대학에 입학하면서 정서적, 정신적 긴장을 겪게 된다.

따라서 학생들의 정신 건강에 영향을 미치는 요인이 무엇인지를 분석하여 해결 방안을 제시!!!



제출 메일 주소 : aiffall@naver.com

메일 제목 : 20250222~23 주말과제 OOO (본인이름)

메일 내용 : 분석 결과 및 해결 방안

첨부 파일 : 작업 프로젝트 및 시각화 자료

               시각화 자료는 result 폴더에 저장하여 작업프로젝트를 압축하여 제출
"""
'''
단계 설정
1. 데이터 불러오기
2. 데이터의 정보 확인
3. 데이터 전처리
    3.1 Age 결측치 처리
    3.2 year 대소문자 통일, 학점(CGPA)의 결측치 처리   
    
4. 정신 건강에 관련된 요인 분석
    4.1 카테고리변 정신 건강 문제 발생 비율 확인

5. 시각화 및 인사이트 도출
'''
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'AppleGothic'

# 1. 데이터 불러오기
df = pd.read_csv("./data/Student Mental health.csv")

# 2. 데이터의 정보 확인
df.info()
'''
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 101 entries, 0 to 100
Data columns (total 11 columns):
 #   Column                                        Non-Null Count  Dtype  
---  ------                                        --------------  -----  
 0   Timestamp                                     101 non-null    object 
 1   Choose your gender                            101 non-null    object 
 2   Age                                           100 non-null    float64 <- 널값 존재
 3   What is your course?                          101 non-null    object 
 4   Your current year of Study                    101 non-null    object 
 5   What is your CGPA?                            101 non-null    object 
 6   Marital status                                101 non-null    object 
 7   Do you have Depression?                       101 non-null    object 
 8   Do you have Anxiety?                          101 non-null    object 
 9   Do you have Panic attack?                     101 non-null    object 
 10  Did you seek any specialist for a treatment?  101 non-null    object 
dtypes: float64(1), object(10)
memory usage: 8.8+ KB
'''

# 결측치 확인
df.isna().sum()
'''
Timestamp                                       0
Choose your gender                              0
Age                                             1
What is your course?                            0
Your current year of Study                      0
What is your CGPA?                              0
Marital status                                  0
Do you have Depression?                         0
Do you have Anxiety?                            0
Do you have Panic attack?                       0
Did you seek any specialist for a treatment?    0
dtype: int64
'''
df.shape

# 3. 데이터 전처리
# Age 행중 하나에 결측치 발견, 해당값을 Age의 중앙값으로 변경
# 결측치가 존재하는 행 삭제 후 진행
age_mean = df["Age"].mean()
# 20.53

age_median = df["Age"].median()
# 19.0

# Age의 결측치 값을 중앙값으로 변경
df["Age"].fillna(19, inplace = True)

# 우울증, 불안, 공황 발작등이 정신 건강 문제를 가졌다고 볼 수 있음

# 정신 건강 관련 문제 비율 확인 (정신 건강 관련 칼럼들을 파악)
mental_health_issues = df[["Do you have Depression?", 
                           "Do you have Anxiety?", 
                           "Do you have Panic attack?"]].apply(lambda x: (x == "Yes").mean())

mental_health_issues

'''
Do you have Depression?      0.346535
Do you have Anxiety?         0.336634
Do you have Panic attack?    0.326733
dtype: float64
'''

# 4. 성별과 정신 건강 문제의 관계 분석

# 4-1. 성별에 따른 정신 건강 문제 비율 분석
gender_analysis = df.groupby("Choose your gender")[["Do you have Depression?", 
                                                    "Do you have Anxiety?", 
                                                    "Do you have Panic attack?"]].apply(lambda x: (x == "Yes").mean())

gender_analysis.head()
'''
                    Do you have Depression?  ...  Do you have Panic attack?
Choose your gender                           ...                           
Female                             0.386667  ...                   0.333333
Male                               0.230769  ...                   0.307692
'''
'''
여성
    1. 우울증 38%
    2. 불안 32%
    3. 공황 발작 33%
    
남성
    1. 우울증 23%
    2. 불안 38%
    3. 공황 발작 30%
    
결론 : 
    - 여성이 남성보다 우을중을 더 많이 경험
    - 남성이 여성보다 불안을 더 많이 경험
    - 공황 발작 비율은 크게 차이가 나지 않음
'''

# 4-2. 학년별 정신 건강 문제의 관계 분석
# 학년 데이터를 소문자로 변환하여 통일
df["Your current year of Study"] = df["Your current year of Study"].str.lower()

# 학년별 정신 건강 문제 
year_analysis_cleaned = df.groupby("Your current year of Study")[["Do you have Depression?", 
                                                                  "Do you have Anxiety?", 
                                                                  "Do you have Panic attack?"]].apply(lambda x: (x == "Yes").mean())

year_analysis_cleaned.head()
'''
                            Do you have Depression?  ...  Do you have Panic attack?
Your current year of Study                           ...                           
year 1                                     0.325581  ...                   0.325581
year 2                                     0.384615  ...                   0.307692
year 3                                     0.416667  ...                   0.416667
year 4                                     0.125000  ...                   0.125000
'''
'''
1학년
    1. 우울증 32%
    2. 불안 32%
    3. 공황 발작 32%
2학년
    1. 우울증 38%
    2. 불안 38%
    3. 공황 발작 32%
3학년
    1. 우을증 41%
    2. 불안 33%
    3. 공황 발작 41%
4학년
    1. 우울증 12%
    2. 불안 25%
    3. 공황 발작 12%
    
결론 :
    - 1학년과 2학년의 우울증 및 불안 비율이 상대적으로 높음
    - 3학년에서 우울증과 공황 발작 비율이 가장 높음
    - 4학년의 정신 건강 문제 비율이 가장 낮음
'''

# 4-3. 나이별 정신 건강 문제의 관계 분석
# 나이별 정신 건강 문제 비율 분석
age_analysis = df.groupby("Age")[["Do you have Depression?", 
                                  "Do you have Anxiety?", 
                                  "Do you have Panic attack?"]].apply(lambda x: (x == "Yes").mean())

age_analysis.head()
'''
      Do you have Depression?  Do you have Anxiety?  Do you have Panic attack?
Age                                                                           
18.0                 0.343750              0.437500                   0.281250
19.0                 0.409091              0.227273                   0.409091
20.0                 0.500000              0.500000                   0.166667
21.0                 0.000000              0.666667                   0.000000
22.0                 0.500000              0.000000                   0.000000
'''
# 18세 ~ 24세 까지 분석
'''
- 20세와 22세에서 우울증 비율이 50%로 가장 높음
- 21세에서 불안 비율이 가장 높음(66%)
- 공황 발작은 19세(40%)와 23~24세에서 높은 비율을 보임
'''

# 5. 시각화 진행 및 결론 도출

# 5-1. 성별 정신 건강 문제
# 컬럼명 통일 (성별 컬럼 이름 변경)
df.rename(columns={"Choose your gender": "Gender"}, inplace=True)

# 정신 건강 데이터 (Yes → 1, No → 0 변환)
mental_health_cols = ["Do you have Depression?", 
                      "Do you have Anxiety?", 
                      "Do you have Panic attack?"]
df[mental_health_cols] = df[mental_health_cols].applymap(lambda x: 1 if x == "Yes" else 0)

df[mental_health_cols].describe()

plt.figure(figsize=(12, 5))
df.groupby("Gender")[mental_health_cols].mean().plot(kind="bar", figsize=(10, 6), colormap="coolwarm")
plt.title("성별에 따른 정신 건강 문제 비율")
plt.ylabel("비율")
plt.xticks(rotation=0)
plt.legend(["우울증", "불안", "공황 발작"])

plt.savefig("./result/gender")

plt.show()

# 5-2. 학년별 시각화
# 학년 컬럼 이름 변경
df.rename(columns={"Your current year of Study": "Year"}, inplace=True)

plt.figure(figsize=(12, 5))
df.groupby("Year")[mental_health_cols].mean().plot(kind="bar", figsize=(10, 6), colormap="coolwarm")
plt.title("학년에 따른 정신 건강 문제 비율")
plt.ylabel("비율")
plt.xticks(rotation=0)
plt.legend(["우울증", "불안", "공황 발작"])

plt.savefig("./result/year")

# 5-3. 나이별 시각화


plt.figure(figsize=(12, 5))
df.groupby("Age")[mental_health_cols].mean().plot(kind="bar", figsize=(10, 6), colormap="coolwarm")
plt.title("나이에 따른 정신 건강 문제 비율")
plt.ylabel("비율")
plt.xticks(rotation=0)
plt.legend(["우울증", "불안", "공황 발작"])

plt.savefig("./result/age")

'''
결론
성별의 경우, 
    여학생이 남학생보다 전체적인 정신건강 문제 비율의 정도는 높음.
    하지만 불안의 경우 남학생이 여학생보다 높게 나옴.
    
학년의 경우,
    3학년이 모든 학년을 통틀어 전체적인 정신건강 문제 비율이 높음
    이는 곧 졸업을 앞둔 학생들의 스트레스가 반영되었다고 해석할 수 있음
    또한 4학년의 경우 3가지 (우울증, 불안, 공황 발작)의 요소가 모두 낮게 나왔는데,
    이는 다른 학기의 마무리를 앞둔 시기로서 다른 학년들 보단 자신의 진로나 미래를 어느정도
    결정한 상태에서 나오는 결과라고 해석할 수 있
    또한 갓 입학한 1학년들의 경우 3가지 스트레스 요소가 골고루 높게 나옴으로써 신입생으로서
    학교 적응에 스트레스를 가지고 있다는 것을 알 수 있다.
    
나이의 경우,
    18세부터 24세까지의 데이터가 있으며, 21세와 22세는 각각 하나의 요소만 나온것을 보아
    데이터 전처리가 원활히 이루어지지 않거나 응답자 수가 적다는 것을 유추해볼 수 있

    18세부터 24세까지 전반적인 스트레스 비율을 비슷하게 나오나,
    20세, 25세에서 각각 공황 발작, 불안 요소가 상대적으로 낮게 나옴
    또한 18세는 3가지 요소가 모두 높게 나왔는데 이는 대학에 처음 입학한 신입생으로서 긴장감을 
    가지고 있어 여러한 스트레스 요인을 모두 가지고 있음을 알 수 있

해결방안
    - 1. 취업을 앞둔 3학년 학생들과 신입생들에게 각자에게 맞는 상담이나, 스트레스 관리법의 
    솔루션을 진행한다.
    - 2. 나이별 스트레스 요인을 긴밀히 분석후 3가지 요소에 알맞는 해결책을 제시한다.
    

'''

























