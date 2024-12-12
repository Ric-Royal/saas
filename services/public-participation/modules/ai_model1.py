import os
import logging
import ollama

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaResponder:
    def __init__(self, model_name=None):
        """
        Initialize the OllamaResponder using the Ollama Python library.
        """
        # Load the model name from environment variable or fall back to default
        self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
        logger.info(f"OllamaResponder initialized with model: {self.model_name}")

    def generate_response(self, prompt, max_length=150):
        """
        Generate a response using the Ollama Python library.
        """
        try:
            # Sanitize the prompt
            prompt = prompt.strip()
            if not prompt:
                logger.warning("Empty prompt received.")
                return "Please provide a valid prompt."

            logger.info(f"Generating response for prompt: {prompt[:30]}...")
            # Generate response
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={'max_length': max_length}
            )

            logger.debug(f"Response from Ollama: {response}")

            if 'response' in response:
                response_text = response['response'].strip()
                if not response_text:
                    logger.warning("Received an empty response from the model.")
                    return "Sorry, I couldn't generate a response."

                logger.info("Response generated successfully.")
                return response_text
            else:
                logger.error("No 'response' key in the response from Ollama.")
                return "Sorry, I couldn't generate a response."

        except ollama.ModelNotFoundError:
            logger.error(f"Model '{self.model_name}' not found in Ollama.")
            return f"Model '{self.model_name}' is not available."
        except Exception as e:
            logger.error(f"An error occurred during response generation: {e}")
            return "Sorry, I encountered an error while generating the response."

if __name__ == "__main__":
    # Example usage
    model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
    responder = OllamaResponder(model_name)

    # Sample prompt for testing
    prompt = "Explain the key points of the Agriculture Bill."
    response = responder.generate_response(prompt)

    print(response)


# # # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # # import logging
# # # # # # # # # # # # # # # # # # # # from transformers import AutoTokenizer, AutoModelForCausalLM
# # # # # # # # # # # # # # # # # # # # import torch
# # # # # # # # # # # # # # # # # # # # from transformers import logging as hf_logging

# # # # # # # # # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # # # # # # # # logging.basicConfig(level=logging.INFO)
# # # # # # # # # # # # # # # # # # # # logger = logging.getLogger(__name__)
# # # # # # # # # # # # # # # # # # # # hf_logging.set_verbosity_error()  # Suppress extensive model warnings

# # # # # # # # # # # # # # # # # # # # class LLamaResponder:
# # # # # # # # # # # # # # # # # # # #     def __init__(self, model_name=None):
# # # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # # #         Initialize the Llama model.
# # # # # # # # # # # # # # # # # # # #         Replace 'model_name' with the actual Llama model path or identifier, if provided via environment variable.
# # # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # # #         # Load the model path from environment variable or fall back to passed argument
# # # # # # # # # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("llama3.2", "gpt2")
        
# # # # # # # # # # # # # # # # # # # #         # Initialize tokenizer and model with error handling
# # # # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # # # #             logger.info(f"Loading model and tokenizer: {self.model_name}")
# # # # # # # # # # # # # # # # # # # #             self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
# # # # # # # # # # # # # # # # # # # #             self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
            
# # # # # # # # # # # # # # # # # # # #             # Move model to GPU if available
# # # # # # # # # # # # # # # # # # # #             if torch.cuda.is_available():
# # # # # # # # # # # # # # # # # # # #                 self.device = 'cuda'
# # # # # # # # # # # # # # # # # # # #                 self.model = self.model.to(self.device)
# # # # # # # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # # # # # # #                 self.device = 'cpu'
# # # # # # # # # # # # # # # # # # # #                 logger.warning("CUDA not available. Running on CPU.")
                
# # # # # # # # # # # # # # # # # # # #             self.model.eval()
# # # # # # # # # # # # # # # # # # # #             logger.info(f"Model {self.model_name} loaded successfully.")
# # # # # # # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # # # # # # #             logger.error(f"Failed to load model {self.model_name}: {e}")
# # # # # # # # # # # # # # # # # # # #             raise
        
# # # # # # # # # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150, top_p=0.95, top_k=60):
# # # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # # #         Generate a response based on the input prompt.
# # # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")  # Log first 30 chars of the prompt
# # # # # # # # # # # # # # # # # # # #             # Tokenize input
# # # # # # # # # # # # # # # # # # # #             inputs = self.tokenizer(prompt, return_tensors="pt")
# # # # # # # # # # # # # # # # # # # #             if torch.cuda.is_available():
# # # # # # # # # # # # # # # # # # # #                 inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
# # # # # # # # # # # # # # # # # # # #             # Generate response with error handling
# # # # # # # # # # # # # # # # # # # #             with torch.no_grad():
# # # # # # # # # # # # # # # # # # # #                 outputs = self.model.generate(
# # # # # # # # # # # # # # # # # # # #                     **inputs,
# # # # # # # # # # # # # # # # # # # #                     max_length=max_length,
# # # # # # # # # # # # # # # # # # # #                     do_sample=True,
# # # # # # # # # # # # # # # # # # # #                     top_p=top_p,
# # # # # # # # # # # # # # # # # # # #                     top_k=top_k
# # # # # # # # # # # # # # # # # # # #                 )
            
# # # # # # # # # # # # # # # # # # # #             response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
# # # # # # # # # # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # # # # # # # # # #             return response
# # # # # # # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # # # # # # #             logger.error(f"Failed to generate response: {e}")
# # # # # # # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."
    
# # # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # # # # # # # # #     model_name = os.environ.get("llama3.2", "gpt2")  # Replace with Llama model path if available
# # # # # # # # # # # # # # # # # # # #     responder = LLamaResponder(model_name)
    
# # # # # # # # # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # # # # # # # # #     response = responder.generate_response(prompt)
    
# # # # # # # # # # # # # # # # # # # #     print(response)


# # # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # # import subprocess
# # # # # # # # # # # # # # # # # # # import logging

# # # # # # # # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # # # # # # # logging.basicConfig(level=logging.INFO)
# # # # # # # # # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # # # # # # # # #     def __init__(self, model_name=None):
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         Initialize the OllamaResponder.
# # # # # # # # # # # # # # # # # # #         Uses Ollama CLI to generate responses.
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "ollama")

# # # # # # # # # # # # # # # # # # #         # Check if Ollama is available
# # # # # # # # # # # # # # # # # # #         if not self.is_ollama_available():
# # # # # # # # # # # # # # # # # # #             logger.error("Ollama is not available in the system PATH.")
# # # # # # # # # # # # # # # # # # #             raise EnvironmentError("Ollama is not available in the system PATH.")

# # # # # # # # # # # # # # # # # # #         # Optionally, you can check if the model is available
# # # # # # # # # # # # # # # # # # #         if not self.is_model_available(self.model_name):
# # # # # # # # # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # # # # # # # # #             raise EnvironmentError(f"Model '{self.model_name}' is not available in Ollama.")

# # # # # # # # # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name}")

# # # # # # # # # # # # # # # # # # #     def is_ollama_available(self):
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         Check if Ollama CLI is available in the system PATH.
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # # #             subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# # # # # # # # # # # # # # # # # # #             return True
# # # # # # # # # # # # # # # # # # #         except (subprocess.CalledProcessError, FileNotFoundError):
# # # # # # # # # # # # # # # # # # #             return False

# # # # # # # # # # # # # # # # # # #     def is_model_available(self, model_name):
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         Check if the specified model is available in Ollama.
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # # #             result = subprocess.run(
# # # # # # # # # # # # # # # # # # #                 ["ollama", "list"],
# # # # # # # # # # # # # # # # # # #                 check=True,
# # # # # # # # # # # # # # # # # # #                 stdout=subprocess.PIPE,
# # # # # # # # # # # # # # # # # # #                 stderr=subprocess.PIPE,
# # # # # # # # # # # # # # # # # # #                 text=True
# # # # # # # # # # # # # # # # # # #             )
# # # # # # # # # # # # # # # # # # #             installed_models = [line.strip() for line in result.stdout.strip().splitlines()]
# # # # # # # # # # # # # # # # # # #             return model_name in installed_models
# # # # # # # # # # # # # # # # # # #         except subprocess.CalledProcessError as e:
# # # # # # # # # # # # # # # # # # #             logger.error(f"Error checking model availability: {e}")
# # # # # # # # # # # # # # # # # # #             return False

# # # # # # # # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         Generate a response using Ollama CLI.
# # # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # # # # # # # # # #             # Build the command to pass to Ollama
# # # # # # # # # # # # # # # # # # #             command = [
# # # # # # # # # # # # # # # # # # #                 "ollama", "generate",
# # # # # # # # # # # # # # # # # # #                 "--model", self.model_name,
# # # # # # # # # # # # # # # # # # #                 "--max-length", str(max_length)
# # # # # # # # # # # # # # # # # # #             ]

# # # # # # # # # # # # # # # # # # #             # Run the command and capture output
# # # # # # # # # # # # # # # # # # #             process = subprocess.run(
# # # # # # # # # # # # # # # # # # #                 command,
# # # # # # # # # # # # # # # # # # #                 input=prompt,
# # # # # # # # # # # # # # # # # # #                 text=True,
# # # # # # # # # # # # # # # # # # #                 stdout=subprocess.PIPE,
# # # # # # # # # # # # # # # # # # #                 stderr=subprocess.PIPE,
# # # # # # # # # # # # # # # # # # #                 check=True
# # # # # # # # # # # # # # # # # # #             )

# # # # # # # # # # # # # # # # # # #             response = process.stdout.strip()
# # # # # # # # # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # # # # # # # # #             return response

# # # # # # # # # # # # # # # # # # #         except subprocess.CalledProcessError as e:
# # # # # # # # # # # # # # # # # # #             logger.error(f"Ollama command failed: {e.stderr}")
# # # # # # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."
# # # # # # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # # # # # #             logger.error(f"An unexpected error occurred: {e}")
# # # # # # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME")  # Or specify a default model name
# # # # # # # # # # # # # # # # # # #     responder = OllamaResponder(model_name)

# # # # # # # # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # # # # # # # # #     print(response)


# # # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # # import subprocess
# # # # # # # # # # # # # # # # # # import logging
# # # # # # # # # # # # # # # # # # import re

# # # # # # # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # # # # # # logging.basicConfig(level=logging.INFO)
# # # # # # # # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # # # # # # # #     def __init__(self, model_name=None):
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         Initialize the OllamaResponder.
# # # # # # # # # # # # # # # # # #         Uses Ollama CLI to generate responses.
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")

# # # # # # # # # # # # # # # # # #         # Check if Ollama is available
# # # # # # # # # # # # # # # # # #         if not self.is_ollama_available():
# # # # # # # # # # # # # # # # # #             logger.error("Ollama is not available in the system PATH.")
# # # # # # # # # # # # # # # # # #             raise EnvironmentError("Ollama is not available in the system PATH.")

