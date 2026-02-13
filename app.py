import streamlit as st
import os
import numpy as np
import re
from models.scaledown_client import ScaleDownClient
from models.paper_compressor import PaperCompressor
from models.text_encoder import TextEncoder
from models.vector_engine import VectorEngine
from models.citation_graph import CitationGraph
from models.recommender import Recommender

# HIGHLIGHT FUNCTION
def highlight_query(text, query):
    words = query.split()
    for word in words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub(
            f"<span style='background-color: #FF954E'>{word}</span>",
            text
        )
    return text


# CONFIG
st.set_page_config(page_title="Sci-Lit Explorer", layout="wide")


# SESSION STATE INITIALIZATION
if "vector_db" not in st.session_state:
    st.session_state.vector_db = VectorEngine(dimension=768)

if "encoder" not in st.session_state:
    st.session_state.encoder = TextEncoder()

if "recommender" not in st.session_state:
    st.session_state.recommender = Recommender()

if "processed" not in st.session_state:
    st.session_state.processed = False


# SIDEBAR
st.sidebar.title("Sci-Lit Explorer")

uploaded_file = st.sidebar.file_uploader(
    "Upload Research Paper (PDF)", type="pdf"
)

st.sidebar.subheader("ScaleDown API Key (Optional)")

user_api_key = st.sidebar.text_input(
    "Enter your ScaleDown API Key", type="password"
)

use_ai = st.sidebar.checkbox(
    "Enable AI Compression (uses API credits)"
)

st.sidebar.markdown(
    "Generate your API key at [ScaleDown.ai](https://scaledown.ai/)"
)

if use_ai and not user_api_key:
    st.sidebar.warning("Enter API key to enable compression.")

if use_ai and user_api_key:
    st.sidebar.success("AI Compression Enabled")

if st.sidebar.button("Clear Database"):
    st.session_state.vector_db.reset()
    st.session_state.processed = False
    st.sidebar.success("Database Cleared!")


