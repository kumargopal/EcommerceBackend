# swagger_custom.py

from drf_yasg.inspectors import SwaggerAutoSchema

class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_security_definitions(self, auto_schema):
        return {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
            }
        }