# # # # # # # # # # # # # # # # # #         # Check if the model is available
# # # # # # # # # # # # # # # # # #         if not self.is_model_available(self.model_name):
# # # # # # # # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # # # # # # # #             raise EnvironmentError(f"Model '{self.model_name}' is not available in Ollama.")

# # # # # # # # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name}")

# # # # # # # # # # # # # # # # # #     def is_ollama_available(self):
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         Check if Ollama CLI is available in the system PATH.
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # #             subprocess.run(
# # # # # # # # # # # # # # # # # #                 ["ollama", "--version"],
# # # # # # # # # # # # # # # # # #                 check=True,
# # # # # # # # # # # # # # # # # #                 stdout=subprocess.PIPE,
# # # # # # # # # # # # # # # # # #                 stderr=subprocess.PIPE
# # # # # # # # # # # # # # # # # #             )
# # # # # # # # # # # # # # # # # #             return True
# # # # # # # # # # # # # # # # # #         except (subprocess.CalledProcessError, FileNotFoundError):
# # # # # # # # # # # # # # # # # #             return False

# # # # # # # # # # # # # # # # # #     def is_model_available(self, model_name):
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         Check if the specified model is available in Ollama.
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # #             result = subprocess.run(
# # # # # # # # # # # # # # # # # #                 ["ollama", "list"],
# # # # # # # # # # # # # # # # # #                 check=True,
# # # # # # # # # # # # # # # # # #                 stdout=subprocess.PIPE,
# # # # # # # # # # # # # # # # # #                 stderr=subprocess.PIPE,
# # # # # # # # # # # # # # # # # #                 text=True
# # # # # # # # # # # # # # # # # #             )
# # # # # # # # # # # # # # # # # #             lines = result.stdout.strip().splitlines()
# # # # # # # # # # # # # # # # # #             if len(lines) > 1:
# # # # # # # # # # # # # # # # # #                 # Skip the header line
# # # # # # # # # # # # # # # # # #                 model_lines = lines[1:]
# # # # # # # # # # # # # # # # # #                 installed_models = []
# # # # # # # # # # # # # # # # # #                 for line in model_lines:
# # # # # # # # # # # # # # # # # #                     # Use regex to split on two or more spaces
# # # # # # # # # # # # # # # # # #                     columns = re.split(r'\s{2,}', line.strip())
# # # # # # # # # # # # # # # # # #                     if columns:
# # # # # # # # # # # # # # # # # #                         name = columns[0]
# # # # # # # # # # # # # # # # # #                         installed_models.append(name)
# # # # # # # # # # # # # # # # # #                 logger.debug(f"Installed models: {installed_models}")
# # # # # # # # # # # # # # # # # #                 return model_name in installed_models
# # # # # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # # # # #                 logger.error("No models found in Ollama.")
# # # # # # # # # # # # # # # # # #                 return False
# # # # # # # # # # # # # # # # # #         except subprocess.CalledProcessError as e:
# # # # # # # # # # # # # # # # # #             logger.error(f"Error checking model availability: {e}")
# # # # # # # # # # # # # # # # # #             return False

# # # # # # # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         Generate a response using Ollama CLI.
# # # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # # #             # Sanitize the prompt to prevent command injection
# # # # # # # # # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")

# # # # # # # # # # # # # # # # # #             # Build the command to pass to Ollama
# # # # # # # # # # # # # # # # # #             command = [
# # # # # # # # # # # # # # # # # #                 "ollama", "generate",
# # # # # # # # # # # # # # # # # #                 "--model", self.model_name,
# # # # # # # # # # # # # # # # # #                 "--max-length", str(max_length)
# # # # # # # # # # # # # # # # # #             ]

# # # # # # # # # # # # # # # # # #             # Run the command and capture output
# # # # # # # # # # # # # # # # # #             process = subprocess.run(
# # # # # # # # # # # # # # # # # #                 command,
# # # # # # # # # # # # # # # # # #                 input=prompt,
# # # # # # # # # # # # # # # # # #                 text=True,
# # # # # # # # # # # # # # # # # #                 stdout=subprocess.PIPE,
# # # # # # # # # # # # # # # # # #                 stderr=subprocess.PIPE,
# # # # # # # # # # # # # # # # # #                 check=True
# # # # # # # # # # # # # # # # # #             )

# # # # # # # # # # # # # # # # # #             response = process.stdout.strip()
# # # # # # # # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # # # # # # # #             return response

# # # # # # # # # # # # # # # # # #         except subprocess.CalledProcessError as e:
# # # # # # # # # # # # # # # # # #             logger.error(f"Ollama command failed: {e.stderr}")
# # # # # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."
# # # # # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # # # # #             logger.error(f"An unexpected error occurred: {e}")
# # # # # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # # # # # #     responder = OllamaResponder(model_name)

# # # # # # # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # # # # # # # #     print(response)


# # # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # # import logging
# # # # # # # # # # # # # # # # # import ollama

# # # # # # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # # # # # logging.basicConfig(level=logging.INFO)
# # # # # # # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # # # # # # #     def __init__(self, model_name=None):
# # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name}")

# # # # # # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # # # # # # # #             if not prompt:
# # # # # # # # # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # # # # # # # #             # Generate response
# # # # # # # # # # # # # # # # #             response_text = ''
# # # # # # # # # # # # # # # # #             for response in ollama.generate(
# # # # # # # # # # # # # # # # #                 model=self.model_name,
# # # # # # # # # # # # # # # # #                 prompt=prompt,
# # # # # # # # # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # # # # # # # # #             ):
# # # # # # # # # # # # # # # # #                 if 'response' in response:
# # # # # # # # # # # # # # # # #                     response_text += response['response']
# # # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # # #                     logger.error("No 'response' key in the response from Ollama.")
# # # # # # # # # # # # # # # # #                     return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # # # # #             response_text = response_text.strip()
# # # # # # # # # # # # # # # # #             if not response_text:
# # # # # # # # # # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # # # # # # #             return response_text

# # # # # # # # # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # # # # #     responder = OllamaResponder(model_name)

# # # # # # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # # # # # # #     print(response)

# # # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # # import logging
# # # # # # # # # # # # # # # # import ollama

# # # # # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # # # # logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to see detailed logs
# # # # # # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # # # # # #     def __init__(self, model_name=None):
# # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name}")

# # # # # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # # # # # # #             if not prompt:
# # # # # # # # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # # # # # # #             # Generate response
# # # # # # # # # # # # # # # #             response_text = ''
# # # # # # # # # # # # # # # #             for chunk in ollama.generate(
# # # # # # # # # # # # # # # #                 model=self.model_name,
# # # # # # # # # # # # # # # #                 prompt=prompt,
# # # # # # # # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # # # # # # # #             ):
# # # # # # # # # # # # # # # #                 logger.debug(f"Response chunk: {chunk}")
# # # # # # # # # # # # # # # #                 if 'data' in chunk:
# # # # # # # # # # # # # # # #                     response_text += chunk['data']
# # # # # # # # # # # # # # # #                 elif 'error' in chunk:
# # # # # # # # # # # # # # # #                     logger.error(f"Error from Ollama: {chunk['error']}")
# # # # # # # # # # # # # # # #                     return "Sorry, I encountered an error while generating the response."
# # # # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # # # #                     logger.error(f"Unexpected response format: {chunk}")
# # # # # # # # # # # # # # # #                     return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # # # #             response_text = response_text.strip()
# # # # # # # # # # # # # # # #             if not response_text:
# # # # # # # # # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # # # # # #             return response_text

# # # # # # # # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # # # #     responder = OllamaResponder(model_name)

# # # # # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # # # # # #     print(response)

# # # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # # import logging
# # # # # # # # # # # # # # # import ollama

# # # # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # # # logging.basicConfig(level=logging.INFO)
# # # # # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # # # # #     def __init__(self, model_name=None):
# # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name}")

# # # # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # # # # # # #         """
# # # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # # # # # #             if not prompt:
# # # # # # # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # # # # # #             # Generate response
# # # # # # # # # # # # # # #             response = ollama.generate(
# # # # # # # # # # # # # # #                 model=self.model_name,
# # # # # # # # # # # # # # #                 prompt=prompt,
# # # # # # # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # # # # # # #             )

# # # # # # # # # # # # # # #             logger.debug(f"Response from Ollama: {response}")

# # # # # # # # # # # # # # #             if 'response' in response:
# # # # # # # # # # # # # # #                 response_text = response['response'].strip()
# # # # # # # # # # # # # # #                 if not response_text:
# # # # # # # # # # # # # # #                     logger.warning("Received an empty response from the model.")
# # # # # # # # # # # # # # #                     return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # # #                 logger.info("Response generated successfully.")
# # # # # # # # # # # # # # #                 return response_text
# # # # # # # # # # # # # # #             else:
# # # # # # # # # # # # # # #                 logger.error("No 'response' key in the response from Ollama.")
# # # # # # # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # # #     responder = OllamaResponder(model_name)

# # # # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # # # # #     print(response)


# # # # # # # # # # # # # # # ai_model.py

# # # # # # # # # # # # # # import os
# # # # # # # # # # # # # # import logging
# # # # # # # # # # # # # # import ollama

# # # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # # logging.basicConfig(level=logging.INFO)
# # # # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # # # #     def __init__(self, model_name=None, base_url='http://127.0.0.1:11434'):
# # # # # # # # # # # # # #         """
# # # # # # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # # # # # #         """
# # # # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # #         self.base_url = base_url
# # # # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # # # # # # # # #         # Initialize the Ollama client
# # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # #             self.client = ollama.Client(base_url=self.base_url)
# # # # # # # # # # # # # #             # Check if the model is available
# # # # # # # # # # # # # #             if not self.is_model_available(self.model_name):
# # # # # # # # # # # # # #                 logger.error(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # # # #                 raise EnvironmentError(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # # # # # # # # #             raise

# # # # # # # # # # # # # #     def is_model_available(self, model_name):
# # # # # # # # # # # # # #         """
# # # # # # # # # # # # # #         Check if the specified model is available in Ollama.
# # # # # # # # # # # # # #         """
# # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # #             models = self.client.list_models()
# # # # # # # # # # # # # #             available_models = [model['name'] for model in models]
# # # # # # # # # # # # # #             logger.debug(f"Available models: {available_models}")
# # # # # # # # # # # # # #             return model_name in available_models
# # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # #             logger.error(f"Error checking model availability: {e}")
# # # # # # # # # # # # # #             return False

# # # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # # # #         """
# # # # # # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # # # # # #         """
# # # # # # # # # # # # # #         try:
# # # # # # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # # # # #             if not prompt:
# # # # # # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # # # # #             # Generate response
# # # # # # # # # # # # # #             response_text = ''
# # # # # # # # # # # # # #             for chunk in self.client.generate(
# # # # # # # # # # # # # #                 model=self.model_name,
# # # # # # # # # # # # # #                 prompt=prompt,
# # # # # # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # # # # # #             ):
# # # # # # # # # # # # # #                 logger.debug(f"Response chunk: {chunk}")
# # # # # # # # # # # # # #                 if 'response' in chunk:
# # # # # # # # # # # # # #                     response_text += chunk['response']
# # # # # # # # # # # # # #                 elif 'error' in chunk:
# # # # # # # # # # # # # #                     logger.error(f"Error from Ollama: {chunk['error']}")
# # # # # # # # # # # # # #                     return "Sorry, I encountered an error while generating the response."
# # # # # # # # # # # # # #                 else:
# # # # # # # # # # # # # #                     logger.error(f"Unexpected response format: {chunk}")
# # # # # # # # # # # # # #                     return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # #             response_text = response_text.strip()
# # # # # # # # # # # # # #             if not response_text:
# # # # # # # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # # # #             return response_text

# # # # # # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # # #     base_url = 'http://127.0.0.1:11434'  # Adjust if running Ollama on a different port
# # # # # # # # # # # # # #     responder = OllamaResponder(model_name, base_url)

# # # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # # # #     print(response)

# # # # # # # # # # # # # # ai_model.py

# # # # # # # # # # # # # import os
# # # # # # # # # # # # # import logging
# # # # # # # # # # # # # import ollama

# # # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # # logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to see detailed logs
# # # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # # #     def __init__(self, model_name=None, base_url='http://127.0.0.1:11434'):
# # # # # # # # # # # # #         """
# # # # # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # # # # #         """
# # # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # #         self.base_url = base_url
# # # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # # # # # # # #         # Initialize the Ollama client
# # # # # # # # # # # # #         try:
# # # # # # # # # # # # #             self.client = ollama.Client(base_url=self.base_url)
# # # # # # # # # # # # #             # Check if the model is available
# # # # # # # # # # # # #             if not self.is_model_available(self.model_name):
# # # # # # # # # # # # #                 logger.error(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # # #                 raise EnvironmentError(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # # # # # # # #             raise

# # # # # # # # # # # # #     def is_model_available(self, model_name):
# # # # # # # # # # # # #         """
# # # # # # # # # # # # #         Check if the specified model is available in Ollama.
# # # # # # # # # # # # #         """
# # # # # # # # # # # # #         try:
# # # # # # # # # # # # #             models = self.client.list_models()
# # # # # # # # # # # # #             available_models = [model['name'] for model in models]
# # # # # # # # # # # # #             logger.debug(f"Available models: {available_models}")
# # # # # # # # # # # # #             return model_name in available_models
# # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # #             logger.error(f"Error checking model availability: {e}")
# # # # # # # # # # # # #             return False

# # # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # # #         """
# # # # # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # # # # #         """
# # # # # # # # # # # # #         try:
# # # # # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # # # #             if not prompt:
# # # # # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # # # #             # Generate response
# # # # # # # # # # # # #             response_text = ''
# # # # # # # # # # # # #             response = self.client.generate(
# # # # # # # # # # # # #                 model=self.model_name,
# # # # # # # # # # # # #                 prompt=prompt,
# # # # # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # # # # #             )

# # # # # # # # # # # # #             # Depending on the Ollama library version, response may be a generator yielding strings
# # # # # # # # # # # # #             # or dictionaries. We'll handle both cases.

# # # # # # # # # # # # #             for chunk in response:
# # # # # # # # # # # # #                 logger.debug(f"Chunk received: {chunk}")

# # # # # # # # # # # # #                 if isinstance(chunk, str):
# # # # # # # # # # # # #                     # If the chunk is a string, append it directly
# # # # # # # # # # # # #                     response_text += chunk
# # # # # # # # # # # # #                 elif isinstance(chunk, dict):
# # # # # # # # # # # # #                     # If the chunk is a dict, it might contain 'response' or 'choices'
# # # # # # # # # # # # #                     if 'response' in chunk:
# # # # # # # # # # # # #                         response_text += chunk['response']
# # # # # # # # # # # # #                     elif 'choices' in chunk:
# # # # # # # # # # # # #                         for choice in chunk['choices']:
# # # # # # # # # # # # #                             response_text += choice.get('text', '')
# # # # # # # # # # # # #                     elif 'data' in chunk:
# # # # # # # # # # # # #                         response_text += chunk['data']
# # # # # # # # # # # # #                     else:
# # # # # # # # # # # # #                         logger.error(f"Unexpected chunk format: {chunk}")
# # # # # # # # # # # # #                 else:
# # # # # # # # # # # # #                     logger.error(f"Unexpected chunk type: {type(chunk)}")

# # # # # # # # # # # # #             response_text = response_text.strip()
# # # # # # # # # # # # #             if not response_text:
# # # # # # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # # #             return response_text

# # # # # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # # #     # Example usage
# # # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # # #     base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
# # # # # # # # # # # # #     responder = OllamaResponder(model_name, base_url)

# # # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # # #     print(response)

# # # # # # # # # # # # # ai_model.py

# # # # # # # # # # # # import os
# # # # # # # # # # # # import logging
# # # # # # # # # # # # import urllib.parse
# # # # # # # # # # # # import ollama

# # # # # # # # # # # # # Configure logging
# # # # # # # # # # # # logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to see detailed logs
# # # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # # #     def __init__(self, model_name=None, base_url='http://127.0.0.1:11434'):
# # # # # # # # # # # #         """
# # # # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # # # #         """
# # # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # #         self.base_url = base_url
# # # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # # # # # # #         # Parse the base_url to extract host and port
# # # # # # # # # # # #         parsed_url = urllib.parse.urlparse(self.base_url)
# # # # # # # # # # # #         host = parsed_url.hostname or '127.0.0.1'
# # # # # # # # # # # #         port = parsed_url.port or 11434

# # # # # # # # # # # #         # Initialize the Ollama client
# # # # # # # # # # # #         try:
# # # # # # # # # # # #             self.client = ollama.Client(host=host, port=port)
# # # # # # # # # # # #             # Check if the model is available
# # # # # # # # # # # #             if not self.is_model_available(self.model_name):
# # # # # # # # # # # #                 logger.error(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # #                 raise EnvironmentError(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # # # # # # #             raise

# # # # # # # # # # # #     def is_model_available(self, model_name):
# # # # # # # # # # # #         """
# # # # # # # # # # # #         Check if the specified model is available in Ollama.
# # # # # # # # # # # #         """
# # # # # # # # # # # #         try:
# # # # # # # # # # # #             models = self.client.list_models()
# # # # # # # # # # # #             available_models = [model['name'] for model in models]
# # # # # # # # # # # #             logger.debug(f"Available models: {available_models}")
# # # # # # # # # # # #             return model_name in available_models
# # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # #             logger.error(f"Error checking model availability: {e}")
# # # # # # # # # # # #             return False

# # # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # # #         """
# # # # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # # # #         """
# # # # # # # # # # # #         try:
# # # # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # # #             if not prompt:
# # # # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # # #             # Generate response
# # # # # # # # # # # #             response_text = ''
# # # # # # # # # # # #             response = self.client.generate(
# # # # # # # # # # # #                 model=self.model_name,
# # # # # # # # # # # #                 prompt=prompt,
# # # # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # # # #             )

# # # # # # # # # # # #             # Depending on the Ollama library version, response may be a generator yielding strings
# # # # # # # # # # # #             # or dictionaries. We'll handle both cases.

# # # # # # # # # # # #             for chunk in response:
# # # # # # # # # # # #                 logger.debug(f"Chunk received: {chunk}")

# # # # # # # # # # # #                 if isinstance(chunk, str):
# # # # # # # # # # # #                     # If the chunk is a string, append it directly
# # # # # # # # # # # #                     response_text += chunk
# # # # # # # # # # # #                 elif isinstance(chunk, dict):
# # # # # # # # # # # #                     # If the chunk is a dict, it might contain 'response' or 'choices'
# # # # # # # # # # # #                     if 'response' in chunk:
# # # # # # # # # # # #                         response_text += chunk['response']
# # # # # # # # # # # #                     elif 'choices' in chunk:
# # # # # # # # # # # #                         for choice in chunk['choices']:
# # # # # # # # # # # #                             response_text += choice.get('text', '')
# # # # # # # # # # # #                     elif 'data' in chunk:
# # # # # # # # # # # #                         response_text += chunk['data']
# # # # # # # # # # # #                     else:
# # # # # # # # # # # #                         logger.error(f"Unexpected chunk format: {chunk}")
# # # # # # # # # # # #                 else:
# # # # # # # # # # # #                     logger.error(f"Unexpected chunk type: {type(chunk)}")

# # # # # # # # # # # #             response_text = response_text.strip()
# # # # # # # # # # # #             if not response_text:
# # # # # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # # #             return response_text

# # # # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # # # #         except Exception as e:
# # # # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # # #     # Example usage
# # # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # # #     base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
# # # # # # # # # # # #     responder = OllamaResponder(model_name, base_url)

# # # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # # #     print(response)

# # # # # # # # # # # # ai_model.py

# # # # # # # # # # # import os
# # # # # # # # # # # import logging
# # # # # # # # # # # import ollama

# # # # # # # # # # # # Configure logging
# # # # # # # # # # # logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to see detailed logs
# # # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # # class OllamaResponder:
# # # # # # # # # # #     def __init__(self, model_name=None, base_url='http://127.0.0.1:11434'):
# # # # # # # # # # #         """
# # # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # # #         """
# # # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # #         self.base_url = base_url
# # # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # # # # # #         # Initialize the Ollama client
# # # # # # # # # # #         try:
# # # # # # # # # # #             self.client = ollama.Client(self.base_url)
# # # # # # # # # # #             # Check if the model is available
# # # # # # # # # # #             if not self.is_model_available(self.model_name):
# # # # # # # # # # #                 logger.error(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # #                 raise EnvironmentError(f"Model '{self.model_name}' is not available in Ollama.")
# # # # # # # # # # #         except Exception as e:
# # # # # # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # # # # # #             raise

# # # # # # # # # # #     def is_model_available(self, model_name):
# # # # # # # # # # #         """
# # # # # # # # # # #         Check if the specified model is available in Ollama.
# # # # # # # # # # #         """
# # # # # # # # # # #         try:
# # # # # # # # # # #             models = self.client.list_models()
# # # # # # # # # # #             available_models = [model['name'] for model in models]
# # # # # # # # # # #             logger.debug(f"Available models: {available_models}")
# # # # # # # # # # #             return model_name in available_models
# # # # # # # # # # #         except Exception as e:
# # # # # # # # # # #             logger.error(f"Error checking model availability: {e}")
# # # # # # # # # # #             return False

# # # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # # #         """
# # # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # # #         """
# # # # # # # # # # #         try:
# # # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # # #             if not prompt:
# # # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # # #             # Generate response
# # # # # # # # # # #             response_text = ''
# # # # # # # # # # #             response = self.client.generate(
# # # # # # # # # # #                 model=self.model_name,
# # # # # # # # # # #                 prompt=prompt,
# # # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # # #             )

# # # # # # # # # # #             for chunk in response:
# # # # # # # # # # #                 logger.debug(f"Chunk received: {chunk}")

