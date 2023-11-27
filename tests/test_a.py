import unittest
from main import VA

target = __import__("main.py")
cmd_relay = target.VaaniVA.cmd_relay


class test_vaani_va(unittest.TestCase):
    def test_func(self):
        pass

    def test_cmd_relay(self):
        list_name = []
        inp_str = 'input_str'

        # res1 = VaaniVA.cmd_relay(list_name, inp_str)
        res1 = VA.cmd_relay(list_name, inp_str)
        self.assertEquals(res1, self.test_func())


if __name__ == '__main__':
    obj1c = test_vaani_va()
    obj1c.test_cmd_relay()
