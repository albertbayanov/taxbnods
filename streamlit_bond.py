
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Облигационный калькулятор", layout="centered")

PRIMARY_COLOR = "#1F3568"
BG_COLOR = "#F6F2EC"
TEXT_COLOR = "#1F3568"

st.markdown(
    f"""
    <style>
    body {{
        background-color: {BG_COLOR};
        color: {TEXT_COLOR};
        font-family: 'Georgia', serif;
    }}
    h1 {{
        font-size: 32px;
        text-align: center;
        color: {PRIMARY_COLOR};
    }}
    .stDataFrame thead tr th {{
        background-color: {PRIMARY_COLOR};
        color: white;
        font-weight: bold;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True
)

st.image("logo.png", width=120)

st.markdown("<h1>📊 Облигационный калькулятор</h1>", unsafe_allow_html=True)

st.markdown("""
**Условия расчёта:**  
- 💰 Сумма облигации: $100,000 (фиксировано)  
- 📈 Купон начисляется пропорционально сроку (НКД)  
- 🧾 Налог 20% на купон — только при владении 12 месяцев  
- 🔄 Курсовая разница (курс продажи - курс покупки) облагается налогом 25%  
- 💹 Доходность считается годовая, с учётом всех налогов  
""")

amount_usd = 100000
months = months = st.number_input("Срок владения облигацией (мес.)", min_value=1, max_value=12, value=6, step=1)
initial_exchange_rate = st.number_input("Курс покупки (₽)", min_value=80.0, max_value=120.0, value=82.5, step=0.5)
exchange_rate = st.number_input("Курс продажи (₽)", min_value=80.0, max_value=120.0, value=90.0, step=0.5)
coupon_rate = st.number_input("Купон (%)", min_value=1.0, max_value=15.0, value=8.25, step=0.05)

purchase_price_rub = amount_usd * initial_exchange_rate
sale_price_rub = amount_usd * exchange_rate
coupon_usd = amount_usd * (coupon_rate / 100)
nkd_rub = coupon_usd * (months / 12) * exchange_rate
coupon_tax = nkd_rub * 0.20 if months == 12 else 0
currency_profit = (exchange_rate - initial_exchange_rate) * amount_usd
currency_tax = currency_profit * 0.25 if currency_profit > 0 else 0

profit_before_tax = sale_price_rub - purchase_price_rub + nkd_rub
net_profit = profit_before_tax - coupon_tax - currency_tax

annualized_return_before_tax = (profit_before_tax / purchase_price_rub) * (12 / months) * 100
annualized_net_return = (net_profit / purchase_price_rub) * (12 / months) * 100

result_df = pd.DataFrame.from_dict({
    "Срок владения (мес.)": [months],
    "Купон (%)": [f"{coupon_rate:.2f}"],
    "НКД (₽)": [f"{nkd_rub:.2f}"],
    "Доходность до налогов (%)": [f"{annualized_return_before_tax:.2f}"],
    "Чистая доходность (%)": [f"{annualized_net_return:.2f}"]
}, orient="index", columns=["Значение"])

st.markdown("<h4 style='padding-top: 20px;'>Результаты расчета:</h4>", unsafe_allow_html=True)
st.dataframe(result_df.style.set_properties(**{
    'text-align': 'center'
}, orient="index", columns=["Значение"]).set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center')]
}]), use_container_width=True)