# # # # # # # # # # #                 if isinstance(chunk, str):
# # # # # # # # # # #                     # If the chunk is a string, append it directly
# # # # # # # # # # #                     response_text += chunk
# # # # # # # # # # #                 elif isinstance(chunk, dict):
# # # # # # # # # # #                     # If the chunk is a dict, it might contain 'response' or 'choices'
# # # # # # # # # # #                     if 'response' in chunk:
# # # # # # # # # # #                         response_text += chunk['response']
# # # # # # # # # # #                     elif 'choices' in chunk:
# # # # # # # # # # #                         for choice in chunk['choices']:
# # # # # # # # # # #                             response_text += choice.get('text', '')
# # # # # # # # # # #                     elif 'data' in chunk:
# # # # # # # # # # #                         response_text += chunk['data']
# # # # # # # # # # #                     else:
# # # # # # # # # # #                         logger.error(f"Unexpected chunk format: {chunk}")
# # # # # # # # # # #                 else:
# # # # # # # # # # #                     logger.error(f"Unexpected chunk type: {type(chunk)}")

# # # # # # # # # # #             response_text = response_text.strip()
# # # # # # # # # # #             if not response_text:
# # # # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # # #             return response_text

# # # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # # #         except Exception as e:
# # # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # # #     # Example usage
# # # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # # #     base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
# # # # # # # # # # #     responder = OllamaResponder(model_name, base_url)

# # # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # # #     print(response)

# # # # # # # # # # # ai_model.py

# # # # # # # # # # import os
# # # # # # # # # # import logging
# # # # # # # # # # import ollama

# # # # # # # # # # # Configure logging
# # # # # # # # # # logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to capture detailed logs
# # # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # # class OllamaResponder:
# # # # # # # # # #     def __init__(self, model_name=None, base_url='http://127.0.0.1:11434'):
# # # # # # # # # #         """
# # # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # # #         """
# # # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # #         self.base_url = base_url
# # # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # # # # #         # Initialize the Ollama client
# # # # # # # # # #         try:
# # # # # # # # # #             self.client = ollama.Client(self.base_url)
# # # # # # # # # #             logger.debug("Ollama client initialized successfully.")
# # # # # # # # # #         except Exception as e:
# # # # # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # # # # #             raise

# # # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # # #         """
# # # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # # #         """
# # # # # # # # # #         try:
# # # # # # # # # #             # Sanitize the prompt
# # # # # # # # # #             prompt = prompt.strip()
# # # # # # # # # #             if not prompt:
# # # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # # #             # Generate response
# # # # # # # # # #             response_text = ''
# # # # # # # # # #             response = self.client.generate(
# # # # # # # # # #                 model=self.model_name,
# # # # # # # # # #                 prompt=prompt,
# # # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # # #             )

# # # # # # # # # #             for chunk in response:
# # # # # # # # # #                 logger.debug(f"Chunk received: {chunk}")

# # # # # # # # # #                 if isinstance(chunk, str):
# # # # # # # # # #                     # If the chunk is a string, append it directly
# # # # # # # # # #                     response_text += chunk
# # # # # # # # # #                 elif isinstance(chunk, dict):
# # # # # # # # # #                     # If the chunk is a dict, it might contain 'response' or 'choices'
# # # # # # # # # #                     if 'response' in chunk:
# # # # # # # # # #                         response_text += chunk['response']
# # # # # # # # # #                     elif 'choices' in chunk:
# # # # # # # # # #                         for choice in chunk['choices']:
# # # # # # # # # #                             response_text += choice.get('text', '')
# # # # # # # # # #                     elif 'data' in chunk:
# # # # # # # # # #                         response_text += chunk['data']
# # # # # # # # # #                     else:
# # # # # # # # # #                         logger.error(f"Unexpected chunk format: {chunk}")
# # # # # # # # # #                 else:
# # # # # # # # # #                     logger.error(f"Unexpected chunk type: {type(chunk)}")

# # # # # # # # # #             response_text = response_text.strip()
# # # # # # # # # #             if not response_text:
# # # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # # #             return response_text

# # # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # # #         except Exception as e:
# # # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # # if __name__ == "__main__":
# # # # # # # # # #     # Example usage
# # # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # # #     base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
# # # # # # # # # #     try:
# # # # # # # # # #         responder = OllamaResponder(model_name, base_url)
# # # # # # # # # #     except Exception as e:
# # # # # # # # # #         logger.error(f"Cannot initialize OllamaResponder: {e}")
# # # # # # # # # #         exit(1)

# # # # # # # # # #     # Sample prompt for testing
# # # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # # #     print(response)

# # # # # # # # # # ai_model.py

# # # # # # # # # import os
# # # # # # # # # import logging
# # # # # # # # # import ollama

# # # # # # # # # # Configure logging
# # # # # # # # # logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to capture detailed logs
# # # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # # class OllamaResponder:
# # # # # # # # #     def __init__(self, model_name=None, base_url='http://127.0.0.1:11434'):
# # # # # # # # #         """
# # # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # # #         """
# # # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # #         self.base_url = base_url
# # # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # # # #         # Initialize the Ollama client
# # # # # # # # #         try:
# # # # # # # # #             self.client = ollama.Client(self.base_url)
# # # # # # # # #             logger.debug("Ollama client initialized successfully.")
# # # # # # # # #         except Exception as e:
# # # # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # # # #             raise

# # # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # # #         """
# # # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # # #         """
# # # # # # # # #         try:
# # # # # # # # #             # Sanitize the prompt
# # # # # # # # #             prompt = prompt.strip()
# # # # # # # # #             if not prompt:
# # # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # # #             # Generate response
# # # # # # # # #             response_text = ''
# # # # # # # # #             response = self.client.generate(
# # # # # # # # #                 model=self.model_name,
# # # # # # # # #                 prompt=prompt,
# # # # # # # # #                 options={'max_length': max_length}
# # # # # # # # #             )

# # # # # # # # #             for chunk in response:
# # # # # # # # #                 logger.debug(f"Chunk received: {chunk}")

# # # # # # # # #                 if isinstance(chunk, str):
# # # # # # # # #                     # If the chunk is a string, append it directly
# # # # # # # # #                     response_text += chunk
# # # # # # # # #                 elif isinstance(chunk, dict):
# # # # # # # # #                     # If the chunk is a dict, it might contain 'response' or 'choices'
# # # # # # # # #                     if 'response' in chunk:
# # # # # # # # #                         response_text += chunk['response']
# # # # # # # # #                     elif 'choices' in chunk:
# # # # # # # # #                         for choice in chunk['choices']:
# # # # # # # # #                             response_text += choice.get('text', '')
# # # # # # # # #                     elif 'data' in chunk:
# # # # # # # # #                         response_text += chunk['data']
# # # # # # # # #                     else:
# # # # # # # # #                         logger.error(f"Unexpected chunk format: {chunk}")
# # # # # # # # #                 else:
# # # # # # # # #                     logger.error(f"Unexpected chunk type: {type(chunk)}")

# # # # # # # # #             response_text = response_text.strip()
# # # # # # # # #             if not response_text:
# # # # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # # #             logger.info("Response generated successfully.")
# # # # # # # # #             return response_text

# # # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # # #         except Exception as e:
# # # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # # if __name__ == "__main__":
# # # # # # # # #     # Example usage
# # # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # # #     base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
# # # # # # # # #     try:
# # # # # # # # #         responder = OllamaResponder(model_name, base_url)
# # # # # # # # #     except Exception as e:
# # # # # # # # #         logger.error(f"Cannot initialize OllamaResponder: {e}")
# # # # # # # # #         exit(1)

# # # # # # # # #     # Sample prompt for testing
# # # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # # #     print(response)


# # # # # # # # # ai_model.py

# # # # # # # # import os
# # # # # # # # import logging
# # # # # # # # import ollama

# # # # # # # # # Configure logging
# # # # # # # # logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG to capture detailed logs
# # # # # # # # logger = logging.getLogger(__name__)

# # # # # # # # class OllamaResponder:
# # # # # # # #     def __init__(self, model_name=None, base_url='http://127.0.0.1:11434'):
# # # # # # # #         """
# # # # # # # #         Initialize the OllamaResponder using the Ollama Python library.
# # # # # # # #         """
# # # # # # # #         # Load the model name from environment variable or fall back to default
# # # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # #         self.base_url = base_url
# # # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # # #         # Initialize the Ollama client
# # # # # # # #         try:
# # # # # # # #             self.client = ollama.Client(self.base_url)
# # # # # # # #             logger.debug("Ollama client initialized successfully.")
# # # # # # # #         except Exception as e:
# # # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # # #             raise

# # # # # # # #     def generate_response(self, prompt, max_length=150):
# # # # # # # #         """
# # # # # # # #         Generate a response using the Ollama Python library.
# # # # # # # #         """
# # # # # # # #         try:
# # # # # # # #             # Sanitize the prompt
# # # # # # # #             prompt = prompt.strip()
# # # # # # # #             if not prompt:
# # # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # # #                 return "Please provide a valid prompt."

# # # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}...")
# # # # # # # #             # Generate response
# # # # # # # #             response = self.client.generate(
# # # # # # # #                 model=self.model_name,
# # # # # # # #                 prompt=prompt,
# # # # # # # #                 options={'max_length': max_length}
# # # # # # # #             )

# # # # # # # #             # Check the type of response
# # # # # # # #             if isinstance(response, dict):
# # # # # # # #                 # Directly access the 'response' key
# # # # # # # #                 response_text = response.get('response', '').strip()
# # # # # # # #                 if not response_text:
# # # # # # # #                     logger.warning("Received an empty 'response' from the model.")
# # # # # # # #                     return "Sorry, I couldn't generate a response."
# # # # # # # #                 logger.info("Response generated successfully.")
# # # # # # # #                 return response_text
# # # # # # # #             elif isinstance(response, str):
# # # # # # # #                 # If response is a string, return it directly
# # # # # # # #                 response_text = response.strip()
# # # # # # # #                 if not response_text:
# # # # # # # #                     logger.warning("Received an empty string response from the model.")
# # # # # # # #                     return "Sorry, I couldn't generate a response."
# # # # # # # #                 logger.info("Response generated successfully.")
# # # # # # # #                 return response_text
# # # # # # # #             else:
# # # # # # # #                 # Handle unexpected response formats
# # # # # # # #                 logger.error(f"Unexpected response format: {type(response)}")
# # # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # # #         except ollama.ModelNotFoundError:
# # # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # # #         except Exception as e:
# # # # # # # #             logger.error(f"An error occurred during response generation: {e}")
# # # # # # # #             return "Sorry, I encountered an error while generating the response."

# # # # # # # # if __name__ == "__main__":
# # # # # # # #     # Example usage
# # # # # # # #     model_name = os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # # #     base_url = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
# # # # # # # #     try:
# # # # # # # #         responder = OllamaResponder(model_name, base_url)
# # # # # # # #     except Exception as e:
# # # # # # # #         logger.error(f"Cannot initialize OllamaResponder: {e}")
# # # # # # # #         exit(1)

# # # # # # # #     # Sample prompt for testing
# # # # # # # #     prompt = "Explain the key points of the Agriculture Bill."
# # # # # # # #     response = responder.generate_response(prompt)

