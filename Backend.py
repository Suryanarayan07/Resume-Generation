from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import ollama
import json

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/enhance-resume")
async def enhance_resume(request: Request):
    try:
        request_data = await request.json()

        # Extract style and creative control
        style = request_data.get("style", "professional")
        creative_control = request_data.get("creative_control", "medium")

        # Creative control logic
        enhancement_instruction = {
            "low": "Make minimal formatting changes",
            "high": "Significantly enhance content with achievements"
        }.get(creative_control, "Balance between accuracy and enhancement")

        # Build prompt
        prompt = f"""
        Create a {style}-style resume from this data with these guidelines:
        1. Maintain all factual accuracy
        2. {enhancement_instruction}
        3. Add relevant metrics to experience bullet points
        4. Keep language professional but engaging

        Input Data:
        {json.dumps(request_data, indent=2)}
        """

        # Generate resume with Ollama
        response = ollama.generate(
            model='gemma',
            prompt=prompt,
            options={'temperature': 0.3 if creative_control == 'low' else 0.7}
        )

        return {"resume": response['response']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
