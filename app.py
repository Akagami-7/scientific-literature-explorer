import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import numpy as np
import re
from models.scaledown_client import ScaleDownClient
from models.paper_compressor import PaperCompressor
from models.text_encoder import TextEncoder
from models.vector_engine import VectorEngine
from models.citation_graph import CitationGraph
from models.recommender import Recommender
from auth import AuthManager
from history import HistoryManager

# ---------------------------------------------------
# INITIALIZE MANAGERS
# ---------------------------------------------------

if "auth_manager" not in st.session_state:
    st.session_state.auth_manager = AuthManager()

if "history_manager" not in st.session_state:
    st.session_state.history_manager = HistoryManager()

if "user" not in st.session_state:
    st.session_state.user = None

# Handle Google Auth Redirect
if st.query_params.get("google_id_token"):
    token = st.query_params.get("google_id_token")
    # Clear query param to avoid re-login on refresh
    st.query_params.clear()
    res = st.session_state.auth_manager.login_with_google(token)
    if res["success"]:
        st.session_state.user = res["user"]
        st.rerun()
    else:
        st.error(f"Google Login failed: {res['error']}")

def highlight_query(text, query):
    import re
    words = query.split()
    for word in words:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        text = pattern.sub(
            f"<span style='background-color: #FF954E'>{word}</span>",
            text
        )
    return text

# ---------------------------------------------------
# CONFIG & STYLE
# ---------------------------------------------------

st.set_page_config(page_title="Sci-Lit Explorer", layout="wide")

