import streamlit as st
import pandas as pd

from chatbot import (
    english_to_sql,
    clean_sql,
    validate_sql,
    run_sql,
    combine_sql_and_pdf_answer
)

from rag import ask_pdf, get_pdf_context


# STREAMLIT Settings

st.set_page_config(page_title="AI Financial Chatbot", layout="centered")

st.title("📊 AI Financial Chatbot (SQL + RAG + Charts)")
st.write(
    "Ask business questions. The system can answer using:\n"
    "- SQL data\n"
    "- PDF documents (RAG)\n"
    "- Or both, with charts and explanations"
)


# User input

question = st.text_input(
    "Ask a question",
    placeholder="e.g. Why did France have the highest profit?"
)

show_sql = st.checkbox("Show generated SQL")

mode = st.radio(
    "Choose answer mode:",
    ["SQL Data", "PDF Documents", "SQL + Documents (Combined)"]
)


# HELPER: SAFE CHART LOGIC

def show_chart(sql_result, sql_query):
    
    if not isinstance(sql_result, list) or len(sql_result) == 0:
        return

    df = pd.DataFrame(sql_result)

    
    if df.shape[1] != 2:
        st.info("ℹ️ Chart not generated (query result has more than 2 columns).")
        return


    df.columns = ["Category", "Value"]

   
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna()

    if df.empty:
        return

    st.subheader("📊 Visualization")

    
    if "year" in sql_query.lower() or "month" in sql_query.lower():
        st.line_chart(df.set_index("Category"))
    else:
        st.bar_chart(df.set_index("Category"))


# Process Question

if question:
    with st.spinner("Thinking..."):

        # MODE 1: SQL ONLY 
        if mode == "SQL Data":
            sql_query = clean_sql(english_to_sql(question))

            if not validate_sql(sql_query):
                st.error("❌ Unsafe SQL detected.")
            else:
                result = run_sql(sql_query)

                st.subheader("Result")
                st.table(result)

                show_chart(result, sql_query)

                if show_sql:
                    st.subheader("Generated SQL")
                    st.code(sql_query, language="sql")

        # MODE 2: PDF ONLY 
        elif mode == "PDF Documents":
            st.subheader("Answer from Documents")
            st.write(ask_pdf(question))

        #  MODE 3: SQL + PDF COMBINED 
        else:
            # SQL
            sql_query = clean_sql(english_to_sql(question))
            sql_result = None

            if validate_sql(sql_query):
                sql_result = run_sql(sql_query)
            else:
                st.error("❌ Unsafe SQL detected.")

            #  PDF context
            pdf_context = get_pdf_context(question)

            #  Combined answer
            final_answer = combine_sql_and_pdf_answer(
                question,
                sql_result,
                pdf_context
            )

            st.subheader("Final Answer")
            st.write(final_answer)

            # Show table + chart if possible
            if isinstance(sql_result, list):
                st.subheader("SQL Result")
                st.table(sql_result)
                show_chart(sql_result, sql_query)

            if show_sql:
                st.subheader("Generated SQL")
                st.code(sql_query, language="sql")


# FOOTER

st.markdown(
    "---\n"
    "🧠 **System:** SQL Analytics + RAG + Charts\n\n"
    "📊 **Charts:** Auto-generated when result shape allows\n\n"
    "💻 **Stack:** MySQL • Python • FAISS • HuggingFace • Ollama • Streamlit\n\n"
    "🚀 **100% local & free**"
)
