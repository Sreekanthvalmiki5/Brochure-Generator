import gradio as gr
import os
from models import get_openrouter_model
from scrapper import fetch_website_contents

class Day2:
    def __init__(self):
        self.router=get_openrouter_model()
        self.name="day2"
        self.system_message="""You are an assistant that analyzes the contents of a company website landing page
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks."""
        # self.system_message="You are a helpful assistant for generating brochures. You will be given a topic and you will generate a brochure for that topic. The brochure should be in markdown format and should be concise and informative. The brochure should include a title, a description, and a list of features or benefits. The brochure should be no more than 1000 words."
    def message_openrouter(self, prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="gpt-oss-20b",messages=messages)
        return response.choices[0].message.content
    def generate_chat(self):
        message_input=gr.Textbox(label="Type Your Message",info="Ask Anything",lines=7)
        message_output=gr.Markdown(label="Response")
        view=gr.Interface(fn=self.message_openrouter,title="Enter a Message",inputs=message_input,outputs=message_output,examples=["Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",])
        view.launch()
        
    def stream_gpt(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="gpt-oss-20b",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or " "
            yield result
    def generate_stream_chat(self):
        message_input=gr.Textbox(label="Type Your Message",info="Ask Anything",lines=7)
        message_output=gr.Markdown(label="Response")
        view=gr.Interface(fn=self.stream_gpt,title="Enter a Message",inputs=message_input,outputs=message_output,examples=["Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",])
        view.launch()
    
    def stream_gemma(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="gemma-4-26b-a4b-it",messages=messages,stream=True)
        result=""
        for chunck in response:
            result+=chunck.choices[0].delta.content or ""
            yield result
    def stream_liquid(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="liquid/lfm-2.5-1.2b-instruct",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
    def stream_meta(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="llama-3.2-3b-instruct",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
            
    def stream_nex(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="nex-n2-pro",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
    def stream_hermes(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="hermes-3-llama-3.1-405b",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
    def stream_nvidia(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="llama-nemotron-embed-vl-1b-v2",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
    def stream_poolside(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="laguna-m.1",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
    def stream_qwen(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="qwen3-coder",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
    def stream_venice(self,prompt):
        messages=[{"role":"system","content":self.system_message},{"role":"user","content":prompt}]
        response=self.router.chat.completions.create(model="dolphin-mistral-24b-venice-edition",messages=messages,stream=True)
        result=""
        for chunk in response:
            result+=chunk.choices[0].delta.content or ""
            yield result
    def select_stream_model(self,prompt,model):
        if model=="CHATGPT":
            yield from self.stream_gpt(prompt)
        elif model=="GEMMA":
            yield from self.stream_gemma(prompt)
        elif model=="LIQUID":
            yield from self.stream_liquid(prompt)
        elif model=="META":
            yield from self.stream_meta(prompt)
        elif model=="NEX":
            yield from self.stream_nex(prompt)
        elif model=="HERMES":
            yield from self.stream_hermes(prompt)
        elif model=="NVIDIA":
            yield from self.stream_nvidia(prompt)
        elif model=="POOLSIDE":
            yield from self.stream_poolside(prompt)
        elif model=="QWEN":
            yield from self.stream_qwen(prompt)
        elif model=="VENICE":
            yield from self.stream_venice(prompt)
    def stream_all_models(self):
        message_input=gr.Textbox(label="Type Your Message",info="Ask Anything",lines=7)
        message_output=gr.Markdown(label="Response")
        model_selector=gr.Dropdown(label="Select Model",choices=["CHATGPT","LIQUID","GEMMA","META"])
        view=gr.Interface(fn=self.select_stream_model,title="Enter a Message",inputs=[message_input,model_selector],outputs=message_output)
        view.launch()
    def stream_brochure(self,company_name,url,model):
        yield
        prompt=f"Generate a brochure for {company_name} Here is the langing page of the company:"
        prompt+=fetch_website_contents(url)
        if model=="CHATGPT":
            result= self.stream_gpt(prompt)
        elif model=="GEMMA":
            result= self.stream_gemma(prompt)
        elif model=="META":
            result= self.stream_meta(prompt)
        else:
            raise ValueError("Unknown model")
        yield from result
    def generate_brochure(self):
        company_name=gr.Textbox(label="Company Name")
        url=gr.Textbox(label="Company URL")
        model_selector=gr.Dropdown(label="Select Model",choices=["CHATGPT","LIQUID","GEMMA","META"])
        message_output=gr.Markdown(label="Brochure")
        view=gr.Interface(fn=self.stream_brochure,title="Generate Brochure",inputs=[company_name,url,model_selector],outputs=message_output,examples=[
            ["Hugging Face", "https://huggingface.co", "GPT"],
            ["DeepMind", "https://deepmind.com", "GEMMA"],
            ["OpenAI", "https://openai.com", "META"],
        ], )
        view.launch()
      
        
        
    
if __name__ =="__main__":
    day2=Day2()
    # day2.stream_all_models()
    # day2.generate_chat()
    # day2.generate_stream_chat()
    day2.generate_brochure()