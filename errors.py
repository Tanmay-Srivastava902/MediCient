'''CONTAINS CUSTOM ERROR CLASSES AND ERROR CONSTANTS '''
class InstallError(Exception):
    '''installation of program/service is failed'''
    pass
class AuthError(Exception):
    '''  wrong credential leading to failed authentication needs retied'''
    pass
class InvalidArgumentError(Exception):
    '''  wrong parameters given'''
    pass
class MysqlConnectionError(Exception):
    '''  could not connect due to general connector problem'''
class MaxAttemptError(Exception):
    '''  no attempts left'''
    pass
class NeedsInstallError(Exception):
    '''  something program/service is missing needed to be installed'''
    pass
class AlreadyExistsError(Exception):
    '''entity file/folder/db/user/record is already existing'''
    pass

class FileNotFoundError(Exception):
    '''file is missing/corrupted'''
    pass
class DBConnectionError(Exception):
    pass
class FolderNotFoundError(Exception):
    '''entity folder is missing/corrupted'''
    pass
class UserNotFoundError(Exception):
    '''user not exists'''
    pass
class InsertError(Exception):
    pass
class UpdateError(Exception):
    pass
class RecordNotFoundError(Exception):
    '''record is missing/corrupted'''
    pass
class RecordError(Exception):
    pass
class DatabaseNotFoundError(Exception):
    pass
class DBError(Exception):
    pass

class ExecutionError(Exception):
    '''the problem in subprocess or executor '''
    pass
class TableError(Exception):
    '''database tables are not proper'''
class ServiceError(Exception):
    '''Class For all error  systemd failure '''
    pass
class PipError(Exception):
    '''Class For all error  pip failure '''
    pass
class PackageError(Exception):
    '''Class For all error  Package failure '''
    pass
class AptError(Exception):
    '''Class For all error  Package failure '''
    pass
class VenvError(Exception):
    '''Class For all error  Venv failure '''
    pass
class EncryptionError(Exception):
    '''for '''
    pass
class SecurityError(Exception):
    pass
class ConfigError(Exception):
    pass
class GeneralFileError(Exception):
    pass