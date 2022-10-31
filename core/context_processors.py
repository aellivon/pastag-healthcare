from django.conf import settings  # import the settings file


def static_folder_subpath(request):

    if not settings.DEBUG or settings.TESTING_BUILD:
        return {'static_supbpath': "dist"}
    else:
        return {'static_supbpath': "src"}