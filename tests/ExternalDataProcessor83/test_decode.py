import os
import sys
import json
import shutil
import unittest
from v8unpack.unittest_helper import HelperTestDecode
from v8unpack import helper


class TestDecode(HelperTestDecode):
    def setUp(self):
        super(TestDecode, self).setUp()
        self.src_dir = os.path.join(sys.path[0])
        self.src_file = 'ВнешняяОбработка1.epf'
        self.test_dir = os.path.join(sys.path[0], 'tmp')
        # with open(os.path.join(self.test_dir,'index.json'), 'r', encoding='utf-8') as f:
        #     self.index = json.load(f)

        # self.version = '83'
        self.result = {
            'count_root_files_stage1': 14,
            'count_root_files_stage3': 7,
            'count_root_files_stage4': 7,
            'count_forms_files': 7,
            'count_templates_files': 2
        }
        self.init()
        pass

    def test_01_decode_stage1(self):
        super(TestDecode, self).decode_stage1()

    def test_02_decode_stage2(self):
        super(TestDecode, self).decode_stage2()

    def test_03_decode_stage3(self):
        super(TestDecode, self).decode_stage3()
        self.assert_external_data_processor_decode_stage3()

    def test_04_decode_stage4(self):
        shutil.rmtree(os.path.join(sys.path[0], 'decodeCodeSubmodule'), ignore_errors=True)
        super(TestDecode, self).decode_stage4()

    def test_05_encode_stage4(self):
        super(TestDecode, self).encode_stage4()

    def test_06_encode_stage3(self):
        super(TestDecode, self).encode_stage3()

    def test_07_encode_stage2(self):
        super(TestDecode, self).encode_stage2()

    def test_08_encode_stage1(self):
        super(TestDecode, self).encode_stage1()

    @unittest.skip
    def test_extract(self):
        from v8unpack.v8unpack import extract, build
        extract('ВнешняяОбработка1.epf', 'src')
        build('src', 'ВнешняяОбработка.build.epf')

    @unittest.skip
    def test_create_index(self):
        helper.create_index(os.path.join(sys.path[0], 'tmp', 'index.json'), self.decode_dir_stage4,
                            'decodeCodeSubmodule')


if __name__ == '__main__':
    unittest.main()
