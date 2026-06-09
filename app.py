
import streamlit as st
import random
import time

st.set_page_config(
    page_title="EcoQuest RPG Edition",
    page_icon="🌱",
    layout="wide"
)

# =========================
# 직업 데이터
# =========================

jobs = {

    "meat": {
        "job":"⚔️ 탄소 절감 버서커",
        "sprite":"images/berserker_pixel.png",
        "title":"붉은 초원의 전사",
        "quote":"고기를 포기할 필요는 없다. 더 현명하게 먹으면 된다.",

        "attack":95,
        "recovery":60,
        "eco_power":40,

        "base_score":40,

        "before":"소고기덮밥",
        "after":"닭가슴살 비빔밥 + 버섯볶음",

        "before_carbon":8.0,
        "after_carbon":3.5,

        "meals":[
            "닭가슴살 비빔밥",
            "버섯고기비빔밥",
            "두부불고기덮밥"
        ],

        "tips":[
            "소고기보다 닭고기 선택",
            "버섯·두부 추가",
            "주 1~2회 대체식 실천"
        ]
    },

    "instant": {
        "sprite":"images/ranger_pixel.png",
        "job":"🏹 제로웨이스트 레인저",
        "title":"질주의 추적자",
        "quote":"빠른 선택도 좋은 방향으로 바꿀 수 있다.",

        "attack":70,
        "recovery":55,
        "eco_power":50,

        "base_score":45,

        "before":"컵라면 + 소시지",
        "after":"채소김밥 + 두유",

        "before_carbon":4.5,
        "after_carbon":1.8,

        "meals":[
            "채소김밥",
            "두부유부초밥",
            "오트밀볼"
        ],

        "tips":[
            "채소 추가",
            "가공육 줄이기",
            "두유 선택"
        ]
    },

    "vegetable": {
        "sprite":"images/druid_pixel.png",
        "job":"🌿 숲을 지키는 드루이드",
        "title":"숲의 수호자",
        "quote":"작은 선택이 숲을 지키는 힘이 된다.",

        "attack":55,
        "recovery":95,
        "eco_power":100,

        "base_score":75,

        "before":"채소비빔밥",
        "after":"렌틸콩 비빔밥",

        "before_carbon":2.5,
        "after_carbon":2.0,

        "meals":[
            "병아리콩샐러드",
            "두부샐러드",
            "렌틸콩카레"
        ],

        "tips":[
            "단백질 보완",
            "제철채소 활용",
            "영양 균형 유지"
        ]
    },

    "dessert": {
        "sprite":"images/alchemist_pixel.png",
        "job":"✨ 친환경 연금술사",
        "title":"달콤한 연구가",
        "quote":"즐거움과 건강은 함께 갈 수 있다.",

        "attack":50,
        "recovery":70,
        "eco_power":65,

        "base_score":55,

        "before":"커피 + 초콜릿",
        "after":"두유 바나나 스무디",

        "before_carbon":3.2,
        "after_carbon":1.4,

        "meals":[
            "과일샐러드",
            "오트밀 초코볼",
            "바나나 오트 쿠키"
        ],

        "tips":[
            "탄산 대신 물",
            "과일 활용",
            "빈도 조절"
        ]
    }
}

# =========================
# 식단 재료
# =========================

meal_ingredients = {

    "닭가슴살 비빔밥":["닭고기","쌀"],
    "버섯고기비빔밥":["소고기","버섯"],
    "두부불고기덮밥":["두부"],

    "채소김밥":["오이","당근"],
    "두부유부초밥":["두부"],
    "오트밀볼":["귀리"],

    "병아리콩샐러드":["병아리콩"],
    "두부샐러드":["두부"],
    "렌틸콩카레":["렌틸콩"],

    "과일샐러드":["사과","바나나"],
    "오트밀 초코볼":["귀리"],
    "바나나 오트 쿠키":["바나나"]
}

