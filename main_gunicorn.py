#########################
# File main_gunicorn.py #
#########################

from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="89.32.250.198", port=8000)
