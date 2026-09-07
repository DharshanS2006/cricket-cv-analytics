from pathlib import Path

import cv2


def extract_frames(
    video_path: str,
    output_dir: str,
    interval: int = 30,
) -> int:
    """
    Extract frames from a video at a fixed frame interval.

    Parameters
    ----------
    video_path : str
        Path to the input cricket video.

    output_dir : str
        Directory where extracted frames will be saved.

    interval : int
        Save one frame every `interval` frames.

    Returns
    -------
    int
        Number of frames successfully saved.
    """

    video = Path(video_path)
    output = Path(output_dir)

    if not video.exists():
        raise FileNotFoundError(f"Video not found: {video}")

    output.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video))

    if not capture.isOpened():
        raise RuntimeError(f"Unable to open video: {video}")

    frame_number = 0
    saved_count = 0

    while True:
        success, frame = capture.read()

        if not success:
            break

        if frame_number % interval == 0:
            frame_name = output / f"frame_{frame_number:06d}.jpg"

            cv2.imwrite(str(frame_name), frame)

            saved_count += 1

        frame_number += 1

    capture.release()

    print("========================================")
    print("       CRICKET CV ANALYTICS")
    print("          FRAME EXTRACTION")
    print("========================================")
    print(f"Input video : {video.name}")
    print(f"Frames read : {frame_number}")
    print(f"Frames saved: {saved_count}")
    print(f"Output      : {output}")
    print("========================================")

    return saved_count


if __name__ == "__main__":
    print("Cricket CV Analytics - Frame Extractor")
    print("Frame extractor module loaded successfully.")