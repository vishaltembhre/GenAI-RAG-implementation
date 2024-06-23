GenAI RAG implementation [Marketing Email Generation]
This project uses Python and Streamlit to create a user-friendly web application that assists with generating marketing content, specifically emails. It leverages large language models (LLMs) to craft email copy based on user input and product descriptions.

Key Features:
Email Marketing Type Selection: Choose the type of marketing content you want to create (e.g., promotional, newsletter, educational).

Product Description Input: Enter details manually or upload a file (text, PDF, or PPT).

Data Upload (Optional): Upload a CSV, Excel, or text file containing relevant data for insights.

User Email Vision: Outline your desired email content and focus areas.

Creativity Level: Adjust the level of creativity for the generated email copy.

Legal Footer Selection: Pick a pre-defined legal footer for your email.

Email Generation: Generate email content based on your specifications.

Legal Check (Optional): Ensure the email complies with legal and regulatory requirements.

Download Options: Download the generated email and any insights graphs (if data is uploaded).

Getting Started:
Clone the repository: Use git clone https://github.com/vishaltembhre/GenAI-RAG-implementation.git to clone the project.

Install dependencies: Navigate to the project directory and run pip install -r requirements.txt to install required libraries.

Configure API Keys: Create a secrets file named .secrets and add your Azure OpenAI API details (CLIENT_SECRET) securely.

Run the application: Execute python main.py to start the Streamlit app.

Libraries
Python

Streamlit

langchain (for LLM integration)

pandas (for data manipulation)

PyPDF2 (for PDF processing)

pptx (for PowerPoint processing)

Azure OpenAI (for LLM access)

matplotlib (for data visualization)

seaborn (for data visualization)