recipes = {

    "닭가슴살 비빔밥":
    """
    재료
    - 닭가슴살 100g
    - 밥 1공기
    - 시금치
    - 당근
    - 버섯

    만드는 법
    1. 닭가슴살을 구워 한입 크기로 자른다.
    2. 시금치, 당근, 버섯을 볶는다.
    3. 밥 위에 재료를 올린다.
    4. 고추장이나 간장 소스를 곁들여 비벼 먹는다.
    """,

    "버섯고기비빔밥":
    """
    재료
    - 소고기 80g
    - 버섯
    - 밥 1공기
    - 시금치

    만드는 법
    1. 소고기를 양념해 볶는다.
    2. 버섯과 시금치를 함께 볶는다.
    3. 밥 위에 재료를 올린다.
    4. 잘 비벼서 먹는다.
    """,

    "두부불고기덮밥":
    """
    재료
    - 두부 1모
    - 밥 1공기
    - 양파
    - 버섯

    만드는 법
    1. 두부를 물기 제거 후 구운다.
    2. 양파와 버섯을 볶는다.
    3. 간장 양념을 넣고 함께 조리한다.
    4. 밥 위에 올려 덮밥으로 완성한다.
    """,

    "채소김밥":
    """
    재료
    - 김
    - 밥
    - 오이
    - 시금치
    - 당근

    만드는 법
    1. 채소를 손질한다.
    2. 김 위에 밥을 펴 바른다.
    3. 채소를 넣고 말아준다.
    4. 먹기 좋은 크기로 자른다.
    """,

    "두부유부초밥":
    """
    재료
    - 유부초밥용 유부
    - 밥
    - 두부

    만드는 법
    1. 두부를 으깨 물기를 제거한다.
    2. 밥과 섞어 초밥 속을 만든다.
    3. 유부에 채워 넣는다.
    4. 접시에 담아 완성한다.
    """,

    "오트밀볼":
    """
    재료
    - 귀리(오트밀)
    - 바나나
    - 우유 또는 두유

    만드는 법
    1. 오트밀을 그릇에 담는다.
    2. 우유 또는 두유를 붓는다.
    3. 바나나를 썰어 올린다.
    4. 잘 섞어 먹는다.
    """,

    "병아리콩샐러드":
    """
    재료
    - 병아리콩
    - 상추
    - 오이
    - 토마토

    만드는 법
    1. 병아리콩을 삶는다.
    2. 채소를 씻어 손질한다.
    3. 재료를 한 그릇에 담는다.
    4. 드레싱을 곁들여 먹는다.
    """,

    "두부샐러드":
    """
    재료
    - 두부
    - 상추
    - 오이

    만드는 법
    1. 두부를 구워 식힌다.
    2. 채소를 손질한다.
    3. 접시에 함께 담는다.
    4. 드레싱을 뿌려 완성한다.
    """,

    "렌틸콩카레":
    """
    재료
    - 렌틸콩
    - 감자
    - 양파
    - 카레가루

    만드는 법
    1. 감자와 양파를 볶는다.
    2. 렌틸콩을 넣는다.
    3. 물과 카레가루를 넣고 끓인다.
    4. 밥과 함께 먹는다.
    """,

    "과일샐러드":
    """
    재료
    - 사과
    - 바나나
    - 귤

    만드는 법
    1. 과일을 깨끗이 씻는다.
    2. 먹기 좋은 크기로 자른다.
    3. 그릇에 담아 섞는다.
    4. 바로 먹는다.
    """,

    "오트밀 초코볼":
    """
    재료
    - 귀리
    - 코코아 가루
    - 꿀

    만드는 법
    1. 재료를 섞는다.
    2. 동그랗게 모양을 만든다.
    3. 냉장고에서 굳힌다.
    4. 간식으로 먹는다.
    """,

    "바나나 오트 쿠키":
    """
    재료
    - 바나나
    - 귀리

    만드는 법
    1. 바나나를 으깬다.
    2. 귀리와 섞는다.
    3. 쿠키 모양으로 만든다.
    4. 오븐에서 약 15분 굽는다.
    """
}

meal_info = {

    "닭가슴살 비빔밥":{
        "kcal":450,
        "protein":35,
        "carbon":3.5
    },

    "버섯고기비빔밥":{
        "kcal":520,
        "protein":30,
        "carbon":4.2
    },

    "두부불고기덮밥":{
        "kcal":430,
        "protein":24,
        "carbon":2.8
    },

    "채소김밥":{
        "kcal":380,
        "protein":10,
        "carbon":1.8
    },

    "두부유부초밥":{
        "kcal":410,
        "protein":15,
        "carbon":2.0
    },

    "오트밀볼":{
        "kcal":280,
        "protein":8,
        "carbon":1.2
    },

    "병아리콩샐러드":{
        "kcal":320,
        "protein":15,
        "carbon":1.5
    },

    "두부샐러드":{
        "kcal":250,
        "protein":18,
        "carbon":1.3
    },

    "렌틸콩카레":{
        "kcal":390,
        "protein":16,
        "carbon":2.0
    },

    "과일샐러드":{
        "kcal":220,
        "protein":3,
        "carbon":0.9
    },

    "오트밀 초코볼":{
        "kcal":180,
        "protein":5,
        "carbon":1.0
    },

    "바나나 오트 쿠키":{
        "kcal":210,
        "protein":4,
        "carbon":1.1
    }
}

