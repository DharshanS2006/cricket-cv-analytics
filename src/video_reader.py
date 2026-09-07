from pathlib import Path
import cv2

def inspect_video(video_path: str) -> None:
     """
    Inspect and display basic information about a video.

    Parameters
    ----------
    video_path : str
        Path to the input video.
    """
     path = Path(video_path)

     if not path.exists():
          raise FileNotFoundError(f"Video not found: {path}")

     capture = cv2.VideoCapture(str(path))

     if not capture.isOpened():
          raise RuntimeError(f"Unable to open video: {path}")

     frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
     fps = capture.get(cv2.CAP_PROP_FPS)
     width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
     height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

     duration = frame_count / fps if fps > 0 else 0

     print("========================================")
     print("       CRICKET CV ANALYTICS")
     print("          VIDEO INFORMATION")
     print("========================================")
     print(f"File       : {path.name}")
     print(f"Resolution : {width} x {height}")
     print(f"FPS        : {fps:.2f}")
     print(f"Frames     : {frame_count}")
     print(f"Duration   : {duration:.2f} seconds")
     print("========================================")

     capture.release()

if __name__ == "__main__":
     print("Cricket CV Analytics - Video Reader")
     print("Video reader module loaded successfully.")

