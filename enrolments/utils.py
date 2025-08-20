import uuid

def generate_jitsi_link(session_title):
    unique_id = str(uuid.uuid4())[:8]
    room_name = f"{session_title.replace(' ', '')}_{unique_id}"
    return f"https://meet.jit.si/{room_name}"