# # # # # # # #     print(response)


# # # # # # # # ai_model.py

# # # # # # # import os
# # # # # # # import logging
# # # # # # # import time
# # # # # # # from typing import Optional

# # # # # # # import ollama  # Ensure this library is installed: pip install ollama

# # # # # # # # Configure logging
# # # # # # # LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# # # # # # # LOG_FORMAT = os.environ.get(
# # # # # # #     "LOG_FORMAT",
# # # # # # #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# # # # # # # )
# # # # # # # LOG_FILE = os.environ.get("LOG_FILE", "ai_model.log")

# # # # # # # logging.basicConfig(
# # # # # # #     level=LOG_LEVEL,
# # # # # # #     format=LOG_FORMAT,
# # # # # # #     handlers=[
# # # # # # #         logging.FileHandler(LOG_FILE),
# # # # # # #         logging.StreamHandler()
# # # # # # #     ]
# # # # # # # )
# # # # # # # logger = logging.getLogger(__name__)


# # # # # # # class OllamaResponder:
# # # # # # #     """
# # # # # # #     A responder class that interacts with the Ollama AI model to generate responses based on prompts.
# # # # # # #     """

# # # # # # #     def __init__(
# # # # # # #         self,
# # # # # # #         model_name: Optional[str] = None,
# # # # # # #         base_url: str = 'http://127.0.0.1:11434',
# # # # # # #         max_retries: int = 3,
# # # # # # #         retry_delay: float = 2.0
# # # # # # #     ):
# # # # # # #         """
# # # # # # #         Initialize the OllamaResponder.

# # # # # # #         Args:
# # # # # # #             model_name (Optional[str]): Name of the Ollama model to use. Defaults to environment variable or 'llama3.2:latest'.
# # # # # # #             base_url (str): Base URL for the Ollama API. Defaults to 'http://127.0.0.1:11434'.
# # # # # # #             max_retries (int): Maximum number of retries for API requests. Defaults to 3.
# # # # # # #             retry_delay (float): Initial delay between retries in seconds. Defaults to 2.0.
# # # # # # #         """
# # # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # # #         self.base_url = base_url
# # # # # # #         self.max_retries = max_retries
# # # # # # #         self.retry_delay = retry_delay

# # # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # # #         # Initialize the Ollama client
# # # # # # #         try:
# # # # # # #             self.client = ollama.Client(self.base_url)
# # # # # # #             logger.debug("Ollama client initialized successfully.")
# # # # # # #         except Exception as e:
# # # # # # #             logger.error(f"Failed to initialize Ollama client: {e}")
# # # # # # #             raise

# # # # # # #     def generate_response(
# # # # # # #         self,
# # # # # # #         prompt: str,
# # # # # # #         max_length: int = 150,
# # # # # # #         temperature: float = 0.7,
# # # # # # #         stop_sequences: Optional[list] = None,
# # # # # # #         retries: int = 0
# # # # # # #     ) -> str:
# # # # # # #         """
# # # # # # #         Generate a response from the Ollama model based on the provided prompt.

# # # # # # #         Args:
# # # # # # #             prompt (str): The input prompt for the AI model.
# # # # # # #             max_length (int): Maximum number of tokens in the response. Defaults to 150.
# # # # # # #             temperature (float): Sampling temperature for response variability. Defaults to 0.7.
# # # # # # #             stop_sequences (Optional[list]): Sequences where the AI should stop generating further tokens.
# # # # # # #             retries (int): Current retry attempt. Used internally for recursion.

# # # # # # #         Returns:
# # # # # # #             str: The AI-generated response.
# # # # # # #         """
# # # # # # #         try:
# # # # # # #             # Sanitize the prompt
# # # # # # #             prompt = prompt.strip()
# # # # # # #             if not prompt:
# # # # # # #                 logger.warning("Empty prompt received.")
# # # # # # #                 return "Please provide a valid prompt."

# # # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}{'...' if len(prompt) > 30 else ''}")

# # # # # # #             # Generate response
# # # # # # #             response = self.client.generate(
# # # # # # #                 model=self.model_name,
# # # # # # #                 prompt=prompt,
# # # # # # #                 options={
# # # # # # #                     'max_length': max_length,
# # # # # # #                     'temperature': temperature,
# # # # # # #                     'stop': stop_sequences
# # # # # # #                 }
# # # # # # #             )

# # # # # # #             # Process response based on its type
# # # # # # #             if isinstance(response, dict):
# # # # # # #                 response_text = response.get('response', '').strip()
# # # # # # #             elif isinstance(response, str):
# # # # # # #                 response_text = response.strip()
# # # # # # #             else:
# # # # # # #                 logger.error(f"Unexpected response format: {type(response)}")
# # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # #             if not response_text:
# # # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # # #             logger.info("Response generated successfully.")
# # # # # # #             return response_text

# # # # # # #         except ollama.ModelNotFoundError:
# # # # # # #             logger.error(f"Model '{self.model_name}' not found in Ollama.")
# # # # # # #             return f"Model '{self.model_name}' is not available."
# # # # # # #         except ollama.RequestError as e:
# # # # # # #             logger.error(f"Ollama API request error: {e}")
# # # # # # #             if retries < self.max_retries:
# # # # # # #                 wait = self.retry_delay * (2 ** retries)  # Exponential backoff
# # # # # # #                 logger.info(f"Retrying in {wait} seconds... (Attempt {retries + 1}/{self.max_retries})")
# # # # # # #                 time.sleep(wait)
# # # # # # #                 return self.generate_response(prompt, max_length, temperature, stop_sequences, retries + 1)
# # # # # # #             else:
# # # # # # #                 logger.error("Max retries exceeded. Unable to generate response.")
# # # # # # #                 return "Sorry, I couldn't process your request at this time."
# # # # # # #         except Exception as e:
# # # # # # #             logger.error(f"An unexpected error occurred: {e}")
# # # # # # #             return "Sorry, I encountered an error while generating the response."


# # # # # # # if __name__ == "__main__":
# # # # # # #     # Example usage
# # # # # # #     try:
# # # # # # #         responder = OllamaResponder()
# # # # # # #     except Exception as e:
# # # # # # #         logger.critical(f"Cannot initialize OllamaResponder: {e}")
# # # # # # #         exit(1)

# # # # # # #     # Sample prompts for testing
# # # # # # #     test_prompts = [
# # # # # # #         "Explain the key points of the Agriculture Bill.",
# # # # # # #         "What is the Sustainable Farming Act?",
# # # # # # #         ""  # Empty prompt to test validation
# # # # # # #     ]

# # # # # # #     for prompt in test_prompts:
# # # # # # #         response = responder.generate_response(prompt)
# # # # # # #         print(f"Prompt: {prompt}\nResponse: {response}\n{'-'*60}")


# # # # # # # ai_model.py

# # # # # # import os
# # # # # # import logging
# # # # # # import time
# # # # # # from typing import Optional

# # # # # # import requests  # Ensure this library is installed: pip install requests

# # # # # # # Configure logging
# # # # # # LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# # # # # # LOG_FORMAT = os.environ.get(
# # # # # #     "LOG_FORMAT",
# # # # # #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# # # # # # )
# # # # # # LOG_FILE = os.environ.get("LOG_FILE", "ai_model.log")

# # # # # # logging.basicConfig(
# # # # # #     level=LOG_LEVEL,
# # # # # #     format=LOG_FORMAT,
# # # # # #     handlers=[
# # # # # #         logging.FileHandler(LOG_FILE),
# # # # # #         logging.StreamHandler()
# # # # # #     ]
# # # # # # )
# # # # # # logger = logging.getLogger(__name__)


# # # # # # class OllamaResponder:
# # # # # #     """
# # # # # #     A responder class that interacts with the Ollama AI model to generate responses based on prompts.
# # # # # #     """

# # # # # #     def __init__(
# # # # # #         self,
# # # # # #         model_name: Optional[str] = None,
# # # # # #         base_url: str = 'http://127.0.0.1:11434',
# # # # # #         max_retries: int = 3,
# # # # # #         retry_delay: float = 2.0
# # # # # #     ):
# # # # # #         """
# # # # # #         Initialize the OllamaResponder.

# # # # # #         Args:
# # # # # #             model_name (Optional[str]): Name of the Ollama model to use. Defaults to environment variable or 'llama3.2:latest'.
# # # # # #             base_url (str): Base URL for the Ollama API. Defaults to 'http://127.0.0.1:11434'.
# # # # # #             max_retries (int): Maximum number of retries for API requests. Defaults to 3.
# # # # # #             retry_delay (float): Initial delay between retries in seconds. Defaults to 2.0.
# # # # # #         """
# # # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # # #         self.base_url = base_url
# # # # # #         self.max_retries = max_retries
# # # # # #         self.retry_delay = retry_delay

# # # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # # #     def generate_response(
# # # # # #         self,
# # # # # #         prompt: str,
# # # # # #         max_length: int = 150,
# # # # # #         temperature: float = 0.7,
# # # # # #         stop_sequences: Optional[list] = None,
# # # # # #         retries: int = 0
# # # # # #     ) -> str:
# # # # # #         """
# # # # # #         Generate a response from the Ollama model based on the provided prompt.

# # # # # #         Args:
# # # # # #             prompt (str): The input prompt for the AI model.
# # # # # #             max_length (int): Maximum number of tokens in the response. Defaults to 150.
# # # # # #             temperature (float): Sampling temperature for response variability. Defaults to 0.7.
# # # # # #             stop_sequences (Optional[list]): Sequences where the AI should stop generating further tokens.
# # # # # #             retries (int): Current retry attempt. Used internally for recursion.

# # # # # #         Returns:
# # # # # #             str: The AI-generated response.
# # # # # #         """
# # # # # #         try:
# # # # # #             # Sanitize the prompt
# # # # # #             prompt = prompt.strip()
# # # # # #             if not prompt:
# # # # # #                 logger.warning("Empty prompt received.")
# # # # # #                 return "Please provide a valid prompt."

# # # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}{'...' if len(prompt) > 30 else ''}")

# # # # # #             # Prepare the payload for the Ollama API
# # # # # #             payload = {
# # # # # #                 "prompt": prompt,
# # # # # #                 "max_tokens": max_length,
# # # # # #                 "temperature": temperature,
# # # # # #                 "stop": stop_sequences
# # # # # #             }

# # # # # #             # Send the request to the Ollama API
# # # # # #             response = requests.post(
# # # # # #                 f"{self.base_url}/v1/models/{self.model_name}/generate",
# # # # # #                 json=payload,
# # # # # #                 timeout=30  # Timeout after 30 seconds
# # # # # #             )
# # # # # #             response.raise_for_status()  # Raise an exception for HTTP errors

# # # # # #             data = response.json()

# # # # # #             # Extract the generated text
# # # # # #             response_text = data.get("response", "").strip()

# # # # # #             if not response_text:
# # # # # #                 logger.warning("Received an empty response from the model.")
# # # # # #                 return "Sorry, I couldn't generate a response."

