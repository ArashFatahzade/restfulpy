from os.path import join, dirname

from restfulpy.application import Application

from .tokens import RegisterationToken, ResetPasswordToken
from .authentication import Authenticator
from .controllers.root import Root


__version__ = '0.1.0-dev'


class ${project_name.capitalize()}(Application):
    __authenticator__ = Authenticator()
    __configuration__ = '''
    db:
      url: postgresql://postgres:postgres@localhost/${project_name}_dev
      test_url: postgresql://postgres:postgres@localhost/${project_name}_test
      administrative_url: postgresql://postgres:postgres@localhost/postgres

    reset_password:
      secret: !!binary xxSN/uarj5SpcEphAHhmsab8Ql2Og/2IcieNfQ3PysI=
      max_age: 3600  # seconds
      algorithm: HS256
      callback_url: http://nc.carrene.com/reset_password
      # url: http://localhost:8080/reset_password

    registeration:
      secret: !!binary xxSN/uarj5SpcEphAHhmsab8Ql2Og/2IcieNfQ3PysI=
      max_age: 86400  # seconds
      algorithm: HS256
      callback_url: http://cas.carrene.com/register

    messaging:
      default_messenger: restfulpy.messaging.ConsoleMessenger
      template_dirs:
        - %(root_path)s/${project_name}/email_templates
    '''

    def __init__(self, application_name='${project_name}', root=Root()):
        super().__init__(
            application_name,
            root=root,
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )


${project_name} = ${project_name.capitalize()}()

