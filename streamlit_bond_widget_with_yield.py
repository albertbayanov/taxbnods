
import streamlit as st
import pandas as pd

st.title("Калькулятор доходности по долларовой облигации")

# Слайдеры
amount_usd = st.slider("Сумма облигации ($)", min_value=1000, max_value=1_000_000, step=1000, value=100_000)
exchange_rate = st.slider("Курс ЦБ (руб.)", min_value=80, max_value=120, step=1, value=90)
coupon_rate = st.slider("Купон (%)", min_value=1.0, max_value=15.0, step=0.1, value=8.25)
months = st.slider("Срок в месяцах", min_value=1, max_value=12, step=1, value=6)

# Расчеты
purchase_price_rub = amount_usd * 82.5  # фиксированный курс покупки для примера
sale_price_rub = amount_usd * exchange_rate
coupon_usd = amount_usd * (coupon_rate / 100)
coupon_rub = coupon_usd * exchange_rate if months == 12 else 0
coupon_tax = coupon_rub * 0.20 if months == 12 else 0

profit_before_tax = sale_price_rub - purchase_price_rub + coupon_rub

# Налог только на купон на 12 месяц
net_profit = sale_price_rub - purchase_price_rub + coupon_rub - coupon_tax

# Годовая доходность в процентах
annualized_return_before_tax = (profit_before_tax / purchase_price_rub) * (12 / months) * 100
annualized_net_return = (net_profit / purchase_price_rub) * (12 / months) * 100

# Таблица
result_df = pd.DataFrame({
    "Срок (мес.)": [months],
    "Сумма облигации ($)": [amount_usd],
    "Купон (%)": [coupon_rate],
    "Доходность до налогов (% годовых)": [round(annualized_return_before_tax, 2)],
    "Чистая доходность (% годовых)": [round(annualized_net_return, 2)]
})

st.subheader("Результаты расчета")
st.dataframe(result_df, use_container_width=True)