# # # # # #             logger.info("Response generated successfully.")
# # # # # #             return response_text

# # # # # #         except requests.exceptions.HTTPError as http_err:
# # # # # #             logger.error(f"HTTP error occurred: {http_err}")
# # # # # #             return "Sorry, I encountered an HTTP error while generating the response."
# # # # # #         except requests.exceptions.ConnectionError as conn_err:
# # # # # #             logger.error(f"Connection error occurred: {conn_err}")
# # # # # #             if retries < self.max_retries:
# # # # # #                 wait = self.retry_delay * (2 ** retries)  # Exponential backoff
# # # # # #                 logger.info(f"Retrying in {wait} seconds... (Attempt {retries + 1}/{self.max_retries})")
# # # # # #                 time.sleep(wait)
# # # # # #                 return self.generate_response(prompt, max_length, temperature, stop_sequences, retries + 1)
# # # # # #             else:
# # # # # #                 logger.error("Max retries exceeded. Unable to generate response.")
# # # # # #                 return "Sorry, I couldn't process your request at this time."
# # # # # #         except requests.exceptions.Timeout as timeout_err:
# # # # # #             logger.error(f"Timeout error occurred: {timeout_err}")
# # # # # #             return "Sorry, the request timed out while generating the response."
# # # # # #         except requests.exceptions.RequestException as req_err:
# # # # # #             logger.error(f"Request exception occurred: {req_err}")
# # # # # #             return "Sorry, an error occurred while generating the response."
# # # # # #         except Exception as e:
# # # # # #             logger.error(f"An unexpected error occurred: {e}")
# # # # # #             return "Sorry, I encountered an error while generating the response."


# # # # # # if __name__ == "__main__":
# # # # # #     # Example usage
# # # # # #     try:
# # # # # #         responder = OllamaResponder()
# # # # # #     except Exception as e:
# # # # # #         logger.critical(f"Cannot initialize OllamaResponder: {e}")
# # # # # #         exit(1)

# # # # # #     # Sample prompts for testing
# # # # # #     test_prompts = [
# # # # # #         "Explain the key points of the Agriculture Bill.",
# # # # # #         "What is the Sustainable Farming Act?",
# # # # # #         ""  # Empty prompt to test validation
# # # # # #     ]

# # # # # #     for prompt in test_prompts:
# # # # # #         response = responder.generate_response(prompt)
# # # # # #         print(f"Prompt: {prompt}\nResponse: {response}\n{'-'*60}")

# # # # # # ai_model.py



# # # # # import os
# # # # # import logging
# # # # # import time
# # # # # from typing import Optional

# # # # # import requests  # Ensure this library is installed: pip install requests
# # # # # from dotenv import load_dotenv

# # # # # load_dotenv()  # Load environment variables from .env

# # # # # # After load_dotenv()
# # # # # print(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
# # # # # print(f"OLLAMA_MODEL_NAME: {os.environ.get('OLLAMA_MODEL_NAME')}")
# # # # # print(f"OLLAMA_BASE_URL: {os.environ.get('OLLAMA_BASE_URL')}")

# # # # # # Configure logging
# # # # # LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# # # # # LOG_FORMAT = os.environ.get(
# # # # #     "LOG_FORMAT",
# # # # #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# # # # # )
# # # # # LOG_FILE = os.environ.get("LOG_FILE", "ai_model.log")

# # # # # logging.basicConfig(
# # # # #     level=LOG_LEVEL,
# # # # #     format=LOG_FORMAT,
# # # # #     handlers=[
# # # # #         logging.FileHandler(LOG_FILE),
# # # # #         logging.StreamHandler()
# # # # #     ]
# # # # # )
# # # # # logger = logging.getLogger(__name__)


# # # # # class OllamaResponder:
# # # # #     """
# # # # #     A responder class that interacts with the Ollama AI model to generate responses based on prompts.
# # # # #     """

# # # # #     def __init__(
# # # # #         self,
# # # # #         model_name: Optional[str] = None,
# # # # #         base_url: str = 'http://127.0.0.1:11434',
# # # # #         max_retries: int = 3,
# # # # #         retry_delay: float = 2.0
# # # # #     ):
# # # # #         """
# # # # #         Initialize the OllamaResponder.

# # # # #         Args:
# # # # #             model_name (Optional[str]): Name of the Ollama model to use. Defaults to environment variable or 'llama3.2:latest'.
# # # # #             base_url (str): Base URL for the Ollama API. Defaults to 'http://127.0.0.1:11434'.
# # # # #             max_retries (int): Maximum number of retries for API requests. Defaults to 3.
# # # # #             retry_delay (float): Initial delay between retries in seconds. Defaults to 2.0.
# # # # #         """
# # # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # # #         self.base_url = base_url
# # # # #         self.max_retries = max_retries
# # # # #         self.retry_delay = retry_delay

# # # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # # #     def generate_response(
# # # # #         self,
# # # # #         prompt: str,
# # # # #         max_length: int = 150,
# # # # #         temperature: float = 0.7,
# # # # #         stop_sequences: Optional[list] = None,
# # # # #         retries: int = 0
# # # # #     ) -> str:
# # # # #         """
# # # # #         Generate a response from the Ollama model based on the provided prompt.

# # # # #         Args:
# # # # #             prompt (str): The input prompt for the AI model.
# # # # #             max_length (int): Maximum number of tokens in the response. Defaults to 150.
# # # # #             temperature (float): Sampling temperature for response variability. Defaults to 0.7.
# # # # #             stop_sequences (Optional[list]): Sequences where the AI should stop generating further tokens.
# # # # #             retries (int): Current retry attempt. Used internally for recursion.

# # # # #         Returns:
# # # # #             str: The AI-generated response.
# # # # #         """
# # # # #         try:
# # # # #             # Sanitize the prompt
# # # # #             prompt = prompt.strip()
# # # # #             if not prompt:
# # # # #                 logger.warning("Empty prompt received.")
# # # # #                 return "Please provide a valid prompt."

# # # # #             logger.info(f"Generating response for prompt: {prompt[:30]}{'...' if len(prompt) > 30 else ''}")

# # # # #             # Prepare the payload for the Ollama API
# # # # #             payload = {
# # # # #                 "prompt": prompt,
# # # # #                 "max_tokens": max_length,
# # # # #                 "temperature": temperature,
# # # # #                 "stop": stop_sequences
# # # # #             }

# # # # #             # Send the request to the Ollama API
# # # # #             response = requests.post(
# # # # #                 f"{self.base_url}/v1/models/{self.model_name}/generate",
# # # # #                 json=payload,
# # # # #                 timeout=30  # Timeout after 30 seconds
# # # # #             )
# # # # #             response.raise_for_status()  # Raise an exception for HTTP errors

# # # # #             data = response.json()

# # # # #             # Extract the generated text
# # # # #             response_text = data.get("response", "").strip()

# # # # #             if not response_text:
# # # # #                 logger.warning("Received an empty response from the model.")
# # # # #                 return "Sorry, I couldn't generate a response."

# # # # #             logger.info("Response generated successfully.")
# # # # #             return response_text

# # # # #         except requests.exceptions.HTTPError as http_err:
# # # # #             logger.error(f"HTTP error occurred: {http_err} - URL: {response.url}")
# # # # #             return "Sorry, I encountered an HTTP error while generating the response."
# # # # #         except requests.exceptions.ConnectionError as conn_err:
# # # # #             logger.error(f"Connection error occurred: {conn_err}")
# # # # #             if retries < self.max_retries:
# # # # #                 wait = self.retry_delay * (2 ** retries)  # Exponential backoff
# # # # #                 logger.info(f"Retrying in {wait} seconds... (Attempt {retries + 1}/{self.max_retries})")
# # # # #                 time.sleep(wait)
# # # # #                 return self.generate_response(prompt, max_length, temperature, stop_sequences, retries + 1)
# # # # #             else:
# # # # #                 logger.error("Max retries exceeded. Unable to generate response.")
# # # # #                 return "Sorry, I couldn't process your request at this time."
# # # # #         except requests.exceptions.Timeout as timeout_err:
# # # # #             logger.error(f"Timeout error occurred: {timeout_err}")
# # # # #             return "Sorry, the request timed out while generating the response."
# # # # #         except requests.exceptions.RequestException as req_err:
# # # # #             logger.error(f"Request exception occurred: {req_err}")
# # # # #             return "Sorry, an error occurred while generating the response."
# # # # #         except Exception as e:
# # # # #             logger.error(f"An unexpected error occurred: {e}")
# # # # #             return "Sorry, I encountered an error while generating the response."


# # # # # if __name__ == "__main__":
# # # # #     # Example usage
# # # # #     try:
# # # # #         responder = OllamaResponder()
# # # # #     except Exception as e:
# # # # #         logger.critical(f"Cannot initialize OllamaResponder: {e}")
# # # # #         exit(1)

# # # # #     # Sample prompts for testing
# # # # #     test_prompts = [
# # # # #         "Explain the key points of the Agriculture Bill.",
# # # # #         "What is the Sustainable Farming Act?",
# # # # #         ""  # Empty prompt to test validation
# # # # #     ]

# # # # #     for prompt in test_prompts:
# # # # #         response = responder.generate_response(prompt)
# # # # #         print(f"Prompt: {prompt}\nResponse: {response}\n{'-'*60}")


# # # # # ai_model.py

# # # # from dotenv import load_dotenv
# # # # load_dotenv()  # Load environment variables from .env

# # # # import os
# # # # import logging
# # # # import time
# # # # from typing import Optional

# # # # import requests  # Ensure this library is installed: pip install requests

# # # # # Configure logging
# # # # LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# # # # LOG_FORMAT = os.environ.get(
# # # #     "LOG_FORMAT",
# # # #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# # # # )
# # # # LOG_FILE = os.environ.get("LOG_FILE", "ai_model.log")

# # # # logging.basicConfig(
# # # #     level=LOG_LEVEL,
# # # #     format=LOG_FORMAT,
# # # #     handlers=[
# # # #         logging.FileHandler(LOG_FILE),
# # # #         logging.StreamHandler()
# # # #     ]
# # # # )
# # # # logger = logging.getLogger(__name__)

# # # # # Debugging: Print environment variables
# # # # logger.debug(f"DATABASE_URL: {os.environ.get('DATABASE_URL')}")
# # # # logger.debug(f"OLLAMA_MODEL_NAME: {os.environ.get('OLLAMA_MODEL_NAME')}")
# # # # logger.debug(f"OLLAMA_BASE_URL: {os.environ.get('OLLAMA_BASE_URL')}")

# # # # class OllamaResponder:
# # # #     """
# # # #     A responder class that interacts with the Ollama AI model to generate responses based on prompts.
# # # #     """

# # # #     def __init__(
# # # #         self,
# # # #         model_name: Optional[str] = None,
# # # #         base_url: str = 'http://127.0.0.1:11434',
# # # #         max_retries: int = 3,
# # # #         retry_delay: float = 2.0
# # # #     ):
# # # #         """
# # # #         Initialize the OllamaResponder.

