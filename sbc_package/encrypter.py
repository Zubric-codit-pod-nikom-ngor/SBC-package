import hashlib
import re
import ast
import os
from pathlib import Path
import sbc_package.aes256
from pyaes256 import PyAES256
from sbc_package.support import get


def get_hash(item: str) -> bytes:
    return hashlib.sha512(item.encode()).digest()


def get_16_hash(item: str) -> bytes:
    return hashlib.sha1(item.encode()).digest()


def digest_files(path: str) -> bool:
    def get_all_subdirs(path):
        p = Path(path)
        subdirs = [entry for entry in p.rglob("*") if entry.is_dir()]
        sbdrs = list(map(lambda item: str(item), subdirs))
        sbdrs = list(map(lambda item: item if '__pycache__' not in item else False, sbdrs))
        while False in sbdrs:
            sbdrs.remove(False)
        return sbdrs

    walked = os.walk(path)
    filenames = list(map(lambda item: item[2], walked))
    ffn = []
    for el in filenames:
        for file in el:
            ffn.append(file)
    files = list(map(lambda item: item if '__pycache__' not in item and \
                                          '.pyc' not in item and \
                                          'encryptedBase' not in item and \
                                          'encrypter.py' not in item and \
                                          'base.py' not in item and \
                                          'assigning.py' not in item else False, ffn))
    while False in files:
        files.remove(False)
    hashes = []
    subdirs = get_all_subdirs(path)
    while False in files:
        files.remove(False)
    c = 0
    for item in files:
        p = path
        while True:
            try:
                with open(p + '\\' + item, 'r') as file:
                    hashes.append(str(get_hash(file.read())))
                    c = 0
                    break
            except:
                p = subdirs[c]
                c += 1
    gigahash = get_hash(''.join(hashes))
    return gigahash


def load_dict_with_bytes(s) -> dict:
    bytes_pattern = re.compile(r"b(['\"])(.*?)(?<!\\)\1", re.DOTALL)
    replacements = {}

    def replace(match):
        key = f"__BYTES_{len(replacements)}__"
        quote = match.group(1)
        content = match.group(2)
        replacements[key] = f"b{quote}{content}{quote}"
        return f"'{key}'"

    processed_str = bytes_pattern.sub(replace, s)
    parsed = ast.literal_eval(processed_str)

    def restore(obj):
        if isinstance(obj, dict):
            return {k: restore(v) for k, v in obj.items()}
        if isinstance(obj, str) and obj.startswith('__BYTES_'):
            return ast.literal_eval(replacements[obj])
        return obj

    return restore(parsed)


hashed = digest_files(get('..\\sbc_package'))

with open(get('encryptedBase'), 'r') as encryptedBase:
    try:
        read = encryptedBase.read()
        loaded = load_dict_with_bytes(read)
        aes = PyAES256()
        decrypted = aes.decrypt(url=loaded['url'],
                                    iv=loaded['iv'],
                                    salt=loaded['salt'],
                                    password=str(hashed)).decode()
        exec(decrypted)
        print('core loaded successfully')
    except:
        raise ValueError('Your blockchain was modified, please consider rewinding the changes or reinstalling the package')
# with open(get('encryptedBase'), 'r') as encryptedBase:
#     readddt = encryptedBase.read()
# with open(get('encryptedBase'), 'w') as encryptedBase_w:
#     encrypted = sbc_package.aes256.encrypt(readddt,str(hashed))
#     encryptedBase_w.write(str(encrypted))
#     print(encrypted)