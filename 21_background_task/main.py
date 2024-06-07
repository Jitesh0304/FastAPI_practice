from fastapi import FastAPI, BackgroundTasks, Depends
import time


app = FastAPI()


def write_log(message: str):
    with open('logs.txt', 'w') as log:
        log.write(message)


def get_query(background_task: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query {q}"
        background_task.add_task(write_log, message)
    return q


@app.post("/send-email/{email}")
async def send_notification(email: str, background_task: BackgroundTasks, q: str = Depends(get_query)):
    background_task.add_task(write_notification, email=email, message="your account has been created")
    return {"message": "Notification sent in the background"}


def write_notification(email: str, message=""):
    time.sleep(5)
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_task: BackgroundTasks):
    background_task.add_task(write_notification, email=email, message="your account has been created")
    return {"message": "Notification sent in the background"}


