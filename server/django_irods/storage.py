import os
from tempfile import NamedTemporaryFile

from django.utils.deconstruct import deconstructible
from django.core.files.storage import Storage
from django.core.exceptions import ValidationError
from django.conf import settings

from .icommands import GLOBAL_SESSION, GLOBAL_ENVIRONMENT, SessionException


@deconstructible
class IrodsStorage(Storage):
    def __init__(self):
        self.session = GLOBAL_SESSION
        self.environment = GLOBAL_ENVIRONMENT

    def get_image_coll_path(self, image_file_name):
        """
        Get image collection path in iRODS
        :param image_file_name: image file name to get such as 757000958286.jpg
        :return: the collection path in iRODS
        """
        qrystr = "SELECT COLL_NAME WHERE DATA_NAME = '{}'".format(image_file_name)
        coll_name = self.session.run("iquest", None, "%s", qrystr)[0]

        if "CAT_NO_ROWS_FOUND" in coll_name:
            raise ValidationError("{} cannot be found".format(image_file_name))
        return coll_name.strip('\n')

    def get_one_image_frame(self, image_file_name, dest_path):
        """
        Get one image frame by file name
        :param image_file_name: image file name to get such as 757000958286.jpg
        :param dest_path: destination path on web server to retrieve image from iRODS to
        :return: the image file name with full path
        """

        coll_name = self.get_image_coll_path(image_file_name)
        src_path = os.path.join(coll_name, image_file_name)
        self.session.run("iget", None, '-f', src_path, dest_path)
        return dest_path

    def get_file(self, src_name, dest_name):
        self.session.run("iget", None, '-f', src_name, dest_name)

    def exists(self, name):
        try:
            stdout = self.session.run("ils", None, name)[0]
            return stdout != ""
        except SessionException:
            return False

    def delete(self, name):
        # this storage is read only
        pass

    def open(self, name, mode='rb'):
        tmp = NamedTemporaryFile()
        self.session.run("iget", None, '-f', name, tmp.name)
        return tmp

    def save(self, name, content, max_length=None):
        # this storage is read only
        pass

    def _list_files(self, path):
        """
        internal method to only list data objects/files under path
        :param path: iRODS collection/directory path
        :return: ordered filename_list
        """

        fname_list = []

        # the query below returns name of all data objects/files under the path collection/directory
        qrystr = "select DATA_NAME where DATA_REPL_STATUS != '0' AND " \
                 "{}".format(IrodsStorage.get_absolute_path_query(path))
        stdout = self.session.run("iquest", None, "--no-page", "%s",
                                  qrystr)[0].split("\n")

        for i in range(len(stdout)):
            if not stdout[i] or "CAT_NO_ROWS_FOUND" in stdout[i]:
                break
            fname_list.append(stdout[i])

        return fname_list

    def _list_sub_dirs(self, path):
        """
        internal method to only list sub-collections/sub-directories under path
        :param path: iRODS collection/directory path
        :return: sub-collection/directory name list
        """
        subdir_list = []
        # the query below returns name of all sub-collections/sub-directories
        # under the path collection/directory
        qrystr = "select COLL_NAME where {}".format(IrodsStorage.get_absolute_path_query(path, parent=True))
        stdout = self.session.run("iquest", None, "--no-page", "%s",
                                  qrystr)[0].split("\n")
        for i in range(len(stdout)):
            if not stdout[i] or "CAT_NO_ROWS_FOUND" in stdout[i]:
                break
            dirname = stdout[i]
            # remove absolute path prefix to only show relative sub-dir name
            idx = dirname.find(path)
            if idx > 0:
                dirname = dirname[idx + len(path) + 1:]

            subdir_list.append(dirname)

        return subdir_list

    def get_absolute_path_query(path, parent=False):
        """
        Get iquest query string that needs absolute path of the input path for the HydroShare iRODS data zone
        :param path: input path to be converted to absolute path if needed
        :param parent: indicating whether query string should be checking COLL_PARENT_NAME rather than COLL_NAME
        :return: iquest query string that has the logical path of the input path as input
        """

        # iquest has a bug that cannot handle collection name containing single quote as reported here
        # https://github.com/irods/irods/issues/4887. This is a work around and can be removed after the bug is fixed
        if "'" in path:
            path = path.replace("'", "%")
            qry_str = "COLL_PARENT_NAME like '{}'" if parent else "COLL_NAME like '{}'"
        else:
            qry_str = "COLL_PARENT_NAME = '{}'" if parent else "COLL_NAME = '{}'"

        if os.path.isabs(path):
            # iRODS federated logical path which is already absolute path
            return qry_str.format(path)
        return qry_str.format(os.path.join('/', settings.IRODS_ZONE, 'home', settings.IRODS_USER, path))

    def listdir(self, path):
        """
        return list of sub-collections/sub-directories and data objects/files
        :param path: iRODS collection/directory path
        :return: (sub_directory_list, file_name_list)
        """
        # remove any trailing slashes if any; otherwise, iquest would fail
        path = path.strip()
        while path.endswith('/'):
            path = path[:-1]

        # check first whether the path is an iRODS collection/directory or not, and if not, need
        # to raise SessionException, and if yes, can proceed to get files and sub-dirs under it
        qrystr = "select COLL_NAME where {}".format(IrodsStorage.get_absolute_path_query(path))
        stdout = self.session.run("iquest", None, "%s", qrystr)[0]
        if "CAT_NO_ROWS_FOUND" in stdout:
            raise SessionException(-1, '', 'folder {} does not exist'.format(path))

        fname_list = self._list_files(path)

        subdir_list = self._list_sub_dirs(path)

        listing = (subdir_list, fname_list)

        return listing

    def size(self, name):
        """
        return the size of the data object/file with file name being passed in
        :param name: file name
        :return: the size of the file
        """
        file_info = name.rsplit('/', 1)
        if len(file_info) < 2:
            raise ValidationError('{} is not a valid file path to retrieve file size '
                                  'from iRODS'.format(name))
        coll_name = file_info[0]
        file_name = file_info[1]
        qrystr = "select DATA_SIZE where DATA_REPL_STATUS != '0' AND " \
                 "COLL_NAME like '%{}' AND DATA_NAME = '{}'".format(coll_name, file_name)
        stdout = self.session.run("iquest", None, "%s", qrystr)[0]

        if "CAT_NO_ROWS_FOUND" in stdout:
            raise ValidationError("{} cannot be found in iRODS to retrieve "
                                  "file size".format(name))
        return int(stdout)

    def get_available_name(self, name):
        """
        Reject duplicate file names rather than renaming them.
        """
        if self.exists(name):
            raise ValidationError(str.format("File {} already exists.", name))
        return name
