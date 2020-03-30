from unittest import TestCase


class TestParser(TestCase):
    def test_rbc(self):
        assert self.test_rbc() != None


class TestParser(TestCase):
    def test_vedomosti(self):
        assert self.fail() != None


class TestParser(TestCase):
    def test_kommersant(self):
        assert self.fail() != None


class TestParser(TestCase):
    def test_yandex(self):
        assert  self.yandex() != None
