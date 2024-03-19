import json


class Video:
    def __init__(self, title: str, description: str, subject: str, script: str, language: str, video_path: str):
        self.title = title
        self.description = description
        self.subject = subject
        self.script = script
        self.language = language
        self.video_path = video_path

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "subject": self.subject,
            "script": self.script,
            "language": self.language,
            "video_path": self.video_path
        }

def save_videos_to_json(video_list):
    with open("videos.json", 'w') as file:
        json.dump([video.to_dict() for video in video_list], file, indent=4)

def load_videos_from_json():
    try:
        with open("videos.json", 'r') as file:
            videos_data = json.load(file)
            return [Video(**video_data) for video_data in videos_data]
    except:
        return []
