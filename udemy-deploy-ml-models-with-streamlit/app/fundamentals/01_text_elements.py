import streamlit as st

# Text elements in Streamlit
# Title
st.title("Text Elements in Streamlit")

# Header
st.header("This is a header")

# Subheader
st.subheader("This is a subheader")

# Markdown
st.markdown("## This is a markdown header")
st.markdown("This is **bold** text and this is *italic* text.")
st.markdown("Here is a [link](https://www.streamlit.io) to Streamlit.")

# Caption
st.caption("This is a caption.")

# Code
st.code("print('Hello, Streamlit!')", language="python")

# Preformatted text
st.text("This is preformatted text.\nIt preserves whitespace and line breaks.")

# Latex
st.latex(
    r"""
\begin{align*}
a & = b + c \\
d & = e + f
\end{align*}
"""
)

# Divider
st.divider()

# Emojis
st.markdown("Here are some emojis: 😄🚀🌟")

# Blockquote
st.markdown(
    "> This is a blockquote. It is used to highlight important information or quotes."
)

# Lists
st.markdown("### Unordered List")
st.markdown("- Item 1\n- Item 2\n- Item 3")

# Ordered List
st.markdown("### Ordered List")
st.markdown("1. Item 1\n2. Item 2\n3. Item 3")

# Nested Lists
st.markdown("### Nested List")
st.markdown("- Item 1\n  - Subitem 1.1\n  - Subitem 1.2\n- Item 2")

# Write
st.write("This is a simple way to write text or data to the app.")
st.write("You can also write data structures like lists:", [1, 2, 3, 4, 5])
st.write("Or dictionaries:", {"key1": "value1", "key2": "value2"})
st.write("You can even write pandas DataFrames if you have pandas installed.")
