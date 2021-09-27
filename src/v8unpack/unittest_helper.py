import os
import logging
from .container_reader import extract
from .container_writer import build
from .json_container_decoder import json_decode, json_encode
from .decoder import decode, encode
from .file_organizer import FileOrganizer
from .json_container_decoder import JsonContainerDecoder
from . import helper
import unittest


# os.environ['PYTHONTRACEMALLOC'] = '1'


class HelperTestDecode(unittest.TestCase):
    pool = None

    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.pool = helper.get_pool()
    #     # cls.maxDiff = None
    #
    # @classmethod
    # def tearDownClass(cls) -> None:
    #     helper.close_pool(cls.pool)

    def setUp(self) -> None:
        self.src_dir = ''  # абсолютный путь до папки с исходным файлом
        self.src_file = ''  # имя исходного файла
        self.test_dir = ''  # абсолютный путь до временной папки c файлами промежуточных стадий
        self.result = None
        self.version = '83'
        self.index = None

    def init(self):
        os.makedirs(self.test_dir, exist_ok=True)

        self.decode_dir_stage0 = self.get_decode_folder(0)
        self.decode_dir_stage2 = self.get_decode_folder(2)
        self.decode_dir_stage1 = self.get_decode_folder(1)
        self.decode_dir_stage2 = self.get_decode_folder(2)
        self.decode_dir_stage3 = self.get_decode_folder(3)
        self.decode_dir_stage4 = self.get_decode_folder(4)

        self.encode_dir_stage0 = self.get_encode_folder(0)
        self.encode_dir_stage1 = self.get_encode_folder(1)
        self.encode_dir_stage2 = self.get_encode_folder(2)
        self.encode_dir_stage3 = self.get_encode_folder(3)

        pass

    def get_decode_folder(self, stage):
        return os.path.join(self.test_dir, f'decode_stage_{stage}')

    def get_encode_folder(self, stage):
        return os.path.join(self.test_dir, f'encode_stage_{stage}')

    def decode_stage1(self):
        extract(os.path.join(self.src_dir, self.src_file), self.decode_dir_stage1)
        if self.result:
            files = os.listdir(self.decode_dir_stage1)
            self.assertEqual(len(files), self.result['count_root_files_stage1'])

    def decode_stage2(self):
        json_decode(self.decode_dir_stage1, self.decode_dir_stage2, pool=self.pool)
        if self.result:
            files = os.listdir(self.decode_dir_stage2)
            self.assertEqual(len(files), self.result['count_root_files_stage1'])

    def decode_stage3(self):
        decode(self.decode_dir_stage2, self.decode_dir_stage3, pool=self.pool)
        if self.result:
            files = os.listdir(self.decode_dir_stage3)
            self.assertEqual(len(files), self.result['count_root_files_stage3'])

    def decode_stage4(self):
        helper.clear_dir(os.path.normpath(self.decode_dir_stage4))
        FileOrganizer.unpack(self.decode_dir_stage3, self.decode_dir_stage4, pool=self.pool, index=self.index)
        if self.result:
            files = os.listdir(self.decode_dir_stage4)
            self.assertEqual(len(files), self.result['count_root_files_stage4'])
            pass

    def encode_stage4(self):
        helper.clear_dir(os.path.normpath(self.encode_dir_stage3))
        FileOrganizer.pack(self.decode_dir_stage4, self.encode_dir_stage3, pool=self.pool, index=self.index)
        if self.result:
            files = os.listdir(self.encode_dir_stage3)
            self.assertEqual(len(files), self.result['count_root_files_stage3'])

    def encode_stage3(self):
        encode(self.encode_dir_stage3, self.encode_dir_stage2, version=self.version, pool=self.pool)
        if self.result:
            files = os.listdir(self.encode_dir_stage2)
            self.assertEqual(len(files), self.result['count_root_files_stage1'])
        self.assert_stage(self.decode_dir_stage2, self.encode_dir_stage2)

    def encode_stage2(self):
        json_encode(self.encode_dir_stage2, self.encode_dir_stage1, pool=self.pool)
        if self.result:
            files = os.listdir(self.encode_dir_stage1)
            self.assertEqual(len(files), self.result['count_root_files_stage1'])

        self.assert_stage(self.decode_dir_stage1, self.encode_dir_stage1)

    def encode_stage1(self):
        helper.clear_dir(os.path.normpath(self.encode_dir_stage0))
        encode_file_path = os.path.join(self.encode_dir_stage0, self.src_file)
        # decode_file_path = os.path.join(self.src_dir, self.src_file)
        build(self.encode_dir_stage1, encode_file_path)
        # self.assertByteFile(decode_file_path, encode_file_path)

    def assert_external_data_processor_decode_stage3(self):
        if self.result:
            form_files = os.listdir(os.path.join(self.decode_dir_stage3, 'Form'))
            self.assertEqual(len(form_files), self.result['count_forms_files'])
            template_files = os.listdir(os.path.join(self.decode_dir_stage3, 'Template'))
            self.assertEqual(len(template_files), self.result['count_templates_files'])

    def assert_stage(self, decode_dir, encode_dir):
        problems = self._assert_stage(decode_dir, encode_dir)
        self.assertTrue(not problems, f'file not equal\n{problems}')

    def _assert_stage(self, decode_dir, encode_dir):
        entries = os.listdir(decode_dir)
        problems = ''
        include_problems = ''
        for entry in entries:
            path_decode_entry = os.path.join(decode_dir, entry)
            path_encode_entry = os.path.join(encode_dir, entry)
            if os.path.isdir(path_decode_entry):
                include_problems += self._assert_stage(path_decode_entry, path_encode_entry)
            else:
                with open(path_decode_entry, 'r', encoding='utf-8') as file:
                    decode_data = file.read()
                with open(path_encode_entry, 'r', encoding='utf-8') as file:
                    encode_data = file.read()
                if decode_data != encode_data:
                    problems += f'\n      {entry}'
        if problems:
            problems = f'   {decode_dir}\n   {encode_dir}{problems}\n'
        if include_problems:
            problems += '\n' + include_problems
        return problems

    def tmpl_json_encode(self, *, encode_src_dir='', entity_name='', encode_dest_dir='', decode_dir=''):
        JsonContainerDecoder.encode(encode_src_dir, f'{entity_name}.json', encode_dest_dir)
        if decode_dir:
            self.assertUtfFile(
                os.path.join(encode_dest_dir, entity_name),
                os.path.join(decode_dir, entity_name)
            )

    def assertUtfFile(self, src, dest):
        with open(src, 'r', encoding='utf-8') as file:
            src_data = file.read()
        with open(dest, 'r', encoding='utf-8') as file:
            dest_data = file.read()
        self.assertEqual(dest_data, src_data)

    def assertByteFile(self, src, dest):
        with open(src, 'rb') as file:
            src_data = file.read()
        with open(dest, 'rb') as file:
            dest_data = file.read()
        self.assertEqual(dest_data, src_data)
