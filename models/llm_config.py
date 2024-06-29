from transformers import (AutoTokenizer, AutoModelForSeq2SeqLM, AutoModel, BertModel, BertTokenizer,
                          BertForSequenceClassification, BertForQuestionAnswering)
from llama_cpp import Llama
from langchain_community.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain import PromptTemplate
import torch

import io


def google_flan(prompt):
    # Pass the directory path where the models is stored on your system
    model_name = "google/flan-t5-large"

    # Initialize a tokenizer for the specified models
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained('google/flan-t5-large')
    # prompt = 'A step by step recipe to make bolognese pasta:'

    tokenizer = AutoTokenizer.from_pretrained('google/flan-t5-large')
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs)
    response = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    print(f'Response:\t{response}')
    return response


def google_bert():
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    classifier = BertForSequenceClassification.from_pretrained("bert-base-uncased")
    qa = BertForQuestionAnswering.from_pretrained("bert-base-uncased")

    text = "This is a sample text."
    tokens = tokenizer(text)

    encoded_tokens = model.encode(tokens)
    predictions = classifier(encoded_tokens)
    predicted_class = predictions.logits.argmax().item()

    question = "What is the capital of France?"
    answer = qa(encoded_tokens, question)

    print(f'answer:\t{answer}')


def llama1():
    # Put the location of to the GGUF model that you've download from HuggingFace here
    model_path = "./llama-2-7b-chat.Q2_K.gguf"
    llm = Llama(model_path=model_path)

    # Prompt creation
    system_message = "You are a helpful assistant"
    user_message = "Q: Name the planets in the solar system? A: "

    prompt = f"""<s>[INST] <<SYS>>
    {system_message}
    <</SYS>>
    {user_message} [/INST]"""

    # Run the model
    output = llm(
        prompt,  # Prompt
        # max_tokens=32,  # Generate up to 32 tokens
        max_tokens=999,  # Generate up to 32 tokens
        stop=["Q:", "\n"],  # Stop generating just before the model would generate a new question
        echo=True  # Echo the prompt back in the output
    )  # Generate a completion, can also call create_completion

    # print(output)
    print(output["choices"][0]["text"])


def llama2(input_str):
    template = """
    <s>[INST] <<SYS>>
    Act as a personal assistant.
    <</SYS>>

    {text} [/INST]
    """
    # text = str(input_str)
    prompt = PromptTemplate(
        input_variables=["text"],
        template=template,
    )
    # text = "Explain what is the solar system"
    # print(prompt.format(text=text))

    # Callbacks support token-wise streaming
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    model_path = "llama-2-7b-chat.Q2_K.gguf"
    llm = LlamaCpp(
        model_path=model_path,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,  # Verbose is required to pass to the callback manager
    )

    output = llm.invoke(prompt.format(text=input_str))
    # print(output)
    return output


def llama2_response_store(response_str):
    response_string_io = io.StringIO()
    response_string_io.write(response_str)

    response_string_io_val = response_string_io.getvalue()
    str_io_var = io.StringIO(response_string_io_val)
    print(f'str_io_var:\t::{str_io_var.getvalue()}')

    return str_io_var


# Act as an Astronomer engineer who is teaching high school students.

def check_cuda():
    is_cuda = torch.cuda.is_available()
    if is_cuda:
        print("This computer uses CUDA")
    else:
        print("This computer uses CPU")


if __name__ == '__main__':
    # check_cuda()
    # google_flan()
    # google_bert()
    # llama1()
    prompt = 'can you explain me about chat gpt'
    response = llama2(prompt)
    print(f'Type of Response\t:::{type(response)}')
    io_str_val = llama2_response_store(response)

