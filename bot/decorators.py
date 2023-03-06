import grpc


def grpc_error_decorator(func):
    async def decorate(*args):
        try:
            await func(*args)
        except grpc.aio.AioRpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                await args[0].answer(text=e.details())

    return decorate
