from core.framework.service import use, NAMED_SERVICE
from core.services.db import DB
from core.utils.import_path import import_path
from core.utils.object import call_inherit_method


def module_imports():
    db = use(DB)

    modules = import_path('./**/exports.py', returns=['export_models', 'export_services'])

    paths = []

    db.create_table()

    for module in modules:
        module_path = module.__file__[0:-11]
        paths.append(module_path)

        # Create Table
        models = None

        try:
            models = module.export_models
        except:
            pass

        if models:
            for model in models:
                model._on_load()

        services = None

        try:
            services = module.export_services
        except:
            pass

        if services:
            for service in services:
                service.log_('Initialize')

                NAMED_SERVICE.__setitem__(service.__name__[:-7], service)
                call_inherit_method(use(service), '_on_built')

                service.log_('Initialize Complete')

    return paths
