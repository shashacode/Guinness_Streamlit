"""
🍺 Guinness Selfie Generator - Streamlit App
Generate selfies with Messi or Ronaldo holding a pint of Guinness!
"""

import streamlit as st
from openai import OpenAI
import base64
from PIL import Image
from io import BytesIO
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="🍺 Guinness Selfie Generator",
    page_icon="🍺",
    layout="wide"
)

# Title and description
st.title("🍺 Guinness Selfie Generator")
st.markdown("Generate a legendary selfie with Messi or Ronaldo while holding a pint of Guinness! ⚽✨")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# Get API Key from Streamlit secrets or environment variables
try:
    api_key = st.secrets["OPENROUTER_API_KEY"]
except (KeyError, FileNotFoundError):
    try:
        import os
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("API key not found")
    except:
        st.error("❌ OpenRouter API Key not configured!")
        st.info("""
        **To configure your API key:**
        
        **For Streamlit Cloud:**
        1. Go to your app settings
        2. Click on "Secrets"
        3. Add: `OPENROUTER_API_KEY = "your-api-key-here"`
        
        **For Local Development:**
        1. Create `.streamlit/secrets.toml` file
        2. Add: `OPENROUTER_API_KEY = "your-api-key-here"`
        
        **Or use environment variable:**
        ```bash
        export OPENROUTER_API_KEY="your-api-key-here"
        streamlit run guinness_selfie_streamlit.py
        ```
        
        Get your API key from: https://openrouter.ai/keys
        """)
        st.stop()

st.sidebar.success("✅ API Key Loaded")

# Footballer selection
footballer = st.sidebar.selectbox(
    "Choose Footballer",
    options=["Ronaldo", "Messi", "Both"],
    help="Who do you want in your selfie?"
)