# # # #         Args:
# # # #             model_name (Optional[str]): Name of the Ollama model to use. Defaults to environment variable or 'llama3.2:latest'.
# # # #             base_url (str): Base URL for the Ollama API. Defaults to 'http://127.0.0.1:11434'.
# # # #             max_retries (int): Maximum number of retries for API requests. Defaults to 3.
# # # #             retry_delay (float): Initial delay between retries in seconds. Defaults to 2.0.
# # # #         """
# # # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # # #         self.base_url = base_url
# # # #         self.max_retries = max_retries
# # # #         self.retry_delay = retry_delay

# # # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # # #     def generate_response(
# # # #         self,
# # # #         prompt: str,
# # # #         max_length: int = 150,
# # # #         temperature: float = 0.7,
# # # #         stop_sequences: Optional[list] = None,
# # # #         retries: int = 0
# # # #     ) -> str:
# # # #         """
# # # #         Generate a response from the Ollama model based on the provided prompt.

# # # #         Args:
# # # #             prompt (str): The input prompt for the AI model.
# # # #             max_length (int): Maximum number of tokens in the response. Defaults to 150.
# # # #             temperature (float): Sampling temperature for response variability. Defaults to 0.7.
# # # #             stop_sequences (Optional[list]): Sequences where the AI should stop generating further tokens.
# # # #             retries (int): Current retry attempt. Used internally for recursion.

# # # #         Returns:
# # # #             str: The AI-generated response.
# # # #         """
# # # #         try:
# # # #             # Sanitize the prompt
# # # #             prompt = prompt.strip()
# # # #             if not prompt:
# # # #                 logger.warning("Empty prompt received.")
# # # #                 return "Please provide a valid prompt."

# # # #             logger.info(f"Generating response for prompt: {prompt[:30]}{'...' if len(prompt) > 30 else ''}")

# # # #             # Prepare the payload for the Ollama API
# # # #             payload = {
# # # #                 "prompt": prompt,
# # # #                 "max_tokens": max_length,
# # # #                 "temperature": temperature,
# # # #                 "stop": stop_sequences
# # # #             }

# # # #             # Send the request to the Ollama API
# # # #             response = requests.post(
# # # #                 f"{self.base_url}/v1/models/{self.model_name}/generate",
# # # #                 json=payload,
# # # #                 timeout=30  # Timeout after 30 seconds
# # # #             )
# # # #             response.raise_for_status()  # Raise an exception for HTTP errors

# # # #             data = response.json()

# # # #             # Extract the generated text
# # # #             response_text = data.get("response", "").strip()

# # # #             if not response_text:
# # # #                 logger.warning("Received an empty response from the model.")
# # # #                 return "Sorry, I couldn't generate a response."

# # # #             logger.info("Response generated successfully.")
# # # #             return response_text

# # # #         except requests.exceptions.HTTPError as http_err:
# # # #             logger.error(f"HTTP error occurred: {http_err} - URL: {response.url}")
# # # #             return "Sorry, I encountered an HTTP error while generating the response."
# # # #         except requests.exceptions.ConnectionError as conn_err:
# # # #             logger.error(f"Connection error occurred: {conn_err}")
# # # #             if retries < self.max_retries:
# # # #                 wait = self.retry_delay * (2 ** retries)  # Exponential backoff
# # # #                 logger.info(f"Retrying in {wait} seconds... (Attempt {retries + 1}/{self.max_retries})")
# # # #                 time.sleep(wait)
# # # #                 return self.generate_response(prompt, max_length, temperature, stop_sequences, retries + 1)
# # # #             else:
# # # #                 logger.error("Max retries exceeded. Unable to generate response.")
# # # #                 return "Sorry, I couldn't process your request at this time."
# # # #         except requests.exceptions.Timeout as timeout_err:
# # # #             logger.error(f"Timeout error occurred: {timeout_err}")
# # # #             return "Sorry, the request timed out while generating the response."
# # # #         except requests.exceptions.RequestException as req_err:
# # # #             logger.error(f"Request exception occurred: {req_err}")
# # # #             return "Sorry, an error occurred while generating the response."
# # # #         except Exception as e:
# # # #             logger.error(f"An unexpected error occurred: {e}")
# # # #             return "Sorry, I encountered an error while generating the response."


# # # # if __name__ == "__main__":
# # # #     # Example usage
# # # #     try:
# # # #         responder = OllamaResponder()
# # # #     except Exception as e:
# # # #         logger.critical(f"Cannot initialize OllamaResponder: {e}")
# # # #         exit(1)

# # # #     # Sample prompts for testing
# # # #     test_prompts = [
# # # #         "Explain the key points of the Agriculture Bill.",
# # # #         "What is the Sustainable Farming Act?",
# # # #         ""  # Empty prompt to test validation
# # # #     ]

# # # #     for prompt in test_prompts:
# # # #         response = responder.generate_response(prompt)
# # # #         print(f"Prompt: {prompt}\nResponse: {response}\n{'-'*60}")


# # # # ai_model.py

# # # from dotenv import load_dotenv
# # # load_dotenv()  # Load environment variables from .env

# # # import os
# # # import logging
# # # import time
# # # from typing import Optional

# # # import requests

# # # # Configure logging
# # # LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# # # LOG_FORMAT = os.environ.get(
# # #     "LOG_FORMAT",
# # #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# # # )
# # # LOG_FILE = os.environ.get("LOG_FILE", "ai_model.log")

# # # logging.basicConfig(
# # #     level=LOG_LEVEL,
# # #     format=LOG_FORMAT,
# # #     handlers=[
# # #         logging.FileHandler(LOG_FILE),
# # #         logging.StreamHandler()
# # #     ]
# # # )
# # # logger = logging.getLogger(__name__)

# # # class OllamaResponder:
# # #     def __init__(
# # #         self,
# # #         model_name: Optional[str] = None,
# # #         base_url: str = 'http://127.0.0.1:11434',
# # #         max_retries: int = 3,
# # #         retry_delay: float = 2.0
# # #     ):
# # #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# # #         self.base_url = base_url
# # #         self.max_retries = max_retries
# # #         self.retry_delay = retry_delay

# # #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# # #     def generate_response(
# # #         self,
# # #         prompt: str,
# # #         max_length: int = 150,
# # #         temperature: float = 0.7,
# # #         stop_sequences: Optional[list] = None,
# # #         retries: int = 0
# # #     ) -> str:
# # #         try:
# # #             prompt = prompt.strip()
# # #             if not prompt:
# # #                 logger.warning("Empty prompt received.")
# # #                 return "Please provide a valid prompt."

# # #             logger.info(f"Generating response for prompt: {prompt[:30]}{'...' if len(prompt) > 30 else ''}")

# # #             # Prepare the payload for the Ollama API
# # #             payload = {
# # #                 "model": self.model_name,
# # #                 "prompt": prompt,
# # #                 "options": {
# # #                     "max_tokens": max_length,
# # #                     "temperature": temperature
# # #                 }
# # #             }

# # #             if stop_sequences:
# # #                 payload["options"]["stop"] = stop_sequences

# # #             # Send the request to the Ollama API
# # #             response = requests.post(
# # #                 f"{self.base_url}/api/generate",
# # #                 json=payload,
# # #                 stream=True,  # To handle streaming responses
# # #                 timeout=30  # Timeout after 30 seconds
# # #             )
# # #             response.raise_for_status()  # Raise an exception for HTTP errors

# # #             # Since Ollama streams responses, we need to handle streaming content
# # #             response_text = ""
# # #             for line in response.iter_lines():
# # #                 if line:
# # #                     line_data = line.decode('utf-8')
# # #                     logger.debug(f"Received line: {line_data}")
# # #                     if line_data.startswith("data: "):
# # #                         data = line_data[6:]
# # #                         if data == "[DONE]":
# # #                             break
# # #                         else:
# # #                             response_text += data

# # #             if not response_text:
# # #                 logger.warning("Received an empty response from the model.")
# # #                 return "Sorry, I couldn't generate a response."

# # #             logger.info("Response generated successfully.")
# # #             return response_text.strip()

# # #         except requests.exceptions.HTTPError as http_err:
# # #             logger.error(f"HTTP error occurred: {http_err} - URL: {response.url}")
# # #             return "Sorry, I encountered an HTTP error while generating the response."
# # #         except requests.exceptions.ConnectionError as conn_err:
# # #             logger.error(f"Connection error occurred: {conn_err}")
# # #             if retries < self.max_retries:
# # #                 wait = self.retry_delay * (2 ** retries)  # Exponential backoff
# # #                 logger.info(f"Retrying in {wait} seconds... (Attempt {retries + 1}/{self.max_retries})")
# # #                 time.sleep(wait)
# # #                 return self.generate_response(prompt, max_length, temperature, stop_sequences, retries + 1)
# # #             else:
# # #                 logger.error("Max retries exceeded. Unable to generate response.")
# # #                 return "Sorry, I couldn't process your request at this time."
# # #         except requests.exceptions.Timeout as timeout_err:
# # #             logger.error(f"Timeout error occurred: {timeout_err}")
# # #             return "Sorry, the request timed out while generating the response."
# # #         except requests.exceptions.RequestException as req_err:
# # #             logger.error(f"Request exception occurred: {req_err}")
# # #             return "Sorry, an error occurred while generating the response."
# # #         except Exception as e:
# # #             logger.error(f"An unexpected error occurred: {e}")
# # #             return "Sorry, I encountered an error while generating the response."

# # # if __name__ == "__main__":
# # #     # Example usage
# # #     try:
# # #         responder = OllamaResponder()
# # #     except Exception as e:
# # #         logger.critical(f"Cannot initialize OllamaResponder: {e}")
# # #         exit(1)

# # #     # Sample prompts for testing
# # #     test_prompts = [
# # #         "Explain the key points of the Agriculture Bill.",
# # #         "What is the Sustainable Farming Act?",
# # #         ""  # Empty prompt to test validation
# # #     ]

# # #     for prompt in test_prompts:
# # #         response = responder.generate_response(prompt)
# # #         print(f"Prompt: {prompt}\nResponse: {response}\n{'-'*60}")

# # # ai_model.py

# # from dotenv import load_dotenv
# # load_dotenv()  # Load environment variables from .env

# # import os
# # import logging
# # import time
# # from typing import Optional

# # import requests  # Ensure this library is installed: pip install requests

# # # Configure logging
# # LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# # LOG_FORMAT = os.environ.get(
# #     "LOG_FORMAT",
# #     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# # )
# # LOG_FILE = os.environ.get("LOG_FILE", "ai_model.log")

# # logging.basicConfig(
# #     level=LOG_LEVEL,
# #     format=LOG_FORMAT,
# #     handlers=[
# #         logging.FileHandler(LOG_FILE),
# #         logging.StreamHandler()
# #     ]
# # )
# # logger = logging.getLogger(__name__)

