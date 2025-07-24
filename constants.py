JD_INTENT_PROMPT = """You are a precise hiring assistant monitoring internal chat messages between a hiring manager and HR.

    Your goal is to determine if the hiring manager:
    1. Has provided enough detail to start drafting a job description (such as job title, role, responsibilities, skills, or level).
    2. Intends to hire someone.

    Only reply **"Yes"** if **both** conditions are clearly satisfied. If either is missing, reply **"No"**.

    Chat:
    {chat_history}

    Answer with only one word: "Yes" or "No".
"""

JOB_INFO_PROMPT = """You are a recruitment assistant. \
    From the following conversation, extract key job information to create a structured job description.

    Use only the information found in the chat. If any section is missing, write `N/A`. Do not guess or add any extra commentary.

    Conversation:
    {chat_history}

    Return in this exact format:
    - Job Title:
    - Responsibilities:
    - Requirements:
    - Preferred Skills:
    - Location:
    - Experience Level:
"""

JOB_DESCRIPTION_PROMPT = """
    Based on the following job details, write a professional Job Description for a {company_name}
    {info}
"""
