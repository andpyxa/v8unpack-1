from .Form83 import Form83


class DocumentForm83(Form83):
    @classmethod
    def get_decode_obj_header(cls, header):
        return header[0][1]

    def encode_header(self):
        return [[
            "1",
            [
                "0",
                self.encode_header_title(),
            ],
            "0"
        ]]
