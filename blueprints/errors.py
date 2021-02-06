from flask import jsonify

from blueprints import api_bp


@api_bp.errorhandler(404)
def not_found(e):
    print('api.errors.not_found ', e)
    error_info = '{}'.format(e)
    response = jsonify({'error': error_info})
    response.status_code = 404

    return response


@api_bp.errorhandler(403)
def fobidden(e):
    print(e)
    error_info = '{}'.format(e)
    response = jsonify({'error': error_info})
    response.status_code = 403
    return response