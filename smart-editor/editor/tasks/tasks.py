"""
    Created by Sanjul Sharma on April 22, 2021
    All rights reserved. Copyright © 2021.
"""
import sys

from celery.schedules import crontab
from celery.task import periodic_task

from editor.models import RichText

__author__ = "Sanjul Sharma"


@periodic_task(run_every=crontab(minute="*/10"))
def expire_key_provide_warning_and_decrypt_existing_data():
    from Crypto.Cipher import AES
    import base64
    from hashlib import md5
    def unpad(data):
        return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

    def bytes_to_key(data, salt, output=48):
        assert len(salt) == 8, len(salt)
        data += salt
        key = md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = md5(key + data).digest()
            final_key += key
        return final_key[:output]

    def decrypt(encrypted, passphrase):
        encrypted = base64.b64decode(encrypted)
        assert encrypted[0:8] == b"Salted__"
        salt = encrypted[8:16]
        key_iv = bytes_to_key(passphrase, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = AES.new(key, AES.MODE_CBC, iv)
        return unpad(aes.decrypt(encrypted[16:]))

    sys.stdout.write("Starting auto expiring process >>>>>>>")
    rt = RichText.objects.first()
    txt_ = rt.editor_text
    key_ = rt.key
    if txt_ is not None and key_ is not None:
        sys.stdout.write("Start auto expiring and decrypting >>>>>>>")
        decrypted_txt = decrypt(txt_, key_.encode())
        rt.editor_text = decrypted_txt.decode()
        rt.key_expired = True
        rt.key = None
        rt.key_file_name = None
        rt.save()
        sys.stdout.write("<<<<<<< End auto expiring and decrypting")
    sys.stdout.write("<<<<<<< Ending auto expiring process")
