# recipe_explorer_app.py
import streamlit as st
from textwrap import shorten
import pandas as pd
import numpy as np
import plotly.express as px
import random

st.set_page_config(
    page_title="Recipe Explorer",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Sample data ----------
@st.cache_data
def load_sample_recipes():
    # A small dataset of recipes; in a real app you'd read a DB or API.
    recipes = [
        {
            "id": 1,
            "title": "Spicy Chickpea Curry",
            "cuisine": "Indian",
            "time_mins": 30,
            "difficulty": "Easy",
            "rating": 4.5,
            "ingredients": ["chickpeas", "tomato", "onion", "garlic", "spices"],
            "image": "https://images.unsplash.com/photo-1604908177522-3d5f6b9a3c1b?auto=format&q=60&fit=crop&w=800"
        },
        {
            "id": 2,
            "title": "Creamy Mushroom Pasta",
            "cuisine": "Italian",
            "time_mins": 25,
            "difficulty": "Easy",
            "rating": 4.2,
            "ingredients": ["pasta", "mushroom", "cream", "parmesan"],
            "image": "https://images.unsplash.com/photo-1523986371872-9d3ba2e2f642?auto=format&q=60&fit=crop&w=800"
        },
        {
            "id": 3,
            "title": "Korean Bibimbap",
            "cuisine": "Korean",
            "time_mins": 45,
            "difficulty": "Medium",
            "rating": 4.7,
            "ingredients": ["rice", "spinach", "carrot", "egg", "gochujang"],
            "image": "https://images.unsplash.com/photo-1604908813613-9f2b8d6a3d67?auto=format&q=60&fit=crop&w=800"
        },
        {
            "id": 4,
            "title": "Avocado Toast Deluxe",
            "cuisine": "American",
            "time_mins": 10,
            "difficulty": "Easy",
            "rating": 4.0,
            "ingredients": ["bread", "avocado", "lemon", "chili"],
            "image": "https://images.unsplash.com/photo-1551183053-bf91a1d81141?auto=format&q=60&fit=crop&w=800"
        },
        {
            "id": 5,
            "title": "Shakshuka",
            "cuisine": "Middle Eastern",
            "time_mins": 35,
            "difficulty": "Medium",
            "rating": 4.6,
            "ingredients": ["tomato", "egg", "pepper", "onion", "cumin"],
            "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&q=60&fit=crop&w=800"
        },
    ]
    return pd.DataFrame(recipes)

recipes_df = load_sample_recipes()

# ---------- Helpers ----------
def toggle_favorite(recipe_id):
    favs = st.session_state.get("favorites", set())
    if recipe_id in favs:
        favs.remove(recipe_id)
    else:
        favs.add(recipe_id)
    st.session_state["favorites"] = favs

def is_available(needed, pantry):
    return all(item.lower() in pantry for item in needed)

# Initialize favorites in session_state
if "favorites" not in st.session_state:
    st.session_state["favorites"] = set()

# ---------- Layout: header ----------
st.markdown("<h1 style='margin-bottom:0.2rem'>🥗 Recipe Explorer</h1>", unsafe_allow_html=True)
st.markdown("<small>Discover recipes, check ingredient availability, and save favorites — responsive UI.</small>", unsafe_allow_html=True)
st.write("---")

# ---------- Sidebar controls ----------
with st.sidebar:
    st.header("Filter & Search")
    search_text = st.text_input("Search recipes", placeholder="e.g. pasta, chickpea, shakshuka")
    cuisine_options = ["All"] + sorted(recipes_df["cuisine"].unique().tolist())
    cuisine = st.selectbox("Cuisine", cuisine_options)
    max_time = st.slider("Max cook time (mins)", min_value=5, max_value=120, value=45, step=5)
    difficulty = st.multiselect("Difficulty", options=["Easy", "Medium", "Hard"], default=["Easy", "Medium", "Hard"])
    sort_by = st.radio("Sort by", options=["Recommended", "Time (asc)", "Rating (desc)"], index=0)

    st.write("---")
    st.subheader("Ingredient Checker")
    pantry_raw = st.text_area("What you have (comma separated)", placeholder="e.g. tomato, onion, rice")
    pantry_list = [p.strip().lower() for p in pantry_raw.split(",") if p.strip()]
    st.caption("Tip: enter ingredient names separated by commas.")

    st.write("---")
    st.markdown("Made with ❤️ using Streamlit — mobile friendly layout.")

# ---------- Filter recipes ----------
filtered = recipes_df.copy()

# Search
if search_text:
    mask = filtered["title"].str.contains(search_text, case=False) | filtered["ingredients"].apply(lambda lst: any(search_text.lower() in ing.lower() for ing in lst))
    filtered = filtered[mask]

# Cuisine
if cuisine != "All":
    filtered = filtered[filtered["cuisine"] == cuisine]

# Time & difficulty
filtered = filtered[(filtered["time_mins"] <= max_time) & (filtered["difficulty"].isin(difficulty))]

# Sorting
if sort_by == "Time (asc)":
    filtered = filtered.sort_values("time_mins", ascending=True)
elif sort_by == "Rating (desc)":
    filtered = filtered.sort_values("rating", ascending=False)
else:
    # "Recommended" - shuffle slightly but bias by rating
    filtered = filtered.sample(frac=1, random_state=42).sort_values("rating", ascending=False).reset_index(drop=True)

# ---------- Main UI: show a summary and a chart ----------
col1, col2 = st.columns([3,1])
with col1:
    st.subheader(f"Results — {len(filtered)} recipe(s)")
    st.caption("Tap a card to expand details. Use the Ingredient Checker in the sidebar to see availability.")
with col2:
    # Small ratings distribution chart
    fig = px.histogram(recipes_df, x="rating", nbins=5, title="Ratings distribution", labels={"rating":"rating"})
    fig.update_layout(margin=dict(l=0,r=0,t=30,b=0), height=220)
    st.plotly_chart(fig, use_container_width=True)

st.write("")

# ---------- Responsive recipe cards ----------
# We will render cards in rows of 3 (or fewer on smaller screens)
def render_card(row):
    rid = int(row["id"])
    title = row["title"]
    img = row["image"]
    cuisine = row["cuisine"]
    time = row["time_mins"]
    diff = row["difficulty"]
    rating = row["rating"]
    ingredients = row["ingredients"]

    # Card layout: use columns to place image + text
    st.image(img, caption=f"{title} — {cuisine}", use_column_width=True)
    st.markdown(f"**{title}**  ·  {cuisine}  ·  ⏱ {time} mins  ·  {diff}  ·  ⭐ {rating}")
    st.write(shorten(", ".join(ingredients), width=80, placeholder="..."))
    # Buttons: Favorite + Expand
    cols = st.columns([1,4,2])
    with cols[0]:
        if st.button(("★ Remove" if rid in st.session_state["favorites"] else "☆ Save"), key=f"fav_{rid}"):
            toggle_favorite(rid)
    with cols[1]:
        # Details in an expander
        with st.expander("View details & quick actions"):
            st.markdown("**Ingredients:**")
            st.write(", ".join(ingredients))
            st.markdown("**Quick cook tips:**")
            st.write("- Use fresh spices for the best aroma.\n- Adjust chili to taste.")
            # Availability check
            if pantry_list:
                present = [ing for ing in ingredients if ing.lower() in pantry_list]
                missing = [ing for ing in ingredients if ing.lower() not in pantry_list]
                st.markdown("**Pantry check:**")
                st.write(f"Available: {', '.join(present) if present else '—'}")
                st.write(f"Missing: {', '.join(missing) if missing else '—'}")
                if not missing:
                    st.success("You have everything you need! 🎉")
                else:
                    st.warning(f"Missing {len(missing)} item(s).")
            else:
                st.info("Enter items in the Ingredient Checker (sidebar) to see availability.")
            # Fake nutrition estimate
            calories = int(150 + 10 * random.random() * time)
            st.metric("Estimated calories", f"{calories} kcal")
            st.markdown("---")
            if st.button("Generate shopping list", key=f"shop_{rid}"):
                st.write("Shopping list:")
                st.write("\n".join(f"- {m}" for m in missing) if pantry_list else "Please add pantry items first.")

    with cols[2]:
        st.write("")  # small spacer

# Render cards in rows with columns
cards_per_row = 3
rows = [filtered.iloc[i:i+cards_per_row] for i in range(0, len(filtered), cards_per_row)]
for row_df in rows:
    cols = st.columns(len(row_df))
    for col, (_, r) in zip(cols, row_df.iterrows()):
        with col:
            render_card(r)

st.write("---")

# ---------- Favorites summary ----------
st.subheader("❤️ Favorites")
if st.session_state["favorites"]:
    favs = recipes_df[recipes_df["id"].isin(list(st.session_state["favorites"]))]
    for _, f in favs.iterrows():
        st.write(f"- {f['title']} ({f['cuisine']}) — ⭐ {f['rating']}")
else:
    st.write("No favorites yet — tap ☆ Save on any recipe card to add one.")

# ---------- Footer / small interactive demo: compare two recipes ----------
st.write("---")
st.subheader("Compare two recipes")
left, right = st.columns(2)
left_choice = left.selectbox("Left recipe", options=recipes_df["title"].tolist(), key="cmp_left")
right_choice = right.selectbox("Right recipe", options=recipes_df["title"].tolist(), key="cmp_right")

if left_choice and right_choice:
    a = recipes_df[recipes_df["title"] == left_choice].iloc[0]
    b = recipes_df[recipes_df["title"] == right_choice].iloc[0]
    comp = pd.DataFrame({
        "metric": ["cook time (mins)", "difficulty", "rating", "ingredients_count"],
        "left": [a["time_mins"], a["difficulty"], a["rating"], len(a["ingredients"])],
        "right": [b["time_mins"], b["difficulty"], b["rating"], len(b["ingredients"])]
    })
    st.table(comp)

# ---------- End ----------
st.caption("Demo app — you can connect this to your database or add uploads. Want this adapted to your recipe dataset? Ask and I'll tailor it!")
