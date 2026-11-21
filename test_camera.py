import unittest
from unittest.mock import Mock
from main import monitor


class CameraTests(unittest.TestCase):
    def test_failed_frame_reads_do_not_process_missing_images(self):
        for reads in [[(False, None)], [(True, object()), (False, None)]]:
            camera, cv = Mock(), Mock()
            camera.isOpened.return_value = True
            camera.read.side_effect = reads
            cv.VideoCapture.return_value = camera
            alarm = Mock()
            monitor(cv, alarm)
            cv.absdiff.assert_not_called()
            alarm.assert_not_called()
            camera.release.assert_called_once()
            cv.destroyAllWindows.assert_called_once()

    def test_processing_exception_releases_camera(self):
        camera, cv = Mock(), Mock()
        camera.isOpened.return_value = True
        camera.read.return_value = (True, object())
        cv.VideoCapture.return_value = camera
        cv.absdiff.side_effect = RuntimeError('injected')
        with self.assertRaises(RuntimeError):
            monitor(cv, Mock())
        camera.release.assert_called_once()
        cv.destroyAllWindows.assert_called_once()

    def test_unavailable_camera(self):
        cv = Mock()
        cv.VideoCapture.return_value.isOpened.return_value = False
        with self.assertRaisesRegex(RuntimeError, 'Unable to open'):
            monitor(cv, Mock())
        cv.VideoCapture.return_value.release.assert_called_once()


if __name__ == '__main__':
    unittest.main()
