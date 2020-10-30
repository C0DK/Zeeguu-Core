import os

import sys
from zeeguu_core.logs import info


class CouldNotLoadConfigsError(Exception):
    pass


def load_configuration_or_abort(app, environ_variable, mandatory_config_keys=[]):
    """

        Try to load config from the file named in the environ variable.

        If a config is loaded, the function makes sure that the mandatory_config_keys are
        in the file

    :return: Returns in case of success. Throws exception otherwise.

    """

    if _called_from_within_a_test():
        _load_core_testing_configuration(app)
        _load_api_testing_configuration(app)
        info("ZEEGUU: Loaded testing configuration.")
    else:
        try:
            config_file = _load_config_file(
                environ_variable, mandatory_config_keys)
            app.config.from_pyfile(config_file, silent=False)
            _assert_configs(app.config, mandatory_config_keys, config_file)
            info("ZEEGUU: Loaded {0} config from {1}".format(
                app.name, config_file))
        # TODO don't catch base class exception
        except Exception as e:
            raise CouldNotLoadConfigsError(e)


def _assert_configs(config, required_keys, config_file_name=None):
    for key in required_keys:
        if key not in config or config[key] is None:
            raise CouldNotLoadConfigsError(
                "Please define the {key} key in the {config} file!".format(key=key,
                                                                           config=config_file_name or 'config')
            )


def _called_from_within_a_test():
    return 'unittest' in sys.modules


def _load_core_testing_configuration(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['MAX_SESSION'] = 99999999
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def _load_api_testing_configuration(app):
    app.config['HOST'] = '0.0.0.0'
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = "lalala"


def _load_config_file(environ_variable, mandatory_config_keys):
    try:
        return os.environ[environ_variable]
    except KeyError:
        raise CouldNotLoadConfigsError(
            f"You must define an envvar named {environ_variable} which points to a config file which"
            f'defines at least the following constants: {mandatory_config_keys}')