# # class OllamaResponder:
# #     def __init__(
# #         self,
# #         model_name: Optional[str] = None,
# #         base_url: str = 'http://127.0.0.1:11434',
# #         max_retries: int = 3,
# #         retry_delay: float = 2.0
# #     ):
# #         """
# #         Initialize the OllamaResponder.

# #         Args:
# #             model_name (Optional[str]): Name of the Ollama model to use.
# #                                          Defaults to the 'OLLAMA_MODEL_NAME' environment variable or 'llama3.2:latest'.
# #             base_url (str): Base URL for the Ollama API. Defaults to 'http://127.0.0.1:11434'.
# #             max_retries (int): Maximum number of retries for API requests. Defaults to 3.
# #             retry_delay (float): Initial delay between retries in seconds. Defaults to 2.0.
# #         """
# #         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
# #         self.base_url = base_url
# #         self.max_retries = max_retries
# #         self.retry_delay = retry_delay

# #         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

# #     def generate_response(
# #         self,
# #         prompt: str,
# #         max_length: int = 150,
# #         temperature: float = 0.7,
# #         stop_sequences: Optional[list] = None,
# #         retries: int = 0
# #     ) -> str:
# #         """
# #         Generate a response from the Ollama model based on the provided prompt.

# #         Args:
# #             prompt (str): The input prompt for the AI model.
# #             max_length (int): Maximum number of tokens in the response. Defaults to 150.
# #             temperature (float): Sampling temperature for response variability. Defaults to 0.7.
# #             stop_sequences (Optional[list]): Sequences where the AI should stop generating further tokens.
# #             retries (int): Current retry attempt. Used internally for recursion.

# #         Returns:
# #             str: The AI-generated response.
# #         """
# #         try:
# #             # Sanitize the prompt
# #             prompt = prompt.strip()
# #             if not prompt:
# #                 logger.warning("Empty prompt received.")
# #                 return "Please provide a valid prompt."

# #             logger.info(f"Generating response for prompt: {prompt[:30]}{'...' if len(prompt) > 30 else ''}")

# #             # Prepare the payload for the Ollama API
# #             payload = {
# #                 "model": self.model_name,
# #                 "prompt": prompt,
# #                 "options": {
# #                     "max_tokens": max_length,
# #                     "temperature": temperature
# #                 }
# #             }

# #             if stop_sequences:
# #                 payload["options"]["stop"] = stop_sequences

# #             # Send the request to the Ollama API
# #             response = requests.post(
# #                 f"{self.base_url}/api/generate",
# #                 json=payload,
# #                 stream=True,  # To handle streaming responses
# #                 timeout=30  # Timeout after 30 seconds
# #             )
# #             response.raise_for_status()  # Raise an exception for HTTP errors

# #             # Handle streaming responses
# #             response_text = ""
# #             for line in response.iter_lines():
# #                 if line:
# #                     line_data = line.decode('utf-8')
# #                     logger.debug(f"Received line: {line_data}")
# #                     if line_data.startswith("data: "):
# #                         data = line_data[6:]
# #                         if data == "[DONE]":
# #                             break
# #                         else:
# #                             response_text += data

# #             if not response_text:
# #                 logger.warning("Received an empty response from the model.")
# #                 return "Sorry, I couldn't generate a response."

# #             logger.info("Response generated successfully.")
# #             return response_text.strip()

# #         except requests.exceptions.HTTPError as http_err:
# #             logger.error(f"HTTP error occurred: {http_err} - URL: {response.url}")
# #             return "Sorry, I encountered an HTTP error while generating the response."
# #         except requests.exceptions.ConnectionError as conn_err:
# #             logger.error(f"Connection error occurred: {conn_err}")
# #             if retries < self.max_retries:
# #                 wait = self.retry_delay * (2 ** retries)  # Exponential backoff
# #                 logger.info(f"Retrying in {wait} seconds... (Attempt {retries + 1}/{self.max_retries})")
# #                 time.sleep(wait)
# #                 return self.generate_response(prompt, max_length, temperature, stop_sequences, retries + 1)
# #             else:
# #                 logger.error("Max retries exceeded. Unable to generate response.")
# #                 return "Sorry, I couldn't process your request at this time."
# #         except requests.exceptions.Timeout as timeout_err:
# #             logger.error(f"Timeout error occurred: {timeout_err}")
# #             return "Sorry, the request timed out while generating the response."
# #         except requests.exceptions.RequestException as req_err:
# #             logger.error(f"Request exception occurred: {req_err}")
# #             return "Sorry, an error occurred while generating the response."
# #         except Exception as e:
# #             logger.error(f"An unexpected error occurred: {e}")
# #             return "Sorry, I encountered an error while generating the response."

# # if __name__ == "__main__":
# #     # Example usage
# #     try:
# #         responder = OllamaResponder()
# #     except Exception as e:
# #         logger.critical(f"Cannot initialize OllamaResponder: {e}")
# #         exit(1)

# #     # Sample prompts for testing
# #     test_prompts = [
# #         "Explain the key points of the Agriculture Bill.",
# #         "What is the Sustainable Farming Act?",
# #         ""  # Empty prompt to test validation
# #     ]

# #     for prompt in test_prompts:
# #         response = responder.generate_response(prompt)
# #         print(f"Prompt: {prompt}\nResponse: {response}\n{'-'*60}")


# # ai_model.py

# from dotenv import load_dotenv
# load_dotenv()  # Load environment variables from .env

# import os
# import logging
# import time
# from typing import Optional, List

# import requests  # Ensure this library is installed: pip install requests

# # Configure logging
# LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
# LOG_FORMAT = os.environ.get(
#     "LOG_FORMAT",
#     "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
# )
# LOG_FILE = os.environ.get("LOG_FILE", "ai_model.log")

# logging.basicConfig(
#     level=LOG_LEVEL,
#     format=LOG_FORMAT,
#     handlers=[
#         logging.FileHandler(LOG_FILE),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger(__name__)


# class OllamaResponder:
#     """
#     A responder class that interacts with the Ollama AI model to generate responses based on prompts.
#     """

#     def __init__(
#         self,
#         model_name: Optional[str] = None,
#         base_url: str = 'http://127.0.0.1:11434',
#         max_retries: int = 3,
#         retry_delay: float = 2.0
#     ):
#         """
#         Initialize the OllamaResponder.

#         Args:
#             model_name (Optional[str]): Name of the Ollama model to use.
#                                          Defaults to the 'OLLAMA_MODEL_NAME' environment variable or 'llama3.2:latest'.
#             base_url (str): Base URL for the Ollama API. Defaults to 'http://127.0.0.1:11434'.
#             max_retries (int): Maximum number of retries for API requests. Defaults to 3.
#             retry_delay (float): Initial delay between retries in seconds. Defaults to 2.0.
#         """
#         self.model_name = model_name or os.environ.get("OLLAMA_MODEL_NAME", "llama3.2:latest")
#         self.base_url = base_url
#         self.max_retries = max_retries
#         self.retry_delay = retry_delay

#         logger.info(f"OllamaResponder initialized with model: {self.model_name} at {self.base_url}")

#     def generate_response(
#         self,
#         prompt: str,
#         max_length: int = 150,
#         temperature: float = 0.7,
#         stop_sequences: Optional[List[str]] = None,
#         retries: int = 0
#     ) -> str:
#         """
#         Generate a response from the Ollama model based on the provided prompt.

#         Args:
#             prompt (str): The input prompt for the AI model.
#             max_length (int): Maximum number of tokens in the response. Defaults to 150.
#             temperature (float): Sampling temperature for response variability. Defaults to 0.7.
#             stop_sequences (Optional[List[str]]): Sequences where the AI should stop generating further tokens.
#             retries (int): Current retry attempt. Used internally for recursion.

#         Returns:
#             str: The AI-generated response.
#         """
#         try:
#             # Sanitize the prompt
#             prompt = prompt.strip()
#             if not prompt:
#                 logger.warning("Empty prompt received.")
#                 return "Please provide a valid prompt."

#             logger.info(f"Generating response for prompt: {prompt[:30]}{'...' if len(prompt) > 30 else ''}")

#             # Prepare the payload for the Ollama API
#             payload = {
#                 "model": self.model_name,
#                 "prompt": prompt,
#                 "options": {
#                     "max_tokens": max_length,
#                     "temperature": temperature
#                 }
#             }

#             if stop_sequences:
#                 payload["options"]["stop"] = stop_sequences

#             # Send the request to the Ollama API
#             response = requests.post(
#                 f"{self.base_url}/api/generate",
#                 json=payload,
#                 stream=True,  # To handle streaming responses
#                 timeout=30  # Timeout after 30 seconds
#             )
#             response.raise_for_status()  # Raise an exception for HTTP errors

#             # Handle streaming responses
#             response_text = ""
#             for line in response.iter_lines():
#                 if line:
#                     line_data = line.decode('utf-8')
#                     logger.debug(f"Received line: {line_data}")
#                     if line_data.startswith("data: "):
#                         data = line_data[6:]
#                         if data == "[DONE]":
#                             break
#                         else:
#                             response_text += data

#             if not response_text:
#                 logger.warning("Received an empty response from the model.")
#                 return "Sorry, I couldn't generate a response."

#             logger.info("Response generated successfully.")
#             return response_text.strip()

#         except requests.exceptions.HTTPError as http_err:
#             logger.error(f"HTTP error occurred: {http_err} - URL: {response.url}")
#             return "Sorry, I encountered an HTTP error while generating the response."
#         except requests.exceptions.ConnectionError as conn_err:
#             logger.error(f"Connection error occurred: {conn_err}")
#             if retries < self.max_retries:
#                 wait = self.retry_delay * (2 ** retries)  # Exponential backoff
#                 logger.info(f"Retrying in {wait} seconds... (Attempt {retries + 1}/{self.max_retries})")
#                 time.sleep(wait)
#                 return self.generate_response(prompt, max_length, temperature, stop_sequences, retries + 1)
#             else:
#                 logger.error("Max retries exceeded. Unable to generate response.")
#                 return "Sorry, I couldn't process your request at this time."
#         except requests.exceptions.Timeout as timeout_err:
#             logger.error(f"Timeout error occurred: {timeout_err}")
#             return "Sorry, the request timed out while generating the response."
#         except requests.exceptions.RequestException as req_err:
#             logger.error(f"Request exception occurred: {req_err}")
#             return "Sorry, an error occurred while generating the response."
#         except Exception as e:
#             logger.error(f"An unexpected error occurred: {e}")
#             return "Sorry, I encountered an error while generating the response."


# if __name__ == "__main__":
#     # Example usage
#     try:
#         responder = OllamaResponder()
#     except Exception as e:
#         logger.critical(f"Cannot initialize OllamaResponder: {e}")
#         exit(1)

#     # Sample prompts for testing
#     test_prompts = [
#         "Explain the key points of the Agriculture Bill.",
#         "What is the Sustainable Farming Act?",
#         ""  # Empty prompt to test validation
#     ]

#     for prompt in test_prompts:
#         response = responder.generate_response(prompt)
#         print(f"Prompt: {prompt}\nResponse: {response}\n{'-'*60}")
