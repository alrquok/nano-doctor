import streamlit as st
import math
import random
import time

# ─── 페이지 기본 설정 ───────────────────────────────────────────────

st.set_page_config(
page_title=“나노 닥터 🔬”,
page_icon=“🔬”,
layout=“wide”,
initial_sidebar_state=“expanded”,
)

# ─── CSS 스타일 ──────────────────────────────────────────────────────

st.markdown(”””

<style>
    .main { background-color: #0d1b2a; color: #e0f0ff; }
    .stApp { background-color: #0d1b2a; }
    h1, h2, h3 { color: #00d4ff; }
    .stat-box {
        background: linear-gradient(135deg, #1a2a4a, #0d1b2a);
        border: 1px solid #00d4ff44;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        text-align: center;
    }
    .result-box {
        background: linear-gradient(135deg, #0a2a1a, #0d1b2a);
        border: 1px solid #00ff8844;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
    }
    .warning-box {
        background: linear-gradient(135deg, #2a1a0a, #0d1b2a);
        border: 1px solid #ff880044;
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
    }
    .nano-tag {
        display: inline-block;
        background: #00d4ff22;
        border: 1px solid #00d4ff66;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.85em;
        margin: 2px;
    }
    .stProgress > div > div { background-color: #00d4ff; }
    div[data-testid="metric-container"] {
        background: #1a2a4a;
        border: 1px solid #00d4ff33;
        border-radius: 8px;
        padding: 10px;
    }
</style>

“””, unsafe_allow_html=True)

# ─── 핵심 과학 계산 함수 (파이썬 로직 파트) ─────────────────────────

def calculate_nanoparticle_stats(size_nm: float, zeta_mv: float, material: str) -> dict:
“””
나노입자 설계 스탯 계산
- size_nm   : 입자 크기 (10~200 nm)
- zeta_mv   : 표면 전하 Zeta potential (-50 ~ +50 mV)
- material  : 소재 종류
실제 나노의학 연구 기반 수치 모델
“””
# 소재별 기본 특성 (실제 연구 기반)
material_props = {
“셀룰로오스 나노결정 (CNC)”: {
“biocompat”:   0.95,  # 생체적합성
“drug_load”:   0.70,  # 약물 탑재량
“special”:     “표면 개질 용이 → 업그레이드 보너스 +20%”,
“color”:       “🌿”,
},
“키토산 나노입자”: {
“biocompat”:   0.88,
“drug_load”:   0.80,
“special”:     “점막 부착성·항균성 → 소화기계 데미지 +30%”,
“color”:       “🦐”,
},
“리그닌 나노입자”: {
“biocompat”:   0.82,
“drug_load”:   0.65,
“special”:     “항산화 특성 → 산화 스트레스 적 즉시 제거”,
“color”:       “🌲”,
},
“전분 나노입자”: {
“biocompat”:   0.90,
“drug_load”:   0.75,
“special”:     “빠른 약물 방출 → 긴급 치료 속도 +40%”,
“color”:       “🌽”,
},
}
mp = material_props[material]

```
# 1) 세포 침투율: 크기가 작을수록 높음 (EPR 효과 반영)
#    실제 최적 범위: 50~150 nm
if size_nm <= 100:
    penetration = 95 - (size_nm - 10) * 0.3
else:
    penetration = 95 - (size_nm - 10) * 0.55
penetration = max(10.0, min(100.0, penetration))

# 2) 혈중 안정성: |Zeta| > 30 mV 이면 안정
stability = min(100.0, abs(zeta_mv) * 2.0 + 10)

# 3) 면역 회피율: 음전하 입자가 대식세포 회피에 유리
if zeta_mv < 0:
    immune_evade = 60 + abs(zeta_mv) * 0.8
else:
    immune_evade = 40 - zeta_mv * 0.4
immune_evade = max(5.0, min(100.0, immune_evade))

# 4) pH 반응성: 암세포 주변 산성(pH ≈ 6.5) 환경에서 방출 → 크기 클수록 유리
ph_response = 40 + size_nm * 0.25
ph_response = max(10.0, min(95.0, ph_response))

# 5) 총 효능 (가중평균)
efficacy = (
    penetration   * 0.30 +
    stability     * 0.25 +
    immune_evade  * 0.25 +
    ph_response   * 0.20
) * mp["biocompat"]
efficacy = min(100.0, efficacy)

# 6) 부작용 위험도
side_effect_risk = max(0.0, 100 - efficacy - mp["biocompat"] * 20)

return {
    "penetration":     round(penetration, 1),
    "stability":       round(stability, 1),
    "immune_evade":    round(immune_evade, 1),
    "ph_response":     round(ph_response, 1),
    "efficacy":        round(efficacy, 1),
    "side_effect":     round(side_effect_risk, 1),
    "drug_load":       round(mp["drug_load"] * 100, 1),
    "biocompat":       round(mp["biocompat"] * 100, 1),
    "special":         mp["special"],
    "color":           mp["color"],
}
```

def simulate_blood_travel(stats: dict, peg_coated: bool, sensor_score: int) -> dict:
“””
혈관 항법 시뮬레이션 (전기전자 파트)
- 나노센서 점수, PEG 코팅 여부 반영
“””
base_success = stats[“immune_evade”] * 0.5 + stats[“stability”] * 0.3
if peg_coated:
base_success += 20   # PEG 코팅 → 스텔스 효과
base_success += sensor_score * 0.3   # 센서 탐색 정확도 반영
base_success = min(100.0, base_success)

```
macrophage_blocked = not peg_coated and stats["immune_evade"] < 50
reached = base_success > 45

return {
    "success_rate":      round(base_success, 1),
    "reached_target":    reached,
    "macrophage_blocked": macrophage_blocked,
    "sensor_bonus":      sensor_score,
}
```

def simulate_tumor_attack(stats: dict, travel_result: dict, epr_used: bool) -> dict:
“””
암세포 공략 시뮬레이션 (건강 파트)
- EPR 효과, pH 반응성 반영
“””
if not travel_result[“reached_target”]:
return {“damage”: 0, “normal_damage”: 0, “success”: False,
“message”: “❌ 표적에 도달하지 못했습니다.”}

```
tumor_damage = stats["penetration"] * 0.4 + stats["ph_response"] * 0.4
if epr_used:
    tumor_damage *= 1.35   # EPR 효과 보너스

# 정상세포 피해 (낮을수록 좋음)
normal_damage = max(0.0, 50 - stats["immune_evade"] * 0.3 - stats["ph_response"] * 0.2)

# 약물 탑재량 반영
tumor_damage *= stats["drug_load"] / 100
final_damage = min(100.0, tumor_damage)

score = final_damage - normal_damage * 0.5
success = score > 35

return {
    "damage":        round(final_damage, 1),
    "normal_damage": round(normal_damage, 1),
    "success":       success,
    "score":         round(max(0, score), 1),
    "message":       "✅ 암세포 공략 성공!" if success else "⚠️ 효과가 충분하지 않습니다.",
}
```

def get_grade(efficacy: float) -> str:
if efficacy >= 85: return “S등급 🏆 — 최우수 나노의약품”
if efficacy >= 70: return “A등급 ⭐ — 임상 적용 가능”
if efficacy >= 55: return “B등급 🔬 — 추가 최적화 필요”
if efficacy >= 40: return “C등급 ⚗️  — 설계 재검토 권장”
return “D등급 ❌ — 처음부터 다시 설계”

# ─── 세션 상태 초기화 ────────────────────────────────────────────────

def init_state():
defaults = {
“stage”: 1,
“stats”: None,
“travel_result”: None,
“tumor_result”: None,
“total_score”: 0,
“sensor_score”: 0,
“peg_coated”: False,
“epr_used”: False,
“game_over”: False,
}
for k, v in defaults.items():
if k not in st.session_state:
st.session_state[k] = v

init_state()

# ─── 사이드바: 게임 정보 & 과학 노트 ────────────────────────────────

with st.sidebar:
st.markdown(”## 🔬 나노 닥터”)
st.markdown(”**바이오매스 나노소재로 암을 치료하라!**”)
st.divider()

```
st.markdown("### 📖 과학 노트")
with st.expander("EPR 효과란?"):
    st.markdown("""
```

암 조직은 혈관이 불규칙하게 발달해 틈새가 큽니다.
나노입자(100~200nm)는 이 틈새를 통해 **정상 조직보다
암 조직에 더 잘 축적**됩니다.
→ 게임에서 EPR 버튼을 사용하면 암세포 데미지 +35%!
“””)
with st.expander(“Zeta Potential이란?”):
st.markdown(”””
나노입자 표면의 전기적 성질입니다.

- **|ζ| > 30 mV** → 입자끼리 반발 → 응집 방지 → 안정성 ↑
- **음전하** → 대식세포 회피 유리 (혈액 단백질 흡착 ↓)
  “””)
  with st.expander(“바이오매스 나노소재란?”):
  st.markdown(”””
  목재, 갑각류, 곡물 등 **자연 유래 원료**에서 추출한
  나노 크기의 소재입니다.
- 생체적합성 우수
- 생분해 가능 → 체내 잔류 위험 낮음
- 탄소중립 소재
  “””)
  
  st.divider()
  stage_names = {1: “🧪 소재 설계”, 2: “💻 혈관 항법”, 3: “💊 암세포 공략”}
  st.markdown(f”### 현재 스테이지: {stage_names.get(st.session_state.stage, ‘🏁 완료’)}”)
  if st.session_state.total_score:
  st.metric(“누적 점수”, f”{st.session_state.total_score:.0f}점”)
  
  if st.button(“🔄 처음부터 다시”):
  for k in list(st.session_state.keys()):
  del st.session_state[k]
  st.rerun()

# ─── 메인 화면 ───────────────────────────────────────────────────────

st.markdown(”# 🔬 나노 닥터: 바이오매스 나노입자로 암을 치료하라”)
st.markdown(”*재료공학 × 정보통신 × 의학의 융합 — 나노약물전달체(DDS) 시뮬레이션*”)
st.divider()

# 진행 바

progress = (st.session_state.stage - 1) / 3
st.progress(progress, text=f”진행률: 스테이지 {min(st.session_state.stage, 3)}/3”)
st.markdown(””)

# ════════════════════════════════════════════════════════════════════

# 스테이지 1 — 나노입자 설계실 (재료공학)

# ════════════════════════════════════════════════════════════════════

if st.session_state.stage == 1:
st.markdown(”## 🧪 스테이지 1 — 나노입자 설계실”)
st.markdown(”””
바이오매스 기반 나노입자를 설계하세요.
**크기, 표면 전하, 소재**를 조절해 최적의 약물전달체를 만드세요!
“””)

```
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### ⚙️ 설계 파라미터")

    material = st.selectbox(
        "🌿 소재 선택",
        ["셀룰로오스 나노결정 (CNC)", "키토산 나노입자", "리그닌 나노입자", "전분 나노입자"],
        help="각 소재는 실제 바이오매스에서 추출됩니다."
    )

    size_nm = st.slider(
        "📏 입자 크기 (nm)",
        min_value=10, max_value=200, value=80, step=5,
        help="작을수록 세포 침투 유리, 클수록 pH 반응성 유리"
    )

    zeta_mv = st.slider(
        "⚡ Zeta Potential (mV)",
        min_value=-50, max_value=50, value=-30, step=5,
        help="음전하 → 면역 회피↑, |값|클수록 안정성↑"
    )

    st.markdown("")
    if st.button("🔬 나노입자 분석 시작", type="primary", use_container_width=True):
        stats = calculate_nanoparticle_stats(size_nm, zeta_mv, material)
        st.session_state.stats = stats

with col2:
    if st.session_state.stats:
        s = st.session_state.stats
        st.markdown("### 📊 분석 결과")

        m1, m2 = st.columns(2)
        m1.metric("총 효능", f"{s['efficacy']}%")
        m2.metric("부작용 위험", f"{s['side_effect']}%")

        st.markdown("**세부 스탯**")
        st.markdown(f"🎯 세포 침투율: **{s['penetration']}%**")
        st.progress(s['penetration']/100)
        st.markdown(f"🛡️ 혈중 안정성: **{s['stability']}%**")
        st.progress(s['stability']/100)
        st.markdown(f"👻 면역 회피율: **{s['immune_evade']}%**")
        st.progress(s['immune_evade']/100)
        st.markdown(f"🧪 pH 반응성: **{s['ph_response']}%**")
        st.progress(s['ph_response']/100)
        st.markdown(f"💊 약물 탑재량: **{s['drug_load']}%**")
        st.progress(s['drug_load']/100)

        st.markdown(f"""
```

<div class="result-box">
{s['color']} <b>특수 능력</b><br>{s['special']}
</div>
            """, unsafe_allow_html=True)

```
        grade = get_grade(s['efficacy'])
        st.markdown(f"""
```

<div class="stat-box">
<h3>설계 등급: {grade}</h3>
</div>
            """, unsafe_allow_html=True)

```
        if s['efficacy'] >= 40:
            st.success("✅ 다음 스테이지로 진행할 수 있습니다!")
            if st.button("▶ 스테이지 2로 이동", type="primary"):
                st.session_state.total_score += s['efficacy']
                st.session_state.stage = 2
                st.rerun()
        else:
            st.error("❌ 효능이 너무 낮습니다. 파라미터를 다시 조절하세요.")
```

# ════════════════════════════════════════════════════════════════════

# 스테이지 2 — 혈관 항법 (전기전자/정보통신)

# ════════════════════════════════════════════════════════════════════

elif st.session_state.stage == 2:
st.markdown(”## 💻 스테이지 2 — 혈관 항법 센터”)
st.markdown(”””
나노센서를 이용해 병변을 탐색하고,
면역세포를 피해 표적까지 나노입자를 전달하세요!
“””)

```
s = st.session_state.stats
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 💻 나노센서 제어판")
    st.markdown("""
    <div class="stat-box">
    <b>🔌 나노바이오센서 원리</b><br>
    형광 신호 → 전기 신호 변환 → 병변 위치 데이터 전송<br>
    IoT 의료기기와 연동해 실시간 추적
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**센서 보정 미니게임**: 아래 주파수를 맞춰 신호를 최적화하세요!")
    freq = st.slider("📡 센서 주파수 (GHz)", 1.0, 10.0, 5.0, 0.1)
    gain = st.slider("📶 증폭 이득 (dB)", 0, 50, 25)
    noise = st.slider("🔇 노이즈 필터 (Hz)", 0, 100, 50)

    # 최적값: freq≈6.0, gain≈30, noise≈60 → 센서 점수 계산
    sensor_score = (
        max(0, 100 - abs(freq - 6.0) * 20) * 0.4 +
        max(0, 100 - abs(gain - 30) * 3) * 0.3 +
        max(0, 100 - abs(noise - 60) * 2) * 0.3
    )
    st.session_state.sensor_score = sensor_score
    st.metric("센서 정확도", f"{sensor_score:.1f}%")

    peg = st.checkbox(
        "🛡️ PEG 코팅 적용 (면역 스텔스)",
        help="PEGylation: 대식세포 회피율 +20%, 실제 DDS 연구의 핵심 기법"
    )
    st.session_state.peg_coated = peg

    if st.button("🚀 혈관 항법 시작", type="primary", use_container_width=True):
        result = simulate_blood_travel(s, peg, sensor_score)
        st.session_state.travel_result = result

with col2:
    if st.session_state.travel_result:
        r = st.session_state.travel_result
        st.markdown("### 📡 항법 결과")

        st.metric("표적 도달 성공률", f"{r['success_rate']}%")
        st.progress(r['success_rate']/100)

        if r['macrophage_blocked']:
            st.markdown("""
```

<div class="warning-box">
⚠️ <b>대식세포에게 탐지되었습니다!</b><br>
PEG 코팅을 적용하면 면역 회피율이 높아집니다.<br>
(PEGylation: 혈중 순환 시간 연장 효과)
</div>
                """, unsafe_allow_html=True)

```
        if r['sensor_bonus'] > 70:
            st.success(f"🎯 센서 정밀도 우수! 보너스 +{r['sensor_bonus']:.0f}점")

        if r['reached_target']:
            st.success("✅ 표적 도달 성공! 다음 단계로 진행합니다.")
            if st.button("▶ 스테이지 3으로 이동", type="primary"):
                st.session_state.total_score += r['success_rate']
                st.session_state.stage = 3
                st.rerun()
        else:
            st.error("❌ 표적 도달 실패. 파라미터를 조정하세요.")
            if st.button("🔄 다시 시도"):
                st.session_state.travel_result = None
                st.rerun()
```

# ════════════════════════════════════════════════════════════════════

# 스테이지 3 — 암세포 공략 (건강)

# ════════════════════════════════════════════════════════════════════

elif st.session_state.stage == 3:
st.markdown(”## 💊 스테이지 3 — 암세포 공략”)
st.markdown(”””
드디어 표적 도달! EPR 효과를 활용해 암세포에 약물을 방출하고
정상세포 피해를 최소화하세요.
“””)

```
s  = st.session_state.stats
tr = st.session_state.travel_result
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎯 공략 전략 선택")

    epr = st.checkbox(
        "🔬 EPR 효과 활성화",
        help="암 조직 혈관의 불규칙성을 이용 — 암세포 데미지 +35%"
    )
    st.session_state.epr_used = epr

    st.markdown("**pH 조건 설정** (암세포 주변은 산성)")
    ph_val = st.slider("환경 pH", 5.5, 7.4, 6.5, 0.1,
                       help="낮을수록 산성 → 나노입자 약물 방출 촉진")

    st.markdown("""
```

<div class="stat-box">
<b>💡 건강 지식</b><br>
정상 혈액 pH: 7.35~7.45<br>
암세포 주변 pH: 6.0~6.8 (산성)<br>
→ pH 반응형 나노입자가 암 조직 선택적 약물 방출 가능!
</div>
        """, unsafe_allow_html=True)

```
    if st.button("💥 약물 방출!", type="primary", use_container_width=True):
        result = simulate_tumor_attack(s, tr, epr)
        st.session_state.tumor_result = result
        if result["success"]:
            st.session_state.total_score += result["score"]

with col2:
    if st.session_state.tumor_result:
        r = st.session_state.tumor_result
        st.markdown("### 📊 치료 결과")
        st.markdown(r["message"])

        if r["success"]:
            c1, c2 = st.columns(2)
            c1.metric("암세포 데미지", f"{r['damage']}%", delta="높을수록 good")
            c2.metric("정상세포 피해", f"{r['normal_damage']}%", delta="낮을수록 good",
                      delta_color="inverse")

            st.markdown("**암세포 제거 현황**")
            st.progress(r['damage']/100)
            st.markdown("**정상세포 보호율**")
            st.progress(max(0, 1 - r['normal_damage']/100))

            total = st.session_state.total_score
            final_grade = get_grade(total / 3)

            st.markdown(f"""
```

<div class="result-box">
<h2>🏆 최종 결과</h2>
<h3>총점: {total:.0f}점</h3>
<h3>{final_grade}</h3>
<br>
<b>✅ 나노약물전달체 임상 시험 승인!</b><br>
바이오매스 기반 나노소재의 성공적인 치료 사례로
국제 저널에 등재되었습니다. 🎉
</div>
                """, unsafe_allow_html=True)

```
            st.balloons()

            if st.button("📋 결과 요약 보기"):
                st.session_state.stage = 4
                st.rerun()
        else:
            st.error("pH 조건과 EPR 전략을 다시 검토하세요.")
            if st.button("🔄 다시 시도"):
                st.session_state.tumor_result = None
                st.rerun()
```

# ════════════════════════════════════════════════════════════════════

# 최종 결과 요약

# ════════════════════════════════════════════════════════════════════

elif st.session_state.stage == 4:
st.markdown(”## 🏆 최종 결과 리포트”)
st.markdown(”*나노약물전달체 설계 & 치료 시뮬레이션 완료*”)

```
s  = st.session_state.stats
tr = st.session_state.travel_result
tu = st.session_state.tumor_result

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
```

<div class="stat-box">
<h3>🧪 재료공학</h3>
바이오매스 나노소재 설계
</div>
        """, unsafe_allow_html=True)
        if s:
            st.write(f"소재: {s['color']}")
            st.write(f"효능: {s['efficacy']}%")
            st.write(f"등급: {get_grade(s['efficacy'])}")

```
with col2:
    st.markdown("""
```

<div class="stat-box">
<h3>💻 정보통신</h3>
나노센서 & 혈관 항법
</div>
        """, unsafe_allow_html=True)
        if tr:
            st.write(f"센서 정확도: {tr['sensor_bonus']:.1f}%")
            st.write(f"도달 성공률: {tr['success_rate']}%")
            st.write(f"PEG 코팅: {'적용 ✅' if st.session_state.peg_coated else '미적용'}")

```
with col3:
    st.markdown("""
```

<div class="stat-box">
<h3>💊 건강</h3>
암세포 공략 & 치료
</div>
        """, unsafe_allow_html=True)
        if tu:
            st.write(f"암세포 데미지: {tu['damage']}%")
            st.write(f"정상세포 피해: {tu['normal_damage']}%")
            st.write(f"EPR 효과: {'활성화 ✅' if st.session_state.epr_used else '미사용'}")

```
st.divider()
st.markdown(f"### 🏅 총점: {st.session_state.total_score:.0f}점")
st.markdown(f"### {get_grade(st.session_state.total_score / 3)}")

st.markdown("""
```

-----

**📚 참고 — 실제 연구 분야**

- 나노약물전달체(Nano Drug Delivery System, nano-DDS)
- PEGylation을 통한 스텔스 나노입자
- EPR(Enhanced Permeability and Retention) 효과
- 바이오매스 유래 셀룰로오스·키토산·리그닌 나노소재
  “””)
