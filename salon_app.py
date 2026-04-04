"""Beauty salon Streamlit UI: themed login, booking, and AI advice."""

import streamlit as st
import streamlit.components.v1 as components

from bot import ask_beauty_advisor, get_llm_key_and_provider


def _inject_theme_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(145deg, #fff0f7 0%, #f5e8ff 45%, #fce4ec 100%);
        }
        .block-container { padding-top: 1.2rem; max-width: 720px; }
        h1, h2, h3 {
            background: linear-gradient(90deg, #db2777, #9333ea, #7c3aed);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        div[data-testid="stHorizontalBlock"] button {
            background: linear-gradient(90deg, #ec4899, #a855f7) !important;
            color: white !important;
            border: none !important;
            border-radius: 999px !important;
            font-weight: 600 !important;
            padding: 0.5rem 1.25rem !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        div[data-testid="stHorizontalBlock"] button:hover {
            box-shadow: 0 6px 20px rgba(168, 85, 247, 0.45);
            transform: translateY(-1px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _login_html_banner():
    components.html(
        """
        <div style="
            font-family: 'Segoe UI', system-ui, sans-serif;
            text-align: center;
            padding: 1.5rem 1rem 0.5rem;
            animation: fadeUp 0.8s ease-out both;
        ">
            <style>
            @keyframes fadeUp {
                from { opacity: 0; transform: translateY(28px) scale(0.98); }
                to { opacity: 1; transform: translateY(0) scale(1); }
            }
            @keyframes pulseGlow {
                0%, 100% { filter: drop-shadow(0 0 8px rgba(236,72,153,0.35)); }
                50% { filter: drop-shadow(0 0 18px rgba(168,85,247,0.55)); }
            }
            .sparkle { font-size: 2.5rem; animation: pulseGlow 2.2s ease-in-out infinite; }
            </style>
            <div class="sparkle">💅✨</div>
            <div style="
                font-size: 1.35rem;
                font-weight: 700;
                background: linear-gradient(90deg,#db2777,#9333ea);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-top: 0.35rem;
            ">Welcome to Glow Studio</div>
            <div style="color:#9d174d;opacity:0.85;font-size:0.95rem;margin-top:0.25rem;">
                Sign in to book &amp; get personalized tips
            </div>
        </div>
        """,
        height=200,
    )


def _init_session():
    defaults = {
        "logged_in": False,
        "client_name": "",
        "client_age": None,
        "appointments": [],
        "login_pulse": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def run():
    st.set_page_config(
        page_title="Glow Studio — Beauty Salon",
        page_icon="💅",
        layout="centered",
    )
    _inject_theme_css()
    _init_session()

    if not st.session_state.logged_in:
        _login_html_banner()
        st.subheader("Client login")
        name = st.text_input("Your name", placeholder="e.g. Maya", key="login_name")
        age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
        go = st.button("Enter the salon ✨", type="primary", use_container_width=True)

        if go:
            name_clean = (name or "").strip()
            if not name_clean:
                st.warning("Please enter your name.")
            else:
                st.session_state.client_name = name_clean
                st.session_state.client_age = int(age)
                st.session_state.logged_in = True
                st.session_state.login_pulse = True
                st.balloons()
                st.rerun()
        return

    provider, api_key = get_llm_key_and_provider()

    if st.session_state.get("login_pulse"):
        components.html(
            """
            <div style="height:8px;background:linear-gradient(90deg,#f472b6,#c084fc,#f472b6);
            background-size:200% 100%;animation:sh 1.2s ease infinite;border-radius:4px;margin:0 0 12px 0;">
            <style>@keyframes sh{0%{background-position:0% 50%}100%{background-position:200% 50%}}</style>
            </div>
            """,
            height=40,
        )
        st.session_state.login_pulse = False

    st.markdown(
        f"### Hello, **{st.session_state.client_name}** 💜 "
        f"<span style='color:#86198f;font-size:0.95rem;'>(age {st.session_state.client_age})</span>",
        unsafe_allow_html=True,
    )
    st.caption("Glow Studio — book a visit or ask our virtual stylist for ideas.")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Log out", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.client_name = ""
            st.session_state.client_age = None
            st.rerun()

    tab_book, tab_advice = st.tabs(["📅 Book appointment", "💬 Ask for advice"])

    with tab_book:
        st.markdown("##### Schedule your visit")
        svc = st.selectbox(
            "Service",
            [
                "Haircut & blow-dry",
                "Color / highlights",
                "Manicure",
                "Pedicure",
                "Facial",
                "Brows & lashes",
                "Consultation only",
            ],
        )
        d = st.date_input("Preferred date")
        slot = st.selectbox(
            "Time slot",
            [
                "09:00 — 10:00",
                "10:00 — 11:00",
                "11:00 — 12:00",
                "14:00 — 15:00",
                "15:00 — 16:00",
                "16:00 — 17:00",
            ],
        )
        notes = st.text_area("Notes (optional)", placeholder="Allergies, inspiration photos…")
        if st.button("Confirm booking", type="primary"):
            st.session_state.appointments.append(
                {
                    "name": st.session_state.client_name,
                    "age": st.session_state.client_age,
                    "service": svc,
                    "date": str(d),
                    "slot": slot,
                    "notes": (notes or "").strip(),
                }
            )
            st.success("You’re booked! We’ll see you at Glow Studio 💕")
            st.balloons()

        if st.session_state.appointments:
            st.divider()
            st.markdown("##### Your requests this session")
            for i, ap in enumerate(st.session_state.appointments, start=1):
                st.markdown(
                    f"**{i}.** {ap['service']} — {ap['date']} ({ap['slot']})"
                )

    with tab_advice:
        st.markdown("##### Beauty & care tips")
        if not api_key:
            st.info(
                "Add **OPENAI_API_KEY** (OpenAI) or **ANTHROPIC_API_KEY** (Claude) "
                "in Streamlit **Settings → Secrets** to enable AI advice."
            )
        q = st.text_area(
            "What would you like help with?",
            placeholder="e.g. How do I keep color-treated hair shiny between visits?",
            height=100,
        )
        if st.button("Get advice", type="primary", disabled=not api_key):
            if not (q or "").strip():
                st.warning("Type a question first.")
            else:
                with st.spinner("Gathering ideas…"):
                    try:
                        ans = ask_beauty_advisor(q.strip(), provider, api_key)
                        st.markdown(ans)
                    except Exception as e:
                        st.error(f"Could not reach the AI service: {e}")


if __name__ == "__main__":
    run()
