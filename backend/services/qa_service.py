from typing import Dict, List, Any
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from base64 import b64decode
from services.dependencies import retriever, llm
from langchain_core.output_parsers import StrOutputParser


class QAService:

    def parse_answer(answers):
        """Split base64-encoded images and texts"""
        b64 = []
        text = []
        for answer in answers:
            try:
                b64decode(answer)
                b64.append(answer)
            except Exception as e:
                text.append(answer)
        return {"images": b64, "texts": text}

    def build_prompt(kwargs):
        answers_by_type = kwargs["context"]
        user_question = kwargs["question"]

        context_text = ""
        if len(answers_by_type["texts"]) > 0:
            for text_element in answers_by_type["texts"]:
                context_text += text_element
        # construct prompt with context (including images)
        prompt_template = f"""
        Answer the question based only on the following context, which can include text, tables, and the below image.
        Context: {context_text}
        Question: {user_question}
        """

        prompt_content = [{"type": "text", "text": prompt_template}]

        if len(answers_by_type["images"]) > 0:
            for image in answers_by_type["images"]:
                try:
                    # Try decoding to make sure it is valid base64
                    decoded_image = b64decode(image, validate=True)
                    if decoded_image:
                        prompt_content.append(
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                            }
                        )
                except Exception as e:
                    print(f"⚠️ Skipping invalid image: {e}")

        return ChatPromptTemplate.from_messages(
            [
                HumanMessage(content=prompt_content),
            ]
        )

    async def answer_question(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using the vector store and Azure OpenAI.

        Args:
            question: The question to answer

        Returns:
            Dictionary containing the answer and relevant context
        """

        # Response without sources
        chain = (
            {
                "context": retriever | RunnableLambda(self.parse_answer),
                "question": RunnablePassthrough(),
            }
            | RunnableLambda(self.build_prompt)
            | llm
            | StrOutputParser()
        )

        # Response with sources
        chain_with_sources = {
            "context": retriever | RunnableLambda(self.parse_answer),
            "question": RunnablePassthrough(),
        } | RunnablePassthrough().assign(
            response=(
                RunnableLambda(self.build_prompt)
                | llm
                | StrOutputParser()
            )
        )

        response = chain.invoke(question)

        return {
            "answer": response['response'],
            "context": response['context']
        }
