
import streamlit as st
import random

st.set_page_config(page_title="EcoQuest", page_icon="🌱", layout="wide")

types = {
    "meat": {
        "nickname": "육식 밸런서",
        "type_name": "고기 없인 못 살아형",
        "description": "고기를 좋아하지만 양과 종류를 조절하면 좋은 유형입니다.",
        "before": "소고기덮밥",
        "after": "닭가슴살 비빔밥 + 버섯볶음",
        "before_carbon": 8.0,
        "after_carbon": 3.5,
        "eco_score": 60,
        "meals": ["닭가슴살 비빔밥","버섯고기비빔밥","두부불고기덮밥"],
        "tips": ["소고기보다 닭고기 선택","버섯·두부 추가","주 1~2회 대체식 실천"]
    },
    "instant": {
        "nickname": "편의점 마스터",
        "type_name": "간편식 의존형",
        "description": "빠르고 간편한 음식을 자주 먹는 유형입니다.",
        "before": "컵라면 + 소시지",
        "after": "채소김밥 + 두유",
        "before_carbon": 4.5,
        "after_carbon": 1.8,
        "eco_score": 55,
        "meals": ["채소김밥","두부유부초밥","오트밀볼"],
        "tips": ["채소 추가","가공육 줄이기","두유 선택"]
    },
    "vegetable": {
        "nickname": "지구친화 미식가",
        "type_name": "이미 지구랑 친한 형",
        "description": "채소 중심 식단을 잘 실천 중입니다.",
        "before": "채소비빔밥",
        "after": "렌틸콩 비빔밥",
        "before_carbon": 2.5,
        "after_carbon": 2.0,
        "eco_score": 92,
        "meals": ["병아리콩샐러드","두부샐러드","렌틸콩카레"],
        "tips": ["단백질 보완","제철채소 활용","영양 균형 유지"]
    },
    "dessert": {
        "nickname": "디저트 힐러",
        "type_name": "디저트로 멘탈 충전형",
        "description": "디저트를 자주 즐기는 유형입니다.",
        "before": "커피 + 초콜릿",
        "after": "두유 바나나 스무디",
        "before_carbon": 3.2,
        "after_carbon": 1.4,
        "eco_score": 65,
        "meals": ["과일샐러드","오트밀 초코볼","바나나 오트 쿠키"],
        "tips": ["탄산 대신 물","과일 활용","빈도 조절"]
    }
}

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
    "탄산음료 대신 물 마시기",
    "음식물 쓰레기 줄이기"
]

def bmi_calc(w,h):
    return w/((h/100)**2)

def bmi_text(b):
    if b < 18.5: return "저체중"
    if b < 25: return "정상"
    if b < 30: return "과체중"
    return "비만"

def carbon_level(percent):
    if percent >= 50: return "🌎🌎🌎 Lv.3"
    if percent >= 30: return "🌎🌎 Lv.2"
    return "🌎 Lv.1"

def has_allergy(meal,banned):
    for ingredient in meal_ingredients.get(meal,[]):
        for b in banned:
            if b and (b in ingredient or ingredient in b):
                return True
    return False

st.title("🌱 EcoQuest")
st.caption("게임형 친환경 디지털 영양사")

with st.form("eco"):
    name = st.text_input("이름")
    age = st.number_input("나이",1,120,20)
    height = st.number_input("키(cm)",100,250,170)
    weight = st.number_input("체중(kg)",20,250,70)

    eating = st.radio("평소 식습관",
        ["육류 위주","간편식 위주","채식 위주","디저트 위주"])

    allergy = st.text_input("알레르기 식품 (쉼표로 구분)")

    run = st.form_submit_button("결과 보기")

if run:
    profile_map = {
        "육류 위주":"meat",
        "간편식 위주":"instant",
        "채식 위주":"vegetable",
        "디저트 위주":"dessert"
    }

    result = types[profile_map[eating]]

    bmi = bmi_calc(weight,height)

    st.header("🏅 결과")

    c1,c2,c3 = st.columns(3)
    c1.metric("BMI", round(bmi,1))
    c2.metric("건강 상태", bmi_text(bmi))
    c3.metric("친환경 점수", result["eco_score"])

    st.subheader("🎭 캐릭터")
    st.success(result["nickname"])
    st.write(result["type_name"])
    st.write(result["description"])

    st.subheader("📊 스탯")
    st.write("❤️ 건강력")
    st.progress(max(0,min(100,int(100-abs(22-bmi)*5))))
    st.write("🌍 친환경력")
    st.progress(result["eco_score"])

    st.subheader("🍽 탄소 절감 분석")

    reduced = result["before_carbon"] - result["after_carbon"]
    percent = round(reduced/result["before_carbon"]*100,1)

    st.write(f"기존 식단: {result['before']} ({result['before_carbon']} kgCO₂e)")
    st.write(f"추천 식단: {result['after']} ({result['after_carbon']} kgCO₂e)")

    st.metric("절감률", f"{percent}%")
    st.info(carbon_level(percent))

    st.subheader("🥗 맞춤 추천 식단")

    banned = [x.strip() for x in allergy.split(",") if x.strip()]

    safe_meals = [m for m in result["meals"] if not has_allergy(m,banned)]

    if safe_meals:
        for meal in safe_meals:
            st.success(meal)
    else:
        st.warning("알레르기 조건으로 추천 가능한 식단이 없습니다.")

    st.subheader("🎯 오늘의 미션")
    for m in random.sample(missions,3):
        st.checkbox(m)

    st.subheader("🏆 업적")
    score = result["eco_score"]
    if score >= 90:
        st.success("지구 수호자")
    elif score >= 70:
        st.success("친환경 탐험가")
    else:
        st.success("식습관 입문자")

    st.subheader("💡 실천 팁")
    for tip in result["tips"]:
        st.write("•", tip)

    st.subheader("📄 결과 요약")
    st.code(f"""
이름: {name}
나이: {age}
BMI: {round(bmi,1)}
유형: {result['nickname']}
친환경 점수: {score}
탄소 절감률: {percent}%
""")
