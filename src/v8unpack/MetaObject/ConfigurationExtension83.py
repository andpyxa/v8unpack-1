from ..MetaObject.Configuration83 import Configuration83
from .. import helper
from .. import __version__


class ConfigurationExtension83(Configuration83):
    info = ['6', '8']
    ext_code = {
        'con': '5',
        'app': '6',
        'ssn': '7'
    }

    def __init__(self):
        super(ConfigurationExtension83, self).__init__()

    @classmethod
    def decode(cls, src_dir, dest_dir):
        self = cls()
        self.header = {}
        root = helper.json_read(src_dir, 'configinfo.json')
        self.header['v8unpack'] = __version__
        self.header['file_uuid'] = root[1][1]
        self.header['version'] = root[0][1]
        self.header['versions'] = root[2]
        self.header['copyinfo'] = root[1]
        self.header['data'] = helper.json_read(src_dir, f'{self.header["file_uuid"]}.json')
        _form_header = self.get_decode_header(self.header['data'])
        helper.decode_header(self.header, _form_header)
        self.decode_code(src_dir)

        for i in self.info:  # хз что это
            try:
                self.header[f'info{i}'] = helper.json_read(src_dir, f'{self.header["uuid"]}.{i}.json')
            except FileNotFoundError:
                pass

        helper.json_write(self.header, dest_dir, f'{cls.get_class_name_without_version()}.json')
        self.write_decode_code(dest_dir, cls.__name__)
        tasks = self.decode_includes(src_dir, dest_dir, '', self.header['data'])
        return tasks

    @classmethod
    def encode(cls, src_dir, dest_dir):
        self = cls()
        helper.clear_dir(dest_dir)
        self.header = helper.json_read(src_dir, f'{cls.get_class_name_without_version()}.json')
        helper.check_version(__version__, self.header.get('v8unpack', ''))
        root = [
            ["0", self.encode_version()],
            self.header['copyinfo'],
            self.header['versions']
        ]
        self.encode_code(src_dir, cls.__name__)
        self.write_encode_code(dest_dir)
        helper.json_write(root, dest_dir, 'configinfo.json')
        helper.json_write(self.header['data'], dest_dir, f'{self.header["file_uuid"]}.json')
        for i in self.info:  # хз что это
            try:
                helper.json_write(self.header[f'info{i}'], dest_dir, f'{self.header["uuid"]}.{i}.json')
            except KeyError:
                pass
        tasks = self.encode_includes(src_dir, dest_dir)
        return tasks
