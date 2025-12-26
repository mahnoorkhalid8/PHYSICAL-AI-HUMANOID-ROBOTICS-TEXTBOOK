import os
import asyncio
from typing import Dict, Any, Optional
from groq import AsyncGroq
from pydantic import BaseModel
from ..services.rag_service import RAGService

class PersonalizationService:
    def __init__(self):
        """
        Initialize the personalization service with Groq client and RAG service
        """
        self.groq_client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_name = os.getenv("GROQ_MODEL_NAME", "llama3-70b-8192")  # Default model
        self.rag_service = RAGService()

    async def generate_personalized_content(
        self,
        chapter_content: str,
        chapter_title: Optional[str] = None,
        user_background: Dict[str, str] = None
    ) -> Dict[str, str]:
        """
        Generate personalized content using RAG and AI
        :param chapter_content: The content of the chapter to personalize
        :param chapter_title: Title of the chapter (optional)
        :param user_background: User's background information (software, hardware)
        :return: Dictionary with personalized content and reasoning
        """
        if not user_background:
            user_background = {"software": "beginner", "hardware": "beginner"}

        try:
            # Use RAG service to retrieve actual book content related to the chapter
            # Instead of using just the provided chapter_content, search for relevant content in the book
            rag_query = chapter_title or "textbook content"
            if not rag_query.strip():
                rag_query = chapter_content[:100] if chapter_content else "textbook content"  # Use first 100 chars as query if no title

            # Search for relevant content in the book using RAG
            context_list = self.rag_service.search_embeddings(
                query_text=rag_query,
                top_k=5,
                selected_text=chapter_content,
                search_scope="current_page"  # Focus on content related to the current chapter
            )

            # Combine the retrieved context from the book
            book_content = ""
            for ctx in context_list:
                book_content += f"{ctx.content}\n\n"

            # If no book content was found, fall back to the original chapter content
            if not book_content.strip():
                book_content = chapter_content

            # Create a detailed prompt for the AI model that includes both the book content and user background
            system_prompt = self._create_system_prompt(user_background)
            user_prompt = self._create_user_prompt(book_content, chapter_title, user_background)

            # Call the Groq API for content generation
            chat_completion = await self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                model=self.model_name,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                stream=False,
            )

            # Extract the generated content
            personalized_content = chat_completion.choices[0].message.content

            # Generate reasoning for how the content was personalized
            reasoning = self._generate_reasoning(user_background, chapter_title or "the chapter")

            return {
                "content": personalized_content,
                "reasoning": reasoning
            }

        except Exception as e:
            # In a real implementation, you would have more sophisticated error handling
            print(f"Error in AI generation: {str(e)}")
            # Fallback response
            return {
                "content": f"Based on your background in {user_background.get('software', 'software')} and {user_background.get('hardware', 'hardware')}, this content is tailored for your skill level.",
                "reasoning": f"Content adapted based on your {user_background.get('software', 'software')} and {user_background.get('hardware', 'hardware')} background to provide appropriate complexity."
            }

    def _create_system_prompt(self, user_background: Dict[str, str]) -> str:
        """
        Create system prompt based on user background
        """
        software_level = user_background.get("software", "beginner")
        hardware_level = user_background.get("hardware", "beginner")

        return f"""
        You are an expert educator specializing in humanoid robotics. Your task is to personalize educational content based on the user's background.

        User Background:
        - Software Experience: {software_level}
        - Hardware Experience: {hardware_level}

        When personalizing content:
        1. For beginners: Use simpler explanations, more analogies, and foundational concepts
        2. For intermediate learners: Include practical examples and moderate complexity
        3. For advanced learners: Add technical depth, implementation details, and advanced concepts
        4. For experts: Focus on complex applications, optimization, and cutting-edge research

        Always maintain educational quality and accuracy while adjusting complexity to match the user's background.
        """

    def _create_user_prompt(self, chapter_content: str, chapter_title: Optional[str], user_background: Dict[str, str]) -> str:
        """
        Create user prompt with chapter content and user context
        """
        title_context = f"The chapter title is: '{chapter_title}'" if chapter_title else "The content is from an educational chapter on humanoid robotics."

        return f"""
        {title_context}

        Original content:
        {chapter_content}

        Please generate personalized content that adapts the original material to match the user's background in software ({user_background.get("software", "beginner")}) and hardware ({user_background.get("hardware", "beginner")}).

        The personalized content should maintain the educational value while adjusting complexity, examples, and depth to be most appropriate for the user's experience level.
        """

    def _generate_reasoning(self, user_background: Dict[str, str], chapter_title: str) -> str:
        """
        Generate reasoning for how the content was personalized
        """
        software_level = user_background.get("software", "beginner")
        hardware_level = user_background.get("hardware", "beginner")

        return f"""
        Content adapted for {software_level} software skills and {hardware_level} hardware knowledge.
        Adjusted complexity, examples, and technical depth to match your experience level in {chapter_title}.
        """

    async def validate_background_fields(self, software_background: str, hardware_background: str) -> bool:
        """
        Validate user background fields
        """
        # Check if background fields are valid
        if not software_background or len(software_background) < 2 or len(software_background) > 200:
            return False

        if not hardware_background or len(hardware_background) < 2 or len(hardware_background) > 200:
            return False

        return True