from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": str(error),
                }
            ),
            400,
        )

    @app.errorhandler(TypeError)
    def handle_type_error(error):
        return (
            jsonify(
                {
                    "success": False,
                    "message": str(error),
                }
            ),
            400,
        )
