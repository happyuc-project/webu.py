def construct_user_agent(class_name):
    from webu import __version__ as webu_version

    user_agent = 'Webu.py/{version}/{class_name}'.format(
        version=webu_version,
        class_name=class_name,
    )
    return user_agent
