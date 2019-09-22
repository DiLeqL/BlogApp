import ast


async def validate_post_fields(content):
    try:
        request_json = ast.literal_eval(content)

        if len(request_json['title']) <= 1:
            return False
        if len(request_json['body']) <= 1:
            return False
        if len(request_json['author']) <= 1:
            return False
        return True
    except KeyError:
        return False
    except SyntaxError:
        return False
