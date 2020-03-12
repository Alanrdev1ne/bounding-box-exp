#!/usr/bin/python3

import cv2
from collections import defaultdict


class VideoFeed:

    def __init__(self, cam_id):

        self.cam_id = cam_id
        self.cam = cv2.VideoCapture(0)

        self.frame_h = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_w = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))

        # Will be set during runtime
        self.static_background = None

    def cam_loop(self):
        ret, frame = self.cam.read()
        while ret:
            cv2.imshow("Before", frame)
            diff = cv2.absdiff(self.static_background, frame)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(src=gray, ksize=(5, 5), sigmaX=0)

            _, thresh = cv2.threshold(src=blur,
                                      thresh=70,
                                      maxval=255,
                                      type=cv2.THRESH_BINARY)

            dilated = cv2.dilate(thresh, kernel=None, iterations=3)

            contours, _ = cv2.findContours(image=dilated,
                                           mode=cv2.RETR_TREE,
                                           method=cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                if cv2.contourArea(contour) < 900:
                    continue

                cv2.rectangle(frame,
                              pt1=(x, y),
                              pt2=(x + w, y + h),
                              color=(255, 0, 0),
                              thickness=2)

                cv2.circle(frame,
                           center=(x + w // 2, y + h // 2),
                           radius=5,
                           color=(255, 0, 0),
                           thickness=2)

            cv2.imshow("After", frame)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

            ret, frame = self.cam.read()

    def __del__(self):
        """Destructer Method"""
        cv2.destroyAllWindows()
        self.cam.release()


def main():
    vf = VideoFeed(0)
    input("Setup camera backdrop and press 'Enter' to set...")
    _, frame = vf.cam.read()
    vf.static_background = frame
    vf.cam_loop()


if __name__ == "__main__":
    main()
