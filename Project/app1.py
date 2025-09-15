# from fastapi import FastAPI
# from pydantic import BaseModel
# import dep_classification  # 👈 your original code file

# app = FastAPI()

# # Define request body
# class Complaint(BaseModel):
#     text: str

# @app.get("/")
# def home():
#     return {"message": "Complaint Classification API is running 🚀"}

# @app.post("/classify")
# def classify_complaint(complaint: Complaint): 
#     """Expose your entire code through an API endpoint"""

#     # Run your original classification functions
#     ml_dept =dep_classification.predict_dept(complaint.text)
#     keywords =dep_classification.sentence_classification(complaint.text)
#     keyword_dept =dep_classification.classify_dept(keywords)

#     result = {
#         "input": complaint.text,
#         "ml_dept": ml_dept,
#         "keyword_dept": keyword_dept
#     }

#     if ml_dept == keyword_dept:
#         result["final_department"] = ml_dept
#     else:
#         result["final_department"] = f"Conflict: {ml_dept} vs {keyword_dept}"

#     return result


from fastapi import FastAPI
import app  # 👈 your original code file

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Complaint Classification API is running 🚀"}

@app.get("/classify")
def classify_complaint(q: str):   # 👈 take text from query ?q=...
    """Expose your entire code through an API endpoint"""

    # Run your original classification functions
    ml_dept = app.predict(q)
    keywords = app.sentence_classification(q)
    keyword_dept = app.classify_dept(keywords)

    result = {
        "input": q,
        "ml_dept": ml_dept,
        "keyword_dept": keyword_dept
    }

    if ml_dept == keyword_dept:
        result["final_department"] = ml_dept
    else:
        result["final_department"] = f"Conflict: {ml_dept} vs {keyword_dept}"

    return result
