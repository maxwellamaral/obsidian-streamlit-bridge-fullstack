from fastapi import FastAPI, HTTPException  
from fastapi.middleware.cors import CORSMiddleware  
import subprocess  

app = FastAPI()  

app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  

@app.post("/generate")  
async def generate_streamlit_app(request: dict):  
    content = request.get("content", "")  
    try:  
        with open("temp_app.py", "w") as f:  
            f.write(convert_md_to_streamlit(content))  
        subprocess.Popen(["streamlit", "run", "temp_app.py"])  
        return {"status": "success"}  
    except Exception as e:  
        raise HTTPException(status_code=500, detail=str(e))  

def convert_md_to_streamlit(md_content: str) -> str:  
    streamlit_code = "import streamlit as st\n"  
    in_code_block = False  

    for line in md_content.split('\n'):  
        if line.strip().startswith('```python'):  
            in_code_block = True  
            continue  
        elif line.strip().startswith('```'):  
            in_code_block = False  
            continue  

        if in_code_block:  
            streamlit_code += f"{line}\n"  
        else:  
            streamlit_code += f'st.markdown("""{line}""")\n'  

    return streamlit_code  