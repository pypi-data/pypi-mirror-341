from textwrap import dedent

from jarvismode.components.data import FileComponent
from jarvismode.components.embeddings import OpenAIEmbeddingsComponent
from jarvismode.components.inputs import ChatInput
from jarvismode.components.models import OpenAIModelComponent
from jarvismode.components.outputs import ChatOutput
from jarvismode.components.processing import ParseDataComponent
from jarvismode.components.processing.split_text import SplitTextComponent
from jarvismode.components.prompts import PromptComponent
from jarvismode.components.vectorstores import AstraDBVectorStoreComponent
from jarvismode.graph import Graph


def ingestion_graph():
    # Ingestion Graph
    file_component = FileComponent()
    text_splitter = SplitTextComponent()
    text_splitter.set(data_inputs=file_component.load_files)
    openai_embeddings = OpenAIEmbeddingsComponent()
    vector_store = AstraDBVectorStoreComponent()
    vector_store.set(
        embedding_model=openai_embeddings.build_embeddings,
        ingest_data=text_splitter.split_text,
    )

    return Graph(file_component, vector_store)


def rag_graph():
    # RAG Graph
    openai_embeddings = OpenAIEmbeddingsComponent()
    chat_input = ChatInput()
    rag_vector_store = AstraDBVectorStoreComponent()
    rag_vector_store.set(
        search_query=chat_input.message_response,
        embedding_model=openai_embeddings.build_embeddings,
    )

    parse_data = ParseDataComponent()
    parse_data.set(data=rag_vector_store.search_documents)
    prompt_component = PromptComponent()
    prompt_component.set(
        template=dedent("""Given the following context, answer the question.
                         Context:{context}

                         Question: {question}
                         Answer:"""),
        context=parse_data.parse_data,
        question=chat_input.message_response,
    )

    openai_component = OpenAIModelComponent()
    openai_component.set(input_value=prompt_component.build_prompt)

    chat_output = ChatOutput()
    chat_output.set(input_value=openai_component.text_response)

    return Graph(start=chat_input, end=chat_output)


def vector_store_rag_graph():
    return ingestion_graph() + rag_graph()
