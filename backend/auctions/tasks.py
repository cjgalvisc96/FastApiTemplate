from backend.config import app_celery


@app_celery.task(name="send_email")
def send_email():
    print("*" * 10)
    print("Email sent")
    print("*" * 10)
