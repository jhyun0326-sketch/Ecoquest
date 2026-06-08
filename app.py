
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
        "icon":"⚔️",
        "job":"⚔️ 버서커",
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
        "icon":"🏹",
        "job":"🏹 레인저",
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
        "icon":"🌿",
        "job":"🌿 드루이드",
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
        "icon":"✨",
        "job":"✨ 연금술사",
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

def travel_animation(icon, message):

    area = st.empty()

    for i in range(11):

        road = (
            "⬜" * i
            + icon
            + "⬜" * (10 - i)
        )

        area.markdown(
            f"""
### {message}

{road}
"""
        )

        time.sleep(0.12)

    area.markdown(
        f"""
### {message}

# ❗

# {icon}
"""
    )

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
st.caption("게임형 친환경 식습관 모험")

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

    if st.session_state.step == 1:
        
        travel_animation(
            result["icon"],
            "🌲 숲길 탐험 중..."
        )
        
        st.header("🎭 STEP 1 : 직업 각성")

        st.success(result["job"])

        st.subheader(result["title"])

        st.info(result["quote"])

        if st.button("다음 ▶"):
            st.session_state.step = 2
            st.rerun()


# =========================
# STEP 2
# =========================

    elif st.session_state.step == 2:
       
        travel_animation(
            result["icon"],
            "⛰ 산길 탐험 중..."
        )
        
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
                "건강 상태",
                bmi_text(bmi)
            )

        if st.button("다음 ▶▶"):
            st.session_state.step = 3
            st.rerun()


# =========================
# STEP 3
# =========================

    elif st.session_state.step == 3:
       
        travel_animation(
            result["icon"],
            "🏰 환경의 성으로 이동 중..."
        )
        
        st.header("🏆 STEP 3 : 최종 결과")

        st.subheader(
            "🔍 식단 생성 과정"
        )

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

        st.subheader(
            "🍽 추천 식단"
        )

        if len(safe_meals) == 0:

            st.warning(
                "추천 가능한 식단이 없습니다."
            )

        else:

            for meal in safe_meals:
                st.success(meal)

        st.divider()

        st.subheader(
            "🌳 환경 효과"
        )

        st.metric(
            "탄소 절감률",
            f"{carbon_percent}%"
        )

        st.success(
            f"🌳 약 {trees}그루의 나무를 심은 효과"
        )

        st.info(
            f"🚗 자동차 약 {round(carbon_saved * 100)}km 운행 감소 효과"
        )

        st.divider()

        st.subheader(
            "🏅 친환경 점수 계산"
        )

        st.write(
            f"식습관 점수 : {eating_score}"
        )

        st.write(
            f"탄소 절감 점수 : {carbon_score}"
        )

        st.write(
            f"실천 가능성 점수 : {practice_score}"
        )

        st.success(
            f"총점 : {eco_score}"
        )
        
        st.markdown(
        f"""
        # ❗

        ## {result["icon"]}

        최종 평가 확인 중...
        """
        )

        time.sleep(1.2)
        
        st.header(rank)

        st.divider()

        st.subheader(
            "🏆 업적"
        )

        if eco_score >= 95:

            st.success(
                "숲의 대수호자"
            )

        elif eco_score >= 80:

            st.success(
                "자연의 길잡이"
            )

        else:

            st.success(
                "새싹 모험가"
            )

        st.divider()

        st.subheader(
            "🎯 오늘의 퀘스트"
        )

        for mission in random.sample(
            missions,
            3
        ):
            st.checkbox(
                mission
            )

        st.divider()

        st.subheader(
            "💡 실천 팁"
        )

        for tip in result["tips"]:

            st.write(
                "• " + tip
            )

        st.divider()

        st.subheader(
            "📄 결과 요약"
        )

        st.code(
f"""
이름 : {player['name']}
나이 : {player['age']}

직업 : {result['job']}
칭호 : {result['title']}

BMI : {round(bmi,1)}
건강 상태 : {bmi_text(bmi)}

친환경 점수 : {eco_score}
랭크 : {rank}

탄소 절감률 : {carbon_percent}%
"""
        )
