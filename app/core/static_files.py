from starlette.staticfiles import StaticFiles


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            response = await super().get_response(path, scope)
            if response.status_code == 404:
                response = await super().get_response('.', scope)
        except Exception as e:
            if path.startswith('api/'):
                raise e
            response = await super().get_response('.', scope)
        return response
