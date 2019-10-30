import re
import subprocess
import os
import uuid
from django.conf import settings


class TmpFile:

    def __init__(self, ext):
        self.filename = "%s.%s" % (uuid.uuid4(), ext)
        self.filedir = os.path.join(settings.TMP_DIR, self.filename)

    def create(self, file_content):
        file = open(self.filedir, "wb")
        file.write(bytes(file_content, 'utf-8'))
        file.close()
        return self.filename

    def remove(self):
        os.remove(self.filedir)
        return True


def debug(input, content):
    stdin = bytes(input, 'utf-8')
    tmp_file = TmpFile(ext='py')
    filename = tmp_file.create(content)
    args = [settings.PYTHON_PATH, filename]
    proc = subprocess.Popen(
        args=args,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=settings.TMP_DIR,
    )

    stdout, stderr = proc.communicate(stdin)
    tmp_file.remove()
    proc.kill()
    return {
        'output': stdout.decode("utf-8"),
        'error': re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
    }


def normalize_fract_part(val1, val2, limit=8):
    parts1 = val1.split('.')
    if len(parts1) < 2:
        parts1.append('0')

    parts2 = val2.split('.')
    if len(parts2) < 2:
        parts2.append('0')

    parts1[1] = parts1[1][:limit]
    parts2[1] = parts2[1][:limit]

    return '.'.join(parts1), '.'.join(parts2)


def check_test(output, error, test_output):

    """ Проверка вывода программы на тесте
        Нормализация:
            - удаление спец. символов возврата каректи и пробелов в начале и конце
            - для дробных чисел проверка только до восьмого символа дробной части
            - для дробных числе 1.0 == 1
    """
    if error:
        return False
    else:
        out = output.replace('\r', '').strip()
        t_out = test_output.replace('\r', '').strip()
        if t_out.replace('.', '').isdigit():
            out, t_out = normalize_fract_part(out, t_out)
        return t_out == out


def tests(content, tests):
    tmp_file = TmpFile(ext='py')
    filename = tmp_file.create(content)
    args = [settings.PYTHON_PATH, filename]
    tests_data = []
    tests_num = len(tests)
    tests_num_success = 0
    for i in range(len(tests)):
        proc = subprocess.Popen(
            args=args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=settings.TMP_DIR,
        )
        stdin = bytes(tests[i]['input'], 'utf-8')
        stdout, stderr = proc.communicate(stdin)
        output = stdout.decode("utf-8")
        error = re.sub(r'\s*File.+.py",', "", stderr.decode("utf-8"))
        success = check_test(output, error, tests[i]['output'])
        if success:
            tests_num_success += 1

        tests_data.append({
            "output": output,
            "error": error,
            "success": success
        })
        proc.kill()

    tmp_file.remove()

    return {
        'num': tests_num,
        'num_success': tests_num_success,
        'data': tests_data,
        'success': bool(tests_num == tests_num_success),
    }


__all__ = [
    'debug',
    'tests'
]