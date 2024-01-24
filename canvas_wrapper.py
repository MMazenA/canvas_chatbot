

API_URL = "https://canvas.wayne.edu"
API_KEY = os.environ["CANVAS_TOKEN"]
canvas = Canvas(API_URL, API_KEY)
class CanvasWrapper():
    def __init__(self,api_url,api_key) -> None:
        self.canvas = Canvas(API_URL, API_KEY)
        