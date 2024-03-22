import os
from tiktok_uploader import tiktok

def upload_video_from_json(data):
    print("\033[32m Starting Uploading process...\033[0m")
    # Pre-made user credentials
    pre_made_user = "bob"
    
    # Login using pre-made user
    tiktok.login(pre_made_user)
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    # Prepare variables for video upload
    video_path = os.path.join(script_dir, data["video_path"])
    title = data["title"]
    schedule_time = data.get("schedule_time", 0) #in seconds, up to 10days in advance, min is 20mins
    comment = data.get("comment", 1) #allow
    duet = data.get("duet", 0)
    stitch = data.get("stitch", 0)
    visibility = data.get("visibility", 0)
    brandorganic = data.get("brandorganic", 0)
    brandcontent = data.get("brandcontent", 0)
    ailabel = data.get("ailabel", 0)
    proxy = data.get("proxy", "")

    # Upload video
    tiktok.upload_video(pre_made_user, video_path, title, schedule_time, comment, duet, stitch, visibility, brandorganic, brandcontent, ailabel, proxy)

# upload_video_from_json({"video_path": "out/jokes_111/video.mp4", "title": "my new joke"})