missions = [
    "고기 1끼 줄이기",
    "채소 반찬 추가하기",
    "물 1L 마시기",
    "탄산 대신 물 마시기",
    "음식물 쓰레기 줄이기"
]# =========================
# 계산 함수
# =========================

def bmi_calc(weight, height):
    return weight / ((height / 100) ** 2)

def bmi_text(bmi):

    if bmi < 18.5:
        return "저체중"

    elif bmi < 25:
        return "정상"

    elif bmi < 30:
        return "과체중"

    else:
        return "비만"


def has_allergy(meal, banned_foods):

    ingredients = meal_ingredients.get(meal, [])

    for ingredient in ingredients:

        for banned in banned_foods:

            if banned and (banned in ingredient or ingredient in banned):
                return True

    return False


def get_rank(score):

    if score >= 95:
        return "🏆 S Rank"

    elif score >= 80:
        return "🥇 A Rank"

    elif score >= 60:
        return "🥈 B Rank"

    elif score >= 40:
        return "🥉 C Rank"

    else:
        return "🎖 D Rank"


def get_tree_effect(saved_carbon):

    trees = round(saved_carbon * 365 / 22)

    if trees < 1:
        trees = 1

    return trees

def travel_animation(sprite, message):

    area = st.empty()

    for i in range(11):

        area.empty()

        with area.container():

            st.markdown(f"### {message}")

            cols = st.columns(11)

            for j in range(11):

                with cols[j]:

                    if j == i:
                        st.image(sprite, width=80)
                    else:
                        st.write("")

        time.sleep(0.15)

    area.empty()

    with area.container():

        st.markdown(f"### {message}")

        st.markdown(
            "<h1 style='text-align:center;'>❗</h1>",
            unsafe_allow_html=True
        )

        st.image(sprite, width=120)

    time.sleep(0.8)

    area.empty()



# =========================
# 세션 상태
# =========================

if "step" not in st.session_state:
    st.session_state.step = 0

if "player" not in st.session_state:
    st.session_state.player = {}


# =========================
# 메인 화면
# =========================

st.title("🌱 EcoQuest RPG Edition")
st.caption("모험형 친환경 식습관 게임")

with st.form("eco_form"):

    name = st.text_input("이름")

    age = st.number_input(
        "나이",
        min_value=1,
        max_value=120,
        value=20
    )

    height = st.number_input(
        "키(cm)",
        min_value=100,
        max_value=250,
        value=170
    )

    weight = st.number_input(
        "체중(kg)",
        min_value=20,
        max_value=250,
        value=70
    )

    eating = st.radio(
        "평소 식습관",
        [
            "육류 위주",
            "간편식 위주",
            "채식 위주",
            "디저트 위주"
        ]
    )

    allergy = st.text_input(
        "알레르기 식품 (쉼표로 구분)"
    )

    start = st.form_submit_button("🎮 모험 시작")

if start:

    st.session_state.pop("step1_intro", None)
    st.session_state.pop("step2_intro", None)
    st.session_state.pop("step3_intro", None)

    profile_map = {
        "육류 위주":"meat",
        "간편식 위주":"instant",
        "채식 위주":"vegetable",
        "디저트 위주":"dessert"
    }

    st.session_state.player = {
        "name": name,
        "age": age,
        "height": height,
        "weight": weight,
        "eating": eating,
        "allergy": allergy,
        "profile": profile_map[eating]
    }

    st.session_state.step = 1
    st.rerun()


# =========================
# 결과 계산
# =========================

if st.session_state.step > 0:

    player = st.session_state.player

    result = jobs[player["profile"]]

    bmi = bmi_calc(
        player["weight"],
        player["height"]
    )

    carbon_saved = (
        result["before_carbon"]
        - result["after_carbon"]
    )

    carbon_percent = round(
        carbon_saved
        / result["before_carbon"]
        * 100,
        1
    )

    banned_foods = [
        food.strip()
        for food in player["allergy"].split(",")
        if food.strip()
    ]

    safe_meals = []

    for meal in result["meals"]:

        if not has_allergy(
            meal,
            banned_foods
        ):
            safe_meals.append(meal)

    eating_score = result["base_score"]

    carbon_score = int(
        carbon_percent * 0.5
    )

    practice_score = min(
        10,
        len(safe_meals) * 3
    )

    eco_score = (
        eating_score
        + carbon_score
        + practice_score
    )

    eco_score = min(
        100,
        eco_score
    )

    rank = get_rank(
        eco_score
    )

    trees = get_tree_effect(
        carbon_saved
    )# =========================
