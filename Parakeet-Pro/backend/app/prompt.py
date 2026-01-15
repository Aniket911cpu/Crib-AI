from typing import Optional
import os

class ParakeetPrompt:
    def __init__(self, resume_text: str = "", job_description: str = ""):
        self.resume_text = resume_text
        self.job_description = job_description
        
        # Base System Prompt
        self.system_prompt = """
You are Parakeet, an expert coding interview candidate. Your goal is to help the user answer interview questions correctly, concisely, and naturally.

### CONTEXT
ROLES:
- You are the candidate (based on the user's resume).
- The input text is the interviewer's question (transcribed in real-time).

RESUME CONTEXT:
{resume_context}

JOB DESCRIPTION:
{job_context}

### INSTRUCTIONS
1. **Be Concise**: specific bullet points or short sentences. No fluff.
2. **Be Conversational**: Sound like a human, not a Wikipedia article.
3. **Speed is Key**: The user is reading this live. Keep it short.
4. **Anti-Hallucination**: If you do not know the answer or if the question requires specific knowledge effectively missing from the context, say "I don't know" or suggest a clarifying question. DO NOT make up facts about the user's experience that are not in the resume.
5. **Code**: If asked for code, provide the most optimal Python/JS solution immediately.

### OUTPUT FORMAT
- Bullet points (2-3 max)
- Or a short code snippet
- Or a direct answer sentence
"""

    def construct_prompt(self, transcript_history: str) -> str:
        """
        Combines the static context with the dynamic transcript history.
        """
        # Format the system prompt with current context
        # (In a real app, you might update resume/JD dynamically)
        formatted_system = self.system_prompt.format(
            resume_context=self.resume_text if self.resume_text else "No resume provided.",
            job_context=self.job_description if self.job_description else "No job description provided."
        )

        # Create the full message chain for the LLM
        # This function returns the string for a "User" message, or the full prompt structure
        # dependent on the LLM API (Groq/OpenAI usually take a list of dicts).
        # Here we return a simple string representation for the 'user' content or the full structure.
        
        return formatted_system 
    
    def get_messages(self, transcript: str):
        """
        Returns the message list for OpenAI/Groq APIs
        """
        system_content = self.system_prompt.format(
            resume_context=self.resume_text if self.resume_text else "[RESUME PLACEHOLDER]",
            job_context=self.job_description if self.job_description else "[JOB DESCRIPTION PLACEHOLDER]"
        )
        
        return [
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"Interviewer just said: \"{transcript}\"\n\nSuggest a concise answer:"}
        ]

# Example Usage
if __name__ == "__main__":
    prompter = ParakeetPrompt(
        resume_text="Senior Python Developer, 5 years exp at Google.",
        job_description="Looking for an expert in FastAPI and React."
    )
    msgs = prompter.get_messages("So tell me about a time you optimized a slow API endpoint.")
    print(msgs)