# Style selection
style = st.sidebar.selectbox(
    "Choose Style",
    options=["Casual", "Photorealistic", "Cinematic", "Professional"],
    help="Select the style for your generated image"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Model Info")
st.sidebar.markdown("**Model:** google/gemini-2.5-flash-image-preview")
st.sidebar.markdown("**Endpoint:** OpenRouter API")

# Initialize session state
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'generation_history' not in st.session_state:
    st.session_state.generation_history = []

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📸 Upload Your Photo")
    uploaded_file = st.file_uploader(
        "Choose a photo...",
        type=["png", "jpg", "jpeg"],
        help="Upload a clear photo of yourself"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        user_image = Image.open(uploaded_file)
        st.image(user_image, caption="Your Photo", use_container_width=True)
        
        # Image info
        st.caption(f"Size: {user_image.size[0]}x{user_image.size[1]} pixels | Format: {user_image.format}")

with col2:
    st.header("✨ Generated Selfie")
    
    if st.session_state.generated_image is not None:
        st.image(st.session_state.generated_image, caption="Your Legendary Selfie! 🎉", use_container_width=True)
        
        # Download button
        buffered = BytesIO()
        st.session_state.generated_image.save(buffered, format="PNG")
        st.download_button(
            label="💾 Download Image",
            data=buffered.getvalue(),
            file_name=f"guinness_selfie_{footballer.lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png"
        )
    else:
        st.info("👈 Upload a photo and click 'Generate Selfie' to see your result here!")

# Generate button
st.markdown("---")

generate_col1, generate_col2, generate_col3 = st.columns([1, 2, 1])

with generate_col2:
    generate_button = st.button(
        "🎨 Generate Selfie",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_file is None)
    )

if generate_button:
    if uploaded_file is None:
        st.error("❌ Please upload a photo first!")
    else:
        # Build footballer description
        if footballer == "Messi":
            footballer_desc = "Lionel Messi in his Argentina national team jersey"
        elif footballer == "Ronaldo":
            footballer_desc = "Cristiano Ronaldo in his Portugal national team jersey"
        else:
            footballer_desc = "Lionel Messi in his Argentina jersey and Cristiano Ronaldo in his Portugal jersey"
        
        # Create prompt
        prompt = f"""Create a {style.lower()} image where the person in the provided photo is taking a selfie
with {footballer_desc}. The person should be holding a pint of Guinness beer with the iconic
dark stout and creamy white head. All people are looking at the camera as if taking
a group selfie. The setting in the original image should be maintained.
The person's face from the original image should be preserved exactly as it appears.
Make it look natural and celebratory, like they just met their football heroes.
The Guinness glass should be clearly visible and recognizable."""
        
        # Convert image to base64
        user_image = Image.open(uploaded_file)
        buffered = BytesIO()
        user_image.save(buffered, format="PNG")
        user_img_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        # Show progress
        with st.spinner(f"🎨 Generating your selfie with {footballer}... This may take 10-30 seconds..."):
            try:
                # Initialize OpenAI client with OpenRouter
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                )
                
                # Call API
                completion = client.chat.completions.create(
                    model="google/gemini-2.5-flash-image-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "I will provide my photo:"
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{user_img_b64}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ],
                    modalities=["image"],
                    extra_body={"n": 1}
                )
                
                # Parse response
                message = completion.choices[0].message
                image_found = False
                
                # Method 1: Check content field
                if hasattr(message, "content") and message.content:
                    for part in message.content:
                        part_type = getattr(part, "type", None)
                        
                        if part_type in ["output_image", "image_url"] and hasattr(part, "image_url"):
                            img_url = part.image_url.url
                            
                            if img_url.startswith("data:image"):
                                # Extract base64 data
                                img_b64 = img_url.split(",", 1)[1]
                                
                                # Decode and create image
                                img_data = base64.b64decode(img_b64)
                                generated_image = Image.open(BytesIO(img_data))
                                
                                # Store in session state
                                st.session_state.generated_image = generated_image
                                
                                # Add to history
                                st.session_state.generation_history.append({
                                    'timestamp': datetime.now(),
                                    'footballer': footballer,
                                    'style': style,
                                    'image': generated_image
                                })
                                
                                image_found = True
                                st.success("✅ Selfie generated successfully!")
                                st.rerun()
                                break
                
                # Method 2: Fallback - check images field
                if not image_found and hasattr(message, "images") and message.images:
                    for image in message.images:
                        img_url = image.get("image_url", {}).get("url", "")
                        
                        if img_url.startswith("data:image"):
                            img_b64 = img_url.split(",", 1)[1]
                            img_data = base64.b64decode(img_b64)
                            generated_image = Image.open(BytesIO(img_data))
                            
                            st.session_state.generated_image = generated_image
                            st.session_state.generation_history.append({
                                'timestamp': datetime.now(),
                                'footballer': footballer,
                                'style': style,
                                'image': generated_image
                            })
                            
                            image_found = True
                            st.success("✅ Selfie generated successfully!")
                            st.rerun()
                            break
                
                if not image_found:
                    st.error("⚠️ No image found in the API response. Please try again.")
                    st.info("💡 Troubleshooting:\n"
                            "1. Check your OpenRouter API key is valid\n"
                            "2. Verify you have credits/quota on OpenRouter\n"
                            "3. Visit https://openrouter.ai/activity to see API logs\n"
                            "4. Try a smaller image (< 5MB)")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Troubleshooting:\n"
                        "1. Check your OpenRouter API key is valid\n"
                        "2. Verify you have credits/quota on OpenRouter\n"
                        "3. Visit https://openrouter.ai/activity to see API logs\n"
                        "4. Check image size (should be < 5MB)")

# Generation history
if st.session_state.generation_history:
    st.markdown("---")
    st.header("📂 Generation History")
    
    # Show last 6 generations
    cols = st.columns(3)
    for idx, item in enumerate(reversed(st.session_state.generation_history[-6:])):
        col_idx = idx % 3
        with cols[col_idx]:
            st.image(item['image'], caption=f"{item['footballer']} - {item['style']}", use_container_width=True)
            st.caption(item['timestamp'].strftime('%Y-%m-%d %H:%M:%S'))

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Made with ❤️ using OpenRouter + Gemini 🍺⚽✨</p>
        <p><a href="https://openrouter.ai/keys" target="_blank">Get API Key</a> | 
        <a href="https://openrouter.ai/docs" target="_blank">Docs</a> | 
        <a href="https://openrouter.ai/activity" target="_blank">Usage</a></p>
    </div>
    """,
    unsafe_allow_html=True
)