# Professional CSS Injection
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #262730;
        color: white;
        border: 1px solid #4a4a4a;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        color: #ff4b4b;
    }
    .auth-card {
        padding: 40px;
        border-radius: 10px;
        background-color: #1a1c24;
        border: 1px solid #2d2f39;
        margin: auto;
        max-width: 450px;
    }
    .stTextInput>div>div>input {
        background-color: #1a1c24;
        color: white;
    }
    .stTab {
        font-weight: 600 !important;
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------

if "vector_db" not in st.session_state:
    st.session_state.vector_db = VectorEngine(dimension=768)

if "encoder" not in st.session_state:
    st.session_state.encoder = TextEncoder()

if "recommender" not in st.session_state:
    st.session_state.recommender = Recommender()

if "scaledown" not in st.session_state:
    api_key = os.getenv("SCALEDOWN_API_KEY")  # safer than hardcoding
    if api_key:
        st.session_state.scaledown = ScaleDownClient(api_key)
    else:
        st.session_state.scaledown = None

if "processed" not in st.session_state:
    st.session_state.processed = False


# ---------------------------------------------------
# SIDEBAR & MAIN APP
# ---------------------------------------------------

def main_app():
    user_id = st.session_state.user["localId"]
    st.sidebar.title("Sci-Lit Explorer")
    st.sidebar.write(f"Account: {st.session_state.user['email']}")
    
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    uploaded_file = st.sidebar.file_uploader(
        "Upload Research Paper (PDF)", type="pdf"
    )

    use_ai = st.sidebar.checkbox(
        "Enable AI Compression (uses API credits)"
    )

    if st.session_state.scaledown is None:
        st.sidebar.warning("No API key detected. AI compression disabled.")

    if st.sidebar.button("Clear Database"):
        st.session_state.vector_db.reset()
        st.session_state.processed = False
        st.sidebar.success("Database Cleared!")


    # ---------------------------------------------------
    # PROCESS FILE (ONLY ONCE)
    # ---------------------------------------------------

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

                # NEW: Compress using ScaleDown if available
                if use_ai and st.session_state.scaledown:
                    with st.spinner("Compressing paper with ScaleDown..."):
                        try:
                            compressed = st.session_state.scaledown.compress_paper(full_text)
                            if compressed:
                                full_text = compressed
                        except Exception as e:
                            st.warning("ScaleDown failed. Using original text.")


                # IMPORTANT: Recreate chunks from compressed/full text
                chunks = compressor.split_into_chunks(full_text)

                if len(chunks) > 150:
                    chunks = chunks[:150]
                # Encode chunks
                vectors = st.session_state.encoder.encode(chunks)
                # Store in FAISS
                st.session_state.vector_db.add_documents(
                    vectors,
                    chunks,
                    uploaded_file.name
                )

                st.session_state.vector_db.save_index()

                # Compute document embedding using mean of chunks
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
                st.session_state.history_manager.add_upload(user_id, uploaded_file.name)
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


    # ---------------------------------------------------
    # MAIN UI
    # ---------------------------------------------------

    st.title("Scientific Literature Explorer")
    st.markdown("### Interactive Research Analysis")

    tab1, tab2, tab3 = st.tabs(
        ["Semantic Search", "Citation Graph", "Recommendations"]
    )

    # ---------------------------------------------------
    # TAB 1: SEMANTIC SEARCH
    # ---------------------------------------------------

    with tab1:

        user_query = st.text_input(
            "Search for a concept (e.g., 'Methodology', 'Results'):"
        )

        if user_query and st.session_state.processed:

            with st.spinner("Searching through embeddings..."):
                st.session_state.history_manager.add_search(user_id, user_query)
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


    # ---------------------------------------------------
    # TAB 2: CITATION GRAPH
    # ---------------------------------------------------

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


    # ---------------------------------------------------
    # TAB 3: RECOMMENDATIONS
    # ---------------------------------------------------

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

    # ---------------------------------------------------
    # TAB 4: HISTORY
    # ---------------------------------------------------

    with st.expander("Activity History"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Recent Searches")
            searches = st.session_state.history_manager.get_history(user_id, "search")
            for s in searches:
                st.text(f"- {s['query']} ({s['timestamp'][:16]})")
        
        with col2:
            st.subheader("Recent Uploads")
            uploads = st.session_state.history_manager.get_history(user_id, "upload")
            for u in uploads:
                st.text(f"- {u['filename']} ({u['timestamp'][:16]})")


# ---------------------------------------------------
# LOGIN / SIGNUP PAGE
# ---------------------------------------------------

def login_page():
    st.markdown('<div class="main">', unsafe_allow_html=True)
    
    # Header
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("Sci-Lit Explorer")
        st.markdown("##### Scientific Literature Discovery Platform")
        
        # Auth Card
        with st.container():
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            
            tab_login, tab_signup = st.tabs(["Login", "Create Account"])
            
            with tab_login:
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_pass")
                
                if st.button("Login"):
                    res = st.session_state.auth_manager.login(email, password)
                    if res["success"]:
                        st.session_state.user = res["user"]
                        st.success("Welcome back!")
                        st.rerun()
                    else:
                        st.error(f"Authentication failed: {res['error']}")
                
                st.markdown("---")
                # Firebase JS SDK bridge for Google Login
                auth_config = {
                    "apiKey": os.getenv("FIREBASE_API_KEY"),
                    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
                    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
                    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
                    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
                    "appId": os.getenv("FIREBASE_APP_ID")
                }
                
                import json
                config_json = json.dumps(auth_config)
                
                google_auth_html = f"""
                <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-app-compat.js"></script>
                <script src="https://www.gstatic.com/firebasejs/9.22.1/firebase-auth-compat.js"></script>
                <script>
                    const firebaseConfig = {config_json};
                    firebase.initializeApp(firebaseConfig);
                    const provider = new firebase.auth.GoogleAuthProvider();
                    
                    function signIn() {{
                        firebase.auth().signInWithPopup(provider)
                            .then((result) => {{
                                result.user.getIdToken().then((idToken) => {{
                                    const url = new URL(window.parent.location.href);
                                    url.searchParams.set('google_id_token', idToken);
                                    window.parent.location.href = url.href;
                                }});
                            }}).catch((error) => {{
                                console.error(error);
                                alert("Error during Google Sign-In: " + error.message);
                            }});
                    }}
                </script>
                <button onclick="signIn()" style="
                    width: 100%;
                    height: 3em;
                    background-color: white;
                    color: #757575;
                    border: 1px solid #dadce0;
                    border-radius: 4px;
                    font-family: 'Roboto', arial, sans-serif;
                    font-weight: 500;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 10px;
                ">
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" height="18">
                    Sign in with Google
                </button>
                """
                st.components.v1.html(google_auth_html, height=60)

            with tab_signup:
                new_email = st.text_input("Email", key="signup_email")
                new_pass = st.text_input("Password", type="password", key="signup_pass")
                confirm_pass = st.text_input("Confirm Password", type="password", key="signup_confirm")
                
                if st.button("Sign Up"):
                    if new_pass != confirm_pass:
                        st.error("Passwords do not match")
                    else:
                        res = st.session_state.auth_manager.signup(new_email, new_pass)
                        if res["success"]:
                            st.success("Account created! You can now log in.")
                        else:
                            st.error(f"Registration failed: {res['error']}")

            st.markdown('</div>', unsafe_allow_html=True)
            
            # Footer links
            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Forgot Password?", key="forgot_pass_btn"):
                    st.session_state.show_reset = True
            
            if st.session_state.get("show_reset"):
                reset_email = st.text_input("Enter email for reset link:")
                if st.button("Send Link"):
                    res = st.session_state.auth_manager.reset_password(reset_email)
                    if res["success"]:
                        st.success("Reset link sent!")
                        st.session_state.show_reset = False
                    else:
                        st.error(res["error"])

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# ROUTING
# ---------------------------------------------------

if st.session_state.user is None:
    login_page()
else:
    main_app()
