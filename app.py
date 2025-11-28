"""
Amazon Q Prompt Library - Web App
Central collection of reusable Amazon Q prompts
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Configuration
DATA_FILE = Path(__file__).parent / "data" / "prompts.json"
DATA_FILE.parent.mkdir(exist_ok=True)

# Categories
CATEGORIES = [
    "API Development",
    "Testing",
    "Documentation",
    "Refactoring",
    "Data Processing",
    "DevOps/CI-CD",
    "Architecture",
    "Debugging",
    "Code Review",
    "Other"
]

def load_prompts() -> List[Dict]:
    """Load prompts from JSON file"""
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_prompts(prompts: List[Dict]):
    """Save prompts to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)

def add_prompt(title: str, category: str, prompt: str, author: str, tags: List[str]):
    """Add new prompt to library"""
    prompts = load_prompts()
    new_prompt = {
        "id": len(prompts) + 1,
        "title": title,
        "category": category,
        "prompt": prompt,
        "author": author,
        "tags": tags,
        "rating": 0,
        "votes": 0,
        "usage_count": 0,
        "created_at": datetime.now().isoformat(),
        "comments": []
    }
    prompts.append(new_prompt)
    save_prompts(prompts)
    return new_prompt

def update_usage(prompt_id: int):
    """Increment usage counter"""
    prompts = load_prompts()
    for p in prompts:
        if p["id"] == prompt_id:
            p["usage_count"] += 1
            break
    save_prompts(prompts)

def add_rating(prompt_id: int, rating: int):
    """Add rating to prompt"""
    prompts = load_prompts()
    for p in prompts:
        if p["id"] == prompt_id:
            p["rating"] = ((p["rating"] * p["votes"]) + rating) / (p["votes"] + 1)
            p["votes"] += 1
            break
    save_prompts(prompts)

