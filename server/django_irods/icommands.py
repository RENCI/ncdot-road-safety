"""Originally written by Antoine deTorcy"""

import os
import shutil
import subprocess
import textwrap
from io import StringIO
from django.conf import settings
from collections import namedtuple


class SessionException(Exception):
    def __init__(self, exitcode, stdout, stderr):
        super(SessionException, self).__init__(self,
                                               "Error processing IRODS request: {exitcode}. "
                                               "stderr follows:\n\n{stderr}".format(
                                                   exitcode=exitcode, stderr=stderr))
        self.stdout = str(stdout)
        self.stderr = str(stderr)
        self.exitcode = exitcode


IRodsEnv = namedtuple(
    'IRodsEnv',
    ['pk', 'host', 'port', 'def_res', 'home_coll', 'cwd', 'username', 'zone', 'auth']
)


class Session(object):
    """A set of methods to start, close and manage multiple
    iRODS client sessions at the same time, using icommands.
    """

    def __init__(self, session_id='default_session'):
        self.root = settings.IRODS_ROOT  # main directory to store session and log dirs
        self.icommands_path =settings.IRODS_ICOMMANDS_PATH  # where the icommand
        # binaries are
        self.session_id = session_id
        self.session_path = "{root}/{session_id}".format(root=self.root,
                                                         session_id=self.session_id)

    def create_environment(self, myEnv=None):
        """Creates session files in temporary directory.

        Argument myEnv must be instance of RodsEnv defined above.
        This method is to be called prior to calling self.runCmd('iinit').
        """
        # will have to add some testing for existing files
        # and acceptable argument values
        if not os.path.exists(self.session_path):
            try:
                os.makedirs(self.session_path)
            except OSError:
                raise OSError('Session path {} cannot be created'.format(self.session_path))

        if not myEnv:
            hpath = '/' + settings.IRODS_ZONE + '/home/' + settings.IRODS_USER
            myEnv = IRodsEnv(
               pk=-1,
               host=settings.IRODS_HOST,
               port=settings.IRODS_PORT,
               def_res=settings.IRODS_RESC,
               home_coll=hpath,
               cwd=hpath,
               username=settings.IRODS_USER,
               zone=settings.IRODS_ZONE,
               auth=settings.IRODS_PWD
            )

        # create irods_environment.json file
        env_path = "{session_path}/irods_environment.json".format(session_path=self.session_path)
        with open(env_path, "w") as env_file:
            env_pre_str = "{\n"
            env_str = textwrap.dedent("""\
                "irods_host": "{host}",
                "irods_port": {port},
                "irods_default_resource": "{def_res}",
                "irods_home": "{home_coll}",
                "irods_cwd": "{cwd}",
                "irods_user_name": "{username}",
                "irods_zone_name": "{zone}"
            """).format(
                host=myEnv.host,
                port=myEnv.port,
                def_res=myEnv.def_res,
                home_coll=myEnv.home_coll,
                username=myEnv.username,
                cwd=myEnv.cwd,
                zone=myEnv.zone
            )
            env_post_str = "}"
            env_file.write('{line1}{line2}{line3}'.format(line1=env_pre_str, line2=env_str,
                                                          line3=env_post_str))
            return myEnv

    def delete_environment(self):
        """Deletes temporary sessionDir recursively.

        To be called after self.runCmd('iexit').
        """
        shutil.rmtree(self.session_path)

    def run(self, icommand, data=None, *args):
        """Runs an icommand with optional argument list and
        returns tuple (stdout, stderr) from subprocess execution.

        Set of valid commands can be extended.
        """

        myenv = os.environ.copy()
        myenv['IRODS_ENVIRONMENT_FILE'] = os.path.join(self.session_path, "irods_environment.json")
        myenv['IRODS_AUTHENTICATION_FILE'] = os.path.join(self.session_path, ".irodsA")

        cmdStr = os.path.join(self.icommands_path, icommand)
        argList = [cmdStr]
        uargs = [x.encode('utf-8') for x in args]
        argList.extend(uargs)

        stdin = None
        if data:
            stdin = StringIO(data)

        proc = subprocess.Popen(
            argList,
            stdin=subprocess.PIPE if stdin else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=myenv
        )
        stdout, stderr = proc.communicate(input=data) if stdin else proc.communicate()

        if proc.returncode:
            raise SessionException(proc.returncode, stdout, stderr)
        else:
            return stdout.decode(), stderr.decode()

    def run_safe(self, icommand, data=None, *args):
        myenv = os.environ.copy()
        myenv['IRODS_ENVIRONMENT_FILE'] = os.path.join(self.session_path, "irods_environment.json")
        myenv['IRODS_AUTHENTICATION_FILE'] = os.path.join(self.session_path, ".irodsA")

        cmdStr = os.path.join(self.icommands_path, icommand)
        argList = [cmdStr]
        argList.extend(args)

        stdin = None
        if data:
            print(data)
            stdin = StringIO(data)

        proc = subprocess.Popen(
            argList,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=myenv
        )
        return proc

    def runbatch(self, *icommands):
        myenv = os.environ.copy()
        myenv['IRODS_ENVIRONMENT_FILE'] = os.path.join(self.session_path, "irods_environment.json")
        myenv['IRODS_AUTHENTICATION_FILE'] = os.path.join(self.session_path, ".irodsA")
        return_codes = []

        for icommand, args in icommands:
            cmdStr = os.path.join(self.icommands_path, icommand)
            argList = [cmdStr]
            argList.extend(args)

            return_codes.append(subprocess.Popen(
                argList,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=myenv
            ).communicate())
        return return_codes


GLOBAL_SESSION = Session()
GLOBAL_ENVIRONMENT = GLOBAL_SESSION.create_environment()
GLOBAL_SESSION.run('iinit', None, GLOBAL_ENVIRONMENT.auth)
