import os
import requests
import streamlit as st

API=os.getenv("API_BASE_URL","http://localhost:8000")

st.set_page_config(page_title="Enterprise AI Mega Lab",page_icon="🧠",layout="wide")
st.title("Enterprise AI Mega Lab")
st.caption("One fictional enterprise. Multiple specialist agents. One Super Agent.")

with st.sidebar:
    st.header("Workspace")
    user_role=st.selectbox("Role",["employee","seller","support","manager","executive"])
    st.markdown("**Try a question**")
    examples=[
        "Find the best sales opportunities and explain why.",
        "Who should I reach out to at RedStone Energy regarding network modernization?",
        "Prepare me for my meeting with Apex Manufacturing.",
        "Which support tickets need immediate escalation?",
        "What are the biggest finance variances this month?",
        "Which inventory items are at risk of stockout?",
        "Give me an executive brief across the business.",
        "What is our travel reimbursement policy?",
    ]
    selected=st.selectbox("Examples",[""]+examples)

if "messages" not in st.session_state:
    st.session_state.messages=[]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("details"):
            with st.expander("Agent details"):
                st.json(msg["details"])

prompt=st.chat_input("Ask the Enterprise Super Agent...")
if selected and st.button("Use selected example"):
    prompt=selected

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)
    try:
        r=requests.post(f"{API}/agents/ask",json={"message":prompt,"user_role":user_role},timeout=60)
        r.raise_for_status(); data=r.json()
        content=f"**{data['answer']}**"
        if data.get("recommended_actions"):
            content += "\n\n**Recommended actions**\n" + "\n".join(f"- {a}" for a in data["recommended_actions"])
        if data.get("sources"):
            content += "\n\n**Sources**\n" + "\n".join(f"- `{s['source']}`" for s in data["sources"])
        details={"agent":data.get("agent"),"intent":data.get("intent"),"trace":data.get("trace"),"data":data.get("data")}
    except Exception as e:
        content=f"Backend unavailable: {e}. Start it with `uvicorn backend.app.main:app --reload`."
        details=None
    st.session_state.messages.append({"role":"assistant","content":content,"details":details})
    with st.chat_message("assistant"):
        st.markdown(content)
        if details:
            with st.expander("Agent details"): st.json(details)

st.divider()
col1,col2,col3=st.columns(3)
with col1:
    st.subheader("Architecture")
    st.write("Super Agent → specialist agents → governed enterprise tools.")
with col2:
    st.subheader("Local-first")
    st.write("Deterministic workflows and TF-IDF retrieval work without a hosted LLM.")
with col3:
    st.subheader("Extendable")
    st.write("Swap mock enterprise tools for Salesforce, ServiceNow, Workday, SAP, MCP, or OpenAPI connectors.")
