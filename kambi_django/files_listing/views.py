from logging import getLogger
import json

from django import http
from django.core.exceptions import PermissionDenied, BadRequest

from .models import list_files
from . import utilities


logger = getLogger(__name__)


def list_files_view(request, folder_name):
    name = request.GET.get('name', None)
    params = request.GET.get('params', None)

    output, error = list_files(folder_name, name, params)
    result = utilities.to_dict(output, error)

    if error:
        decoded_error = error.decode()
        logger.error(decoded_error)
        if "Permission denied" in decoded_error:
            raise PermissionDenied()
        else:
            raise BadRequest()
    else:
        return http.HttpResponse(json.dumps(result), status=200, content_type="application/json")


def page_not_found_view(request, exception):
    return http.HttpResponseNotFound("The requested URL cannot be found")


def error_view(request):
    return http.HttpResponseServerError("Internal server error")


def permission_denied_view(request, exception):
    return http.HttpResponseForbidden("The requested directory cannot be accessed")


def bad_request_view(request, exception):
    return http.HttpResponseBadRequest("The requested directory does not exist or the parameters cannot be parsed")
