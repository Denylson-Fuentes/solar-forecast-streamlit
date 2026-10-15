import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(
    page_title="Solar Forecast Demo",
    page_icon="☀️",
    layout="wide",
)

st.title("☀️ Probabilistic Solar Irradiance Forecast")
st.markdown(
    """
    A simplified demo of the forecasting system from my
    [portfolio](https://your-portfolio-url.netlify.app).

    Shows a forecast with **P10/P50/P90 uncertainty bands**, benchmarked
    against the clear-sky baseline.
    """
)

col1, col2 = st.columns(2)
with col1:
    hours_ahead = st.slider("Forecast horizon (hours)", 6, 48, 24, step=6)
with col2:
    cloud_cover = st.slider("Cloud cover (%)", 0, 100, 30, step=5)

# --- Forecast logic ---
np.random.seed(42)
hours = np.arange(hours_ahead)
now = datetime.now()

hour_of_day = (now.hour + hours) % 24
clear_sky = 900 * np.sin(np.pi * (hour_of_day - 6) / 12)
clear_sky = np.maximum(clear_sky, 0)

attenuation = 1 - (cloud_cover / 100) * 0.7
p50 = clear_sky * attenuation

uncertainty = 20 + hours * 4
p10 = np.maximum(p50 - 1.28 * uncertainty, 0)
p90 = p50 + 1.28 * uncertainty

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(hours, p10, p90, alpha=0.25, color="#52B788", label="P10–P90 range")
ax.plot(hours, p50, color="#1B4332", linewidth=2, label="P50 forecast")
ax.plot(hours, clear_sky, "--", color="#F4A261", linewidth=1.5, label="Clear-sky baseline")

ax.set_xlabel("Hour ahead")
ax.set_ylabel("GHI (W/m²)")
ax.set_title(f"Forecast — {hours_ahead}h ahead, {cloud_cover}% cloud cover")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()

st.pyplot(fig)

st.markdown("---")
st.markdown(
    """
    **About this demo:** The plot above is a simplified probabilistic forecast.
    The full project (available on my portfolio) trains a Random Forest model
    on NSRDB solar data and NWP forecasts, achieving a P10-P90 coverage of ~73%.
    """
)