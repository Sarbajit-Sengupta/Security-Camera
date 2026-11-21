from pathlib import Path


def monitor(cv2, alarm):
    cam = cv2.VideoCapture(0)
    try:
        if not cam.isOpened():
            raise RuntimeError("Unable to open camera 0")
        while True:
            ok1, frame1 = cam.read()
            if not ok1 or frame1 is None:
                break
            ok2, frame2 = cam.read()
            if not ok2 or frame2 is None:
                break
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) < 5000:
                    continue
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
                alarm()
            cv2.imshow('Security Cam', frame1)
            if cv2.waitKey(5) & 0xff == ord('q'):
                break
    finally:
        cam.release()
        cv2.destroyAllWindows()


def main():
    import cv2
    import winsound
    sound = str(Path(__file__).with_name('alert (1).wav'))
    monitor(cv2, lambda: winsound.PlaySound(sound, winsound.SND_FILENAME | winsound.SND_ASYNC))


if __name__ == '__main__':
    main()
