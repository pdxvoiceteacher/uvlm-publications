"""Video stream adapter for multimodal telemetry ingestion."""

import cv2


def ingest_video_stream(source=0):
    """Yield frames from a video capture source."""
    cap = cv2.VideoCapture(source)

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            yield frame
    finally:
        cap.release()