# STEP 1
# =========================
# =========================
# STEP 1
# =========================

if st.session_state.step == 1:

    if "step1_intro" not in st.session_state:

        travel_animation(
            result["sprite"],
            "🌲 숲길 탐험 중..."
        )

        st.session_state.step1_intro = True
        st.rerun()

    st.header("🛡️ STEP 1 : 직업 각성")

    st.image(
        result["sprite"],
        width=180
    )

    st.success(
        result["job"]
    )

    st.subheader(
        result["title"]
    )

    st.info(
        result["quote"]
    )

    st.divider()

    st.subheader("📋 기본 정보")

    st.write(
        f"이름 : {player['name']}"
    )

    st.write(
        f"나이 : {player['age']}세"
    )

    st.write(
        f"키 : {player['height']}cm"
    )

    st.write(
        f"체중 : {player['weight']}kg"
    )

    st.write(
        f"식습관 : {player['eating']}"
    )

    if st.button("다음 ▶"):
        st.session_state.step = 2
        st.rerun()


# =========================
# STEP 2
# =========================
elif st.session_state.step == 2:

    if "step2_intro" not in st.session_state:

        travel_animation(
            result["sprite"],
            "🏕️ 캠프 도착..."
        )

        st.session_state.step2_intro = True
        st.rerun()

    st.header("📊 STEP 2 : 능력치 공개")

    st.write(
        f"⚔️ 공격력 {result['attack']}/100"
    )
    st.progress(
        result["attack"]
    )

    st.write(
        f"❤️ 회복력 {result['recovery']}/100"
    )
    st.progress(
        result["recovery"]
    )

    st.write(
        f"🌍 친환경력 {result['eco_power']}/100"
    )
    st.progress(
        result["eco_power"]
    )

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "BMI",
            round(bmi, 1)
        )

    with c2:
        st.metric(
            "비만도",
            bmi_text(bmi)
        )

    if st.button("다음 ▶▶"):
        st.session_state.step = 3
        st.rerun()


# =========================
# STEP 3
# =========================

# =========================
# STEP 3
# =========================

elif st.session_state.step == 3:

    if "step3_intro" not in st.session_state:

        travel_animation(
            result["sprite"],
            "🏆 결과 공개..."
        )

        st.session_state.step3_intro = True
        st.rerun()

    st.header("🏆 STEP 3 : 최종 결과")

    st.subheader("🔍 식단 생성 과정")

    st.write(
        f"① 식습관 분석 → {player['eating']}"
    )

    st.write(
        f"② BMI 분석 → {round(bmi,1)} ({bmi_text(bmi)})"
    )

    if player["allergy"]:
        st.write(
            f"③ 알레르기 검사 → {player['allergy']}"
        )
    else:
        st.write(
            "③ 알레르기 검사 → 없음"
        )

    st.write(
        f"④ 탄소 절감 분석 → {carbon_percent}% 감소"
    )

    st.write(
        "⑤ 최종 식단 선정 완료"
    )

    st.divider()

    st.subheader("🎭 나의 직업")

    st.image(
        result["sprite"],
        width=180
    )

    st.success(
        result["job"]
    )

    st.write(
        result["description"]
    )

    st.divider()

    st.subheader("🌳 탄소 절감 효과")

    st.metric(
        "탄소 절감률",
        f"{carbon_percent}%"
    )

    st.metric(
        "심은 나무 수",
        f"{trees}그루"
    )

    st.progress(
        min(100, trees * 5)
    )

    st.divider()

    st.subheader("🥗 추천 식단")

    for meal in safe_meals:
        st.success(meal)

    st.divider()

    st.subheader("🎯 오늘의 미션")

    for m in random.sample(missions, 3):
        st.checkbox(m)

    st.divider()

    st.subheader("📄 결과 요약")

    st.code(
        f'''
이름 : {player["name"]}
BMI : {round(bmi,1)}
비만도 : {bmi_text(bmi)}
직업 : {result["job"]}
탄소 절감률 : {carbon_percent}%
심은 나무 수 : {trees}그루
'''
    )

    st.info(
        "※ 구현 예정 기능 : 웹사이트 레시피 연동, 직업별 일러스트 애니메이션, 업적 시스템 확장"
    )
