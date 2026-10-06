import streamlit as st
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# STEP 1: API Configuration
# -----------------------------------------------------------------------------
# Ensure you have your Gemini API key set up.
# You can set it as an environment variable: export GEMINI_API_KEY="your_key"
# Or let the user input it directly in the app if not found.
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

# Fallback initialization
if api_key:
    client = genai.Client(api_key=api_key)
else:
    # This will automatically look for the GEMINI_API_KEY environment variable
    try:
        client = genai.Client()
    except Exception:
        client = None

# -----------------------------------------------------------------------------
# STEP 2: App UI Setup
# -----------------------------------------------------------------------------
st.set_page_config(page_title="AI Fashion Stylist", page_icon="👗", layout="centered")

st.title("👗 Your AI Fashion Companion")
st.write("Input an item from your wardrobe, choose the occasion, and get two fully styled outfit recommendations.")

# -----------------------------------------------------------------------------
# STEP 3: User Inputs (Sidebar)
# -----------------------------------------------------------------------------
st.sidebar.header("Describe Your Base Item")

item_type = st.sidebar.selectbox(
    "What type of item is it?",
    ["Blouse/Shirt", "T-Shirt", "Sweater/Cardigan", "Blazer/Jacket", "Trousers/Jeans", "Skirt", "Dress", "Shoes", "Accessory (Bag, Scarf, etc.)"]
)

item_color = st.sidebar.text_input("What color is it?", placeholder="e.g., Salmon pink, Navy blue, Emerald green")
item_pattern = st.sidebar.text_input("What is the pattern?", placeholder="e.g., Solid, Stripes, Floral, Polka dot", value="Solid")

st.sidebar.header("The Occasion")
occasion = st.sidebar.selectbox(
    "Where are you wearing this?",
    ["Work / Professional", "Casual Everyday", "Church / Formal Religious", "Working From Home (WFH)", "Party / Night Out", "Wedding Guest", "Date Night"]
)

generate_button = st.sidebar.button("Style My Outfit ✨", type="primary")

# -----------------------------------------------------------------------------
# STEP 4: Styling Prompt & AI Execution
# -----------------------------------------------------------------------------
if generate_button:
    if not client:
        st.error("Please provide a valid Gemini API Key in the sidebar or set the GEMINI_API_KEY environment variable.")
    elif not item_color:
        st.warning("Please enter a color for your item to get the best styling results.")
    else:
        # Construct a detailed, structured prompt ensuring a highly scannable output
        prompt = f"""
        You are an expert personal fashion stylist. 
        The user wants to build an outfit around the following base item:
        - Type: {item_type}
        - Color: {item_color}
        - Pattern: {item_pattern}
        
        The outfit must be perfectly tailored for this occasion: {occasion}.

        Provide exactly TWO distinct styling options. Each option must build a complete look by adding at least 2-3 other complementary clothing pieces, footwear, and accessories.
        
        Format your response cleanly using Markdown:
        
        ### 🌟 Option 1: [Give this style vibe a name]
        *Why it works:* [Brief 1-sentence logic statement on the color theory/vibe]
        *   **Bottoms/Tops (as needed):** [Specific item, color, and fabric]
        *   **Layering (Blazer/Jacket):** [Specific item, color]
        *   **Shoes:** [Specific type and color]
        *   **Accessories:** [Jewelry, bag, or belt details]

        ### 🌟 Option 2: [Give this style vibe a name]
        *Why it works:* [Brief 1-sentence logic statement on the color theory/vibe]
        *   **Bottoms/Tops (as needed):** [Specific item, color, and fabric]
        *   **Layering (Blazer/Jacket):** [Specific item, color]
        *   **Shoes:** [Specific type and color]
        *   **Accessories:** [Jewelry, bag, or belt details]
        """

        with st.spinner("Analyzing color theory and trends..."):
            try:
                # Using the recommended gemini-3.8-flash model for fast, accurate text responses
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt,
                )
                
                # Display results
                st.success("Here are your curated outfits!")
                st.markdown(f"### Base Item: **{item_color} {item_pattern} {item_type}** for **{occasion}**")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred while generating your styles: {e}")

# -----------------------------------------------------------------------------
# STEP 5: Footer instructions
# -----------------------------------------------------------------------------
if not generate_button:
    st.info("Fill out the details in the left sidebar and click 'Style My Outfit' to begin!")
  
