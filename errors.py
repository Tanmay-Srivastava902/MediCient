'''CONTAINS CUSTOM ERROR CLASSES '''
class InstallError(Exception):
    '''class for error indicating an installation of program/service is failed'''
    pass
class AuthError(Exception):
    '''Class for error indicating wrong credential leading to failed authentication needs retied'''
    pass
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
