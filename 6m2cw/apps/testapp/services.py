from .tasks import send_welcome_email_task


def register_user(email):
    send_welcome_email_task.delay(email)
    return {"message": "Registration successful. Welcome email is being sent."}