# PROCESS FILE (ONLY ONCE)
if uploaded_file and not st.session_state.processed:

    st.session_state.vector_db.reset()

    with st.spinner("Processing Paper..."):

        # Save file
        os.makedirs("data/uploads", exist_ok=True)
        save_path = os.path.join("data/uploads", uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract content
        compressor = PaperCompressor()
        data = compressor.extract_content(save_path)

        if "error" in data:
            st.error(data["error"])
        else:
            full_text = data["full_text"]

            # 🔹 CONDITIONAL COMPRESSION
            if use_ai and user_api_key:
                with st.spinner("Compressing paper with ScaleDown..."):
                    try:
                        scaledown_client = ScaleDownClient(user_api_key.strip())
                        compressed = scaledown_client.compress_paper(full_text)
                        if compressed:
                            full_text = compressed
                            st.success("Compression successful.")
                        else:
                            st.warning("Compression failed. Using original text.")

                    except Exception as e:
                        st.error(f"ScaleDown Error: {str(e)}")


            elif use_ai and not user_api_key:
                st.warning("Please enter your ScaleDown API key to enable compression.")

            # Recreate chunks from compressed/full text
            chunks = compressor.split_into_chunks(full_text)

            if len(chunks) > 150:
                chunks = chunks[:150]

            # Encode chunks
            vectors = st.session_state.encoder.encode(chunks)

            # Store in vector DB
            st.session_state.vector_db.add_documents(
                vectors,
                chunks,
                uploaded_file.name
            )

            st.session_state.vector_db.save_index()

            # Compute document embedding
            paper_embedding = np.mean(vectors, axis=0)

            st.session_state.recommender.add_paper(
                uploaded_file.name,
                paper_embedding
            )

            # Store metadata
            st.session_state.citation_data = data["citations"]
            st.session_state.paper_title = uploaded_file.name
            st.session_state.full_text = full_text

            st.session_state.processed = True

            st.sidebar.success("Paper Processed Successfully!")

            '''# Encode chunks
            vectors = st.session_state.encoder.encode(data["chunks"])

            # Store in FAISS
            st.session_state.vector_db.add_documents(
                vectors,
                data["chunks"],
                uploaded_file.name
            )

            st.session_state.vector_db.save_index()

            # Compute document embedding using mean of chunks (FAST)
            paper_embedding = np.mean(vectors, axis=0)

            st.session_state.recommender.add_paper(
                uploaded_file.name,
                paper_embedding
            )

            # Store metadata
            st.session_state.citation_data = data["citations"]
            st.session_state.paper_title = uploaded_file.name
            st.session_state.full_text = data["full_text"]

            st.session_state.processed = True

            st.sidebar.success("Paper Processed Successfully!")'''


# MAIN UI
st.title("Scientific Literature Explorer")
st.markdown("### Interactive Research Analysis (Student Edition)")

tab1, tab2, tab3 = st.tabs(
    ["Semantic Search", "Citation Graph", "Recommendations"]
)

# TAB 1: SEMANTIC SEARCH
with tab1:

    user_query = st.text_input(
        "Search for a concept (e.g., 'Methodology', 'Architecture'):"
    )

    if user_query and st.session_state.processed:

        with st.spinner("Searching through embeddings..."):

            query_vec = st.session_state.encoder.encode(user_query)[0]

            results = st.session_state.vector_db.search(query_vec, k=3)

            if results:
                st.success("Top Semantic Matches Found:")

                for i, result in enumerate(results):
                    with st.expander(
                        f"Result {i+1} | Similarity: {result['score']:.4f}",
                        expanded=True
                    ):
                        highlighted_text = highlight_query(
                            result["text"], user_query
                        )
                        st.markdown(highlighted_text, unsafe_allow_html=True)

                        with st.expander("Quick Explanation"):
                            st.write(
                                "This section explains the concept related to your query. "
                                "It likely defines or describes the mechanism in detail."
                            )

                        st.caption(f"Source: {result['source']}")

            else:
                st.warning("No matching sections found.")

    elif not st.session_state.processed:
        st.info("Upload a PDF to begin searching.")


# TAB 2: CITATION GRAPH
with tab2:

    st.header("Citation Network Analysis")

    if st.session_state.processed:

        graph_builder = CitationGraph()

        graph_builder.build_star_graph(
            st.session_state.paper_title,
            st.session_state.citation_data
        )

        fig = graph_builder.get_matplotlib_figure()

        if st.session_state.citation_data:
            st.pyplot(fig)
            st.write(
                f"Detected {len(st.session_state.citation_data)} references."
            )
        else:
            st.warning("No citation markers like [1], [2] found.")

    else:
        st.info("Upload a paper to see citation network.")

# TAB 3: RECOMMENDATIONS
with tab3:

    st.header("Content-Based Recommendations")

    if st.session_state.processed:

        # Use mean embedding we already computed
        query_embedding = np.mean(
            st.session_state.vector_db.index.reconstruct_n(
                0, st.session_state.vector_db.index.ntotal
            ),
            axis=0
        )

        recommendations = st.session_state.recommender.get_recommendations(
            query_embedding
        )

        if recommendations:
            for rec in recommendations:
                st.info(
                    f"**{rec['title']}**\n\nSimilarity Score: {rec['score']:.4f}"
                )
        else:
            st.warning("No recommendations available yet.")

    else:
        st.info("Upload a paper to generate recommendations.")


# TAB 4: AI INSIGHTS
# with tab4:

#     st.header("AI Research Insights")

#     if st.session_state.processed and st.session_state.scaledown:

#         with st.spinner("Generating research insights..."):

#             insights = st.session_state.scaledown.extract_insights(
#                 st.session_state.full_text
#             )

#             if insights:
#                 st.subheader("Key Contributions")
#                 st.write(insights.get("contributions", "Not available"))

#                 st.subheader("Research Gaps")
#                 st.write(insights.get("gaps", "Not available"))

#                 st.subheader("Future Work")
#                 st.write(insights.get("future_work", "Not available"))
#             else:
#                 st.warning("Could not generate insights.")
#     else:
#         st.info("Upload paper and configure API key to use AI insights.")
