def _get_queryset(klass):
    """
        # NOTE: Taken from django code base itself. We could do a lot of things
          with this!
        Return a QuerySet or a Manager.
    """
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass


def get_object_or_None(klass, *args, **kwargs):
    """
        # Modified get_object_or_404
        Use get() to return an object, or raise a None exception if the object
        does not exist.
        klass may be a Model, Manager, or QuerySet object. All other passed
        arguments and keyword arguments are used in the get() query.
        Like with QuerySet.get(), MultipleObjectsReturned is raised if more than
        one object is found.
    """
    queryset = _get_queryset(klass)
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument to get_object_or_None() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )

    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