# Streamlit App
st.set_page_config(
    page_title="Amazon Q Prompt Library",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Amazon Q Prompt Library")
st.markdown("**Central collection of reusable Amazon Q prompts**")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    page = st.radio("", ["📚 Browse Prompts", "➕ Submit Prompt", "📊 Statistics"])
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    prompts = load_prompts()
    st.metric("Total Prompts", len(prompts))
    st.metric("Total Usage", sum(p["usage_count"] for p in prompts))
    st.metric("Contributors", len(set(p["author"] for p in prompts)))

# Main Content
if page == "📚 Browse Prompts":
    st.header("Browse Prompts")
    
    # Filters
    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input("🔍 Search", placeholder="Search by title, tags, or content...")
    with col2:
        category_filter = st.selectbox("Category", ["All"] + CATEGORIES)
    
    sort_by = st.selectbox("Sort by", ["Most Recent", "Most Used", "Highest Rated"])
    
    # Load and filter prompts
    prompts = load_prompts()
    
    if category_filter != "All":
        prompts = [p for p in prompts if p["category"] == category_filter]
    
    if search:
        search_lower = search.lower()
        prompts = [p for p in prompts if 
                   search_lower in p["title"].lower() or
                   search_lower in p["prompt"].lower() or
                   any(search_lower in tag.lower() for tag in p["tags"])]
    
    # Sort
    if sort_by == "Most Recent":
        prompts = sorted(prompts, key=lambda x: x["created_at"], reverse=True)
    elif sort_by == "Most Used":
        prompts = sorted(prompts, key=lambda x: x["usage_count"], reverse=True)
    elif sort_by == "Highest Rated":
        prompts = sorted(prompts, key=lambda x: x["rating"], reverse=True)
    
    # Display prompts
    if not prompts:
        st.info("No prompts found. Be the first to submit one!")
    
    for prompt in prompts:
        with st.expander(f"**{prompt['title']}** ({prompt['category']})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"👤 **Author:** {prompt['author']}")
            with col2:
                st.markdown(f"⭐ **Rating:** {prompt['rating']:.1f} ({prompt['votes']} votes)")
            with col3:
                st.markdown(f"📊 **Used:** {prompt['usage_count']}x")
            
            st.markdown("**Prompt:**")
            st.code(prompt['prompt'], language="text")
            
            if prompt['tags']:
                st.markdown(f"**Tags:** {', '.join(f'`{tag}`' for tag in prompt['tags'])}")
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("📋 Copy", key=f"copy_{prompt['id']}"):
                    update_usage(prompt['id'])
                    st.success("Usage tracked. Copy from above.")
            with col2:
                rating = st.selectbox("Rate", [1, 2, 3, 4, 5], key=f"rate_{prompt['id']}")
                if st.button("Submit Rating", key=f"submit_rate_{prompt['id']}"):
                    add_rating(prompt['id'], rating)
                    st.success("Rating submitted!")
                    st.rerun()

elif page == "➕ Submit Prompt":
    st.header("Submit New Prompt")
    
    with st.form("submit_prompt"):
        title = st.text_input("Title*", placeholder="e.g., API Client Generator")
        category = st.selectbox("Category*", CATEGORIES)
        prompt = st.text_area("Prompt*", height=300, placeholder="Enter your Kiro prompt here...")
        author = st.text_input("Your Name*", placeholder="e.g., John Doe")
        tags_input = st.text_input("Tags (comma-separated)", placeholder="e.g., python, api, rest")
        
        submitted = st.form_submit_button("Submit Prompt")
        
        if submitted:
            if not all([title, category, prompt, author]):
                st.error("Please fill all required fields (*)")
            else:
                tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                new_prompt = add_prompt(title, category, prompt, author, tags)
                st.success(f"✅ Prompt '{title}' submitted successfully!")
                st.info("Your prompt is now available in the library!")

elif page == "📊 Statistics":
    st.header("Library Statistics")
    
    prompts = load_prompts()
    
    if not prompts:
        st.info("No data yet. Submit the first prompt!")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Prompts", len(prompts))
        with col2:
            st.metric("Total Usage", sum(p["usage_count"] for p in prompts))
        with col3:
            avg_rating = sum(p["rating"] for p in prompts if p["votes"] > 0) / len([p for p in prompts if p["votes"] > 0]) if any(p["votes"] > 0 for p in prompts) else 0
            st.metric("Avg Rating", f"{avg_rating:.1f}⭐")
        with col4:
            st.metric("Contributors", len(set(p["author"] for p in prompts)))
        
        st.markdown("---")
        
        # Top prompts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🔥 Most Used Prompts")
            top_used = sorted(prompts, key=lambda x: x["usage_count"], reverse=True)[:5]
            for i, p in enumerate(top_used, 1):
                st.markdown(f"{i}. **{p['title']}** - {p['usage_count']} uses")
        
        with col2:
            st.subheader("⭐ Highest Rated Prompts")
            top_rated = sorted([p for p in prompts if p["votes"] > 0], key=lambda x: x["rating"], reverse=True)[:5]
            for i, p in enumerate(top_rated, 1):
                st.markdown(f"{i}. **{p['title']}** - {p['rating']:.1f}⭐ ({p['votes']} votes)")
        
        st.markdown("---")
        
        # Category distribution
        st.subheader("📂 Prompts by Category")
        category_counts = {}
        for p in prompts:
            category_counts[p["category"]] = category_counts.get(p["category"], 0) + 1
        
        for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            st.markdown(f"- **{cat}:** {count} prompts")
        
        st.markdown("---")
        
        # Top contributors
        st.subheader("👥 Top Contributors")
        author_counts = {}
        for p in prompts:
            author_counts[p["author"]] = author_counts.get(p["author"], 0) + 1
        
        for author, count in sorted(author_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            st.markdown(f"- **{author}:** {count} prompts")

# Footer
st.markdown("---")
st.markdown("**Amazon Q Prompt Library** | Built with ❤️ | [Submit Feedback](https://github.com)")
