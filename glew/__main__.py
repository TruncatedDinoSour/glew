import base64
import pickle
import bz2
import os
from cryptography.fernet import Fernet


def encrypt_file(file: open):
    try:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        print(f'encrypting {file}...')
        with open(file, 'rb') as f:
            with bz2.BZ2File(f'{file}.sev1', 'wb') as f1:
                pickle.dump(base64.b85encode(fernet.encrypt(f.read())), f1)
        print(f'your decryption key is:\n{base64.b64encode(key)}')
    except Exception as e:
        print(f'failed encrypting {file} - {e}')
    print(f'finished decrypting {file}')


def decrypt_file(file: open, key: bytes):
    print(f'decrypting {file}...')
    try:
        if os.path.splitext(file)[1].lower() == '.sev1':
            fernet = Fernet(base64.b64decode(key))
            with bz2.BZ2File(file, 'rb') as f:
                enc_data = base64.b85decode(pickle.load(f))
                with open('de-'+file.replace('.sev1', ''), 'wb') as f1:
                    f1.write(fernet.decrypt(enc_data))
                    return
        raise Exception('encryption file extension is wrong')
    except Exception as e:
        print(f'failed decrypting {file} - {e}')
    print(f'finished decrypting {file}')
