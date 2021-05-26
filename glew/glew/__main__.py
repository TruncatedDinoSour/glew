import base64, pickle, bz2, os, sys, functools
from cryptography.fernet import Fernet

ENCRYPTION_EXTENSION = '.sev3'


@functools.cache
def encrypt_file(file: open):
    try:
        key = Fernet.generate_key()
        fernet = Fernet(key)
        print(f'encrypting {file}...')
        with open(file, 'rb') as f:
            with bz2.BZ2File(f'{file}{ENCRYPTION_EXTENSION}', 'wb') as f1:
                pickle.dump(base64.b85encode(fernet.encrypt(f.read())), f1)
        print(f'your decryption key is (DO NOT LOSE IT):\n{base64.b64encode(key).decode()}')
    except Exception as e:
        print(f'failed encrypting {file} - {e}')
    finally:
        print(f'finished encrypting {file}')


@functools.cache
def decrypt_file(file: open, key: bytes):
    print(f'decrypting {file}...')
    try:
        if os.path.splitext(file)[1].lower() == ENCRYPTION_EXTENSION:
            fernet = Fernet(base64.b64decode(key))
            with bz2.BZ2File(file, 'rb') as f:
                enc_data = base64.b85decode(pickle.load(f))
                with open(f"{file.replace(ENCRYPTION_EXTENSION, '')}-de", 'wb') as f1:
                    f1.write(fernet.decrypt(enc_data))
            return
        raise Exception('encryption file extension is wrong!')
    except Exception as e:
        print(f'failed decrypting {file} - {e}')
    finally:
        print(f'finished decrypting {file}')


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'encrypt':
            encrypt_file(sys.argv[2])
        elif sys.argv[1] == 'decrypt':
            decrypt_file(sys.argv[2], sys.argv[3].encode())
        else:
            print('''glew encrypt [file]
    glew decrypt \'[file]\' \'[key]\'''')
    except IndexError:
        print('''glew encrypt \'[file]\'
    glew decrypt \'[file]\' \'[key]\'''')
