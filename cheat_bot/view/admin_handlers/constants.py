from cheat_bot import di

ADMIN_LIST = [int(x) for x in di.di_container.settings.admins_id.split(',')]
