import ast


async def validate_post_fields(request):
    try:
        content = await request.content.read()
        request_json = ast.literal_eval(str(content, 'UTF-8'))

        if len(request_json['title']) <= 1:
            print(len(request_json['title']))
            return False
        if len(request_json['body']) <= 1:
            print(len(request_json['bo']))
            return False
        if len(request_json['author']) <= 1:
            print(len(request_json['title']))
            return False
        return True
    except KeyError:
        return False
    except SyntaxError:
        return False
