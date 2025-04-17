
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

amount_usd = st.slider("Сумма облигации ($)", 1000, 1_000_000, 100_000, 1000)
initial_exchange_rate = st.slider("Курс покупки (₽)", 80, 120, 82, 1)
exchange_rate = st.slider("Курс продажи (₽)", 80, 120, 90, 1)
coupon_rate = st.slider("Купон (%)", 1.0, 15.0, 8.25, 0.1)
months = st.slider("Срок владения (мес.)", 1, 12, 6, 1)

purchase_price_rub = amount_usd * initial_exchange_rate
sale_price_rub = amount_usd * exchange_rate
coupon_usd = amount_usd * (coupon_rate / 100)
accrued_coupon_rub = coupon_usd * (months / 12) * exchange_rate
coupon_tax = accrued_coupon_rub * 0.20 if months == 12 else 0
coupon_rub = accrued_coupon_rub

profit_before_tax = sale_price_rub - purchase_price_rub + coupon_rub
net_profit = profit_before_tax - coupon_tax

annualized_return_before_tax = (profit_before_tax / purchase_price_rub) * (12 / months) * 100
annualized_net_return = (net_profit / purchase_price_rub) * (12 / months) * 100

result_df = pd.DataFrame({
    "Срок (мес.)": [months],
    "Сумма ($)": [f"{amount_usd:,.2f}"],
    "Купон (%)": [f"{coupon_rate:.2f}"],
    "Доходность до налогов (%)": [f"{annualized_return_before_tax:.2f}"],
    "Чистая доходность (%)": [f"{annualized_net_return:.2f}"]
})

st.markdown("<h4 style='padding-top: 20px;'>Результаты расчета:</h4>", unsafe_allow_html=True)
st.dataframe(result_df.style.set_properties(**{
    'text-align': 'center'
}).set_table_styles([{
    'selector': 'th',
    'props': [('text-align', 'center')]
}]), use_container_width=True)
