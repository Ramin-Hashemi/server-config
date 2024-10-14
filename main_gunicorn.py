#########################
# File main_gunicorn.py #
#########################

from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="00.00.00.00", port=8000)
