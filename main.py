from __future__ import annotations

import argparse
from typing import Any, Final

import cv2
import mediapipe as mp
import numpy as np


# ── Config ────────────────────────────────────────────────────────────────────
BLUR_KERNEL_SIZE: Final = (51, 51)
BLUR_SIGMA: Final = 12
PEACE_FRAMES_TO_ENABLE: Final = 3
ABSENT_FRAMES_TO_DISABLE: Final = 5
INFERENCE_WIDTH: Final = 360
TEXT_LABEL: Final = "FOTO KITA BLUR"
TEXT_POSITION: Final = (12, 32)


# ── Peace-sign detection ──────────────────────────────────────────────────────
def is_finger_extended(landmarks: Any, tip_id: int, pip_id: int) -> bool:
    return landmarks.landmark[tip_id].y < landmarks.landmark[pip_id].y


def is_finger_folded(landmarks: Any, tip_id: int, pip_id: int) -> bool:
    return landmarks.landmark[tip_id].y > landmarks.landmark[pip_id].y


def is_peace_sign(landmarks: Any) -> bool:
    return (
        is_finger_extended(landmarks, 8, 6)
        and is_finger_extended(landmarks, 12, 10)
        and is_finger_folded(landmarks, 16, 14)
        and is_finger_folded(landmarks, 20, 18)
    )


def update_blur_state(
    peace_detected: bool,
    blur_enabled: bool,
    present_count: int,
    absent_count: int,
) -> tuple[bool, int, int]:
    if peace_detected:
        present_count += 1
        absent_count = 0
    else:
        absent_count += 1
        present_count = 0
    if present_count >= PEACE_FRAMES_TO_ENABLE:
        blur_enabled = True
    if absent_count >= ABSENT_FRAMES_TO_DISABLE:
        blur_enabled = False
    return blur_enabled, present_count, absent_count


# ── Main loop ─────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Peace-sign webcam blur — minimal.")
    parser.add_argument("--camera", type=int, default=0, help="camera index (0=built-in, 1=external)")
    parser.add_argument("--width", type=int, default=640, help="capture width")
    parser.add_argument("--height", type=int, default=480, help="capture height")
    args = parser.parse_args()

    hands_detector = mp.solutions.hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        model_complexity=0,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.5,
    )
    capture = cv2.VideoCapture(args.camera)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    if not capture.isOpened():
        print(f"Error: cannot open camera index {args.camera}. Try --camera 1 or --camera 2.")
        return

    blur_enabled = False
    present_count = 0
    absent_count = 0

    print("Camera:", args.camera, "| Resolution:", args.width, "x", args.height)
    print("Press 'q' to quit, 'c' to cycle camera.")

    with hands_detector:
        while capture.isOpened():
            success, frame = capture.read()
            if not success:
                break

            height, width = frame.shape[:2]

            # Downscale for MediaPipe inference
            scale = INFERENCE_WIDTH / width if width > INFERENCE_WIDTH else 1.0
            if scale < 1.0:
                small = cv2.resize(frame, (INFERENCE_WIDTH, int(height * scale)), interpolation=cv2.INTER_AREA)
            else:
                small = frame
            rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)
            result = hands_detector.process(rgb_small)

            hands = result.multi_hand_landmarks or []
            peace_detected = any(is_peace_sign(h) for h in hands)
            blur_enabled, present_count, absent_count = update_blur_state(
                peace_detected, blur_enabled, present_count, absent_count
            )

            display_frame = frame
            if blur_enabled:
                display_frame = cv2.GaussianBlur(frame, BLUR_KERNEL_SIZE, BLUR_SIGMA)
                cv2.putText(
                    display_frame,
                    TEXT_LABEL,
                    TEXT_POSITION,
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.8,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

            cv2.imshow("Foto Kita Blur", display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("c"):
                next_cam = args.camera + 1
                capture.release()
                capture = cv2.VideoCapture(next_cam)
                if not capture.isOpened():
                    print(f"Camera {next_cam} not available, reverting to {args.camera}")
                    capture = cv2.VideoCapture(args.camera)
                else:
                    print(f"Switched to camera {next_cam}")
                    args.camera = next_cam
                capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
                capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)

    capture.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
