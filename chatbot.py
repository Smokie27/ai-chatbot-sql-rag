import mysql.connector
from langchain_ollama import OllamaLLM


# Database connection

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="XXXXXX",  
    database="finance_project_db"
)

cursor = db.cursor()


# Loading OLLAMA

llm = OllamaLLM(model="llama3")


# English to SQL

def english_to_sql(question):
    prompt = f"""
You are a MySQL expert.

STRICT RULES:
- Output ONLY a valid MySQL SELECT query.
- Do NOT include explanations or markdown.
- Do NOT include ```sql or ``` blocks.
- Do NOT include text before or after the query.
- NEVER use DELETE, UPDATE, INSERT, DROP, ALTER.
- Use ONLY the table sales_data.

AGGREGATION RULES (VERY IMPORTANT):
- If profit or sales is used:
  1. ALWAYS use SUM(profit) or SUM(sales)
  2. ALWAYS GROUP BY non-aggregated columns
  3. ALWAYS ORDER BY the aggregated alias (e.g. total_profit)

Table schema:
sales_data(
segment,
country,
product,
discount_band,
units_sold,
manufacturing_price,
sale_price,
gross_sales,
discounts,
sales,
cogs,
profit,
order_date,
month_number,
month_name,
year
)

Question:
{question}

SQL:
"""
    return llm.invoke(prompt).strip()


# Output

def clean_sql(sql):
    sql = sql.replace("```sql", "").replace("```", "")
    return sql.strip()


# SQL Safety validation

def validate_sql(sql):
    forbidden = ["delete", "update", "insert", "drop", "alter"]
    return not any(word in sql.lower() for word in forbidden)


# EXxecute SQL query

def run_sql(sql):
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        return f"SQL Error: {e}"


# SQL + PDF context (RAG)

def combine_sql_and_pdf_answer(question, sql_result, pdf_context):
    prompt = f"""
You are a financial analyst assistant.

You are given:
1. A numerical result from SQL
2. Context from company documents

Your task:
- Combine both into ONE clear professional answer
- Mention the numerical result explicitly
- Use document context for explanation
- Do NOT invent facts

SQL Result:
{sql_result}

Document Context:
{pdf_context}

Question:
{question}

Final Answer:
"""
    return llm.invoke(prompt)


# Main execution

if __name__ == "__main__":
    question = "Which country has the lowest total profit?"

    sql_query = clean_sql(english_to_sql(question))

    print("Generated SQL:")
    print(sql_query)

    print("\nSQL Result:")
    if validate_sql(sql_query):
        sql_result = run_sql(sql_query)
        print(sql_result)
    else:
        print("Blocked unsafe SQL query")

    # Example PDF context (replace with real RAG output)
    pdf_context = "The company reported weaker performance in this region due to high logistics costs."

    final_answer = combine_sql_and_pdf_answer(
        question,
        sql_result,
        pdf_context
    )

    print("\nFinal AI Answer:")
    print(final_answer)
