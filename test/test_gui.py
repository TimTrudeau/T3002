import unittest
import tkinter as tk
import Page_GUI as pdrobot
import Page_GUI as pds


#@pytest.fixture(autouse=True)
def setup():
    root = tk.Tk()
    # Creates a toplevel widget.
    _top = pdrobot.Toplevel1(root)
    pds.main(_top)
    return _top
    #yield _top
    #root.destroy()


class MyTestCase(unittest.TestCase):
    def test_cb_buttonHome(self):
        top = setup()
        pds.cb_buttonHome('LIN')
        val = top.absolutePos.get()
        self.assertEqual('0', val)
        pds.cb_buttonHome('ROT')
        val = top.absoluteRot.get()
        self.assertEqual('0', val)

    def test_cb_buttonLin(self):
        top = setup()
        pds.cb_buttonLin(20)
        val = top.absolutePos.get()
        self.assertEqual('20', val)
        pds.cb_buttonLin(-30)
        val = top.absolutePos.get()
        self.assertEqual('-10', val)

    def test_cb_buttonRot(self):
        top = setup()
        pds.cb_buttonRot(20)
        val = top.absoluteRot.get()
        self.assertEqual('20', val)
        pds.cb_buttonRot(-30)
        val = top.absoluteRot.get()
        self.assertEqual('-10', val)

    def test_cb_openFile(self):
        top = setup()
        self.assertTrue("TODO test_cb_openFile")

    def test_cb_run_program(self):
        top = setup()
        self.assertTrue("TODO test_cb_run_program")

    def test_cb_cancel_file(self):
        top = setup()
        self.assertTrue("TODO test_cb_cancel_file")

    def test_cb_scaleLinSpeed(self):
        top = setup()
        self.assertTrue("TODO test_cb_scaleLinSpeed")

    def test_cb_scaleRotSpeed(self):
        top = setup()
        self.assertTrue("TODO test_cb_scaleRotSpeed")

    def test_cb_step_program(self):
        top = setup()
        self.assertTrue("TODO test_cb_step_program")

    def test_cb_stop(self):
        top = setup()
        self.assertTrue("TODO test_cb_stop")

    def test_cb_go(self):
        top = setup()
        top.set1_pos.set('10')
        top.set1_rot.set('-200')
        pds.cb_go(1, top.set1_pos, top.set1_rot)
        self.assertEqual('10', top.absolutePos.get())
        self.assertEqual('-200', top.absoluteRot.get())

    def test_cb_waypoint(self):
        top = setup()
        top.absolutePos.set(10)
        top.absoluteRot.set(20)
        pds.cb_waypoint(1)
        self.assertEqual('10', top.set1_pos.get())
        self.assertEqual('20', top.set1_rot.get())

        pds.cb_waypoint(2)
        self.assertEqual('10', top.set2_pos.get())
        self.assertEqual('20', top.set2_rot.get())

        pds.cb_waypoint(3)
        self.assertEqual('10', top.set3_pos.get())
        self.assertEqual('20', top.set3_rot.get())

        pds.cb_waypoint(4)
        self.assertEqual('10', top.set4_pos.get())
        self.assertEqual('20', top.set4_rot.get())


if __name__ == '__main__':
    unittest.main()
