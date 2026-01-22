'''CONTAINS CUSTOM ERROR CLASSES AND ERROR CONSTANTS '''
class InstallError(Exception):
    '''class for error indicating an installation of program/service is failed'''
    pass
class AuthError(Exception):
    '''Class for error indicating wrong credential leading to failed authentication needs retied'''
    pass
class InvalidArgumentError(Exception):
    '''Class for error indicating wrong parameters given'''
    pass
class MysqlConnectionError(Exception):
    '''Class for error indicating could not connect due to general connector problem'''
class MaxAttemptError(Exception):
    '''Class for error indicating no attempts left'''
    pass
class NeedsInstallError(Exception):
    '''Class for error indicating something program/service is missing needed to be installed'''
    pass
class AlreadyExistsError(Exception):
    '''Class for error indicating an entity file/folder/db/user/record is already existing'''
    pass
class DoesNotExistsError(Exception):
    '''Class for error indicating an entity file/folder/db/user/record is missing/corrupted cannot  be found'''
    pass
class ExecutionError(Exception):
    '''Class For all Execution errors indicating the problem in subprocess or executor '''
    pass
# class ServiceStartError(Exception):
#     '''Class For error indicating could not start a service '''
# class ServiceStopError(Exception):
#     '''Class For error indicating could not stop a service '''
# class ServiceRestartError(Exception):
#     '''Class For error indicating could not restart a service '''
class ServiceError(Exception):
    '''Class For all error indicating systemd failure '''
    pass
class PipError(Exception):
    '''Class For all error indicating pip failure '''
    pass
class PackageError(Exception):
    '''Class For all error indicating Package failure '''
    pass
class AptError(Exception):
    '''Class For all error indicating Package failure '''
    pass
class VenvError(Exception):
    '''Class For all error indicating Venv failure '''
    pass
