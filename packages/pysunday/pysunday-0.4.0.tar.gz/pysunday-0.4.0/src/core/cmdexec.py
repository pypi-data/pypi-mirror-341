# coding: utf-8
import subprocess
from threading import Timer
from sunday.core.logger import Logger

logger = Logger('cmdexec').getLogger()

""" subprocess.Popen
入参: args, bufsize=0, executable=None, stdin=None, stdout=None, stderr=None,
preexec_fn=None, close_fds=False, shell=False, cwd=None, env=None,
universal_newlines=False, startupinfo=None, creationflags=0
出参: stdin, stdout, stderr, pid, returncode
"""

def cmdexec(cmd, timeout = 10, **kwargs):
    """
    执行系统命令, 返回: code, stdout, stderr, 当code不为0则为报错

    **Parameters:**

    * **cmd:** `str` -- 命令文本
    * **timeout:** `int` -- 超时时间

    **Return:**

    * **code:** `int` 为0则执行成功，否则执行失败
    * **success:** `str` 执行成功打印内容
    * **error:** `str` 执行失败打印内容
    """
    logger.warning('执行命令: %s' % cmd)
    subp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)
    timer = Timer(timeout, lambda p: p.kill(), [subp])
    try:
        timer.start()
        subp.wait()
        code = subp.returncode
        stdout = subp.stdout.read()
        stderr = subp.stderr.read()
        getattr(logger, 'error' if code else 'info')('%d: %s' % (code, cmd))
        return code, stdout.decode(), stderr.decode()
    except Exception as e:
        logger.exception(e)
        return 1, '', 'timeout'
    finally:
        timer.cancel()


if __name__ == "__main__":
    cmdexec('getToken')
