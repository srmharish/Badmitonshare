import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import io

# ----- App Setup -----
st.set_page_config(
    page_title="Share Calculator",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----- Custom Styling -----
st.markdown("""
    <style>
        .main {
            background-color: #f5f5fa;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 {
            color: #333333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stDownloadButton>button {
            background-color: #1E88E5;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stTextInput>div>input, .stNumberInput>div>input {
            background-color: #ffffff;
            border-radius: 6px;
            padding: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# ----- App Title -----
st.title("💸 Share Calculator")

# Upload Excel file
uploaded_file = st.file_uploader("📤 Upload Excel File (Column A = Player Names)", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, usecols=[0], names=["Player"])
        df.dropna(inplace=True)
        player_names = df["Player"].astype(str).tolist()

        st.subheader("✅ Select Players:")
        selected_players = st.multiselect("Choose players to include:", player_names)

        amount = st.number_input("💰 Enter Total Amount (₹)", min_value=0.0, format="%.2f")

        if st.button("Calculate & Save as Image"):
            if not selected_players:
                st.warning("Please select at least one player.")
            elif amount <= 0:
                st.warning("Please enter a valid amount.")
            else:
                per_share = amount / len(selected_players)

                # Draw image
                height = 60 + 80 * len(selected_players)
                img = Image.new("RGB", (600, height), "white")
                draw = ImageDraw.Draw(img)

                try:
                    font = ImageFont.truetype("Calibri.ttf", 20)
                except:
                    font = ImageFont.load_default()

                y = 20
                draw.text((20, y), f"Total Amount: ₹{amount:.2f}", fill="black", font=font)
                y += 30
                draw.text((20, y), f"Per Player Share: ₹{per_share:.2f}", fill="black", font=font)
                y += 30
                draw.text((20, y), "Players:", fill="black", font=font)
                y += 30

                for i, name in enumerate(selected_players, start=1):
                    draw.text((40, y), f"{i}. {name}", fill="black", font=font)
                    y += 30

                # Save to buffer
                buffer = io.BytesIO()
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                img.save(buffer, format="JPEG")
                buffer.seek(0)

                st.success("✅ Image created successfully!")
                st.image(buffer, caption="Result Image Preview", use_column_width=True)

                # Download button
                st.download_button(
                    label="📥 Download Result Image",
                    data=buffer,
                    file_name=f"Player Share_{timestamp}.jpg",
                    mime="image/jpeg"
                )

    except Exception as e:
        st.error(f"❌ Error reading Excel file: {e}")
