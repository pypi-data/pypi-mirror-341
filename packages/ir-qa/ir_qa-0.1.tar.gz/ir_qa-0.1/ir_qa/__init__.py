#initiator

# Question-Answer System 
from transformers import pipeline
import warnings
import tensorflow as tf

# Suppress warnings
tf.get_logger().setLevel("ERROR")
warnings.filterwarnings("ignore")

# Suppress Hugging Face transformers logging
from transformers.utils import logging as hf_logging
hf_logging.set_verbosity_error()

# Load QA model
qa_pipeline = pipeline("question-answering")

# Provided corpus (context)
context = """
India has the second-largest population in the world. It is surrounded by oceans from three sides 
which are Bay Of Bengal in the east, the Arabian Sea in the west and Indian Ocean in the south.
Tiger is the national animal of India.
Peacock is the national bird of India.
Mango is the national fruit of India.
"""

# Query the system
question = "Which is the national fruit of India?"

# Get answer
result = qa_pipeline(question=question, context=context)

# Display result
print(f"Question: {question}")
print(f"Answer: {result['answer']}")

