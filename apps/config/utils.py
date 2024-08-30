from .models import msg_queue

def add_to_msg_queue(
    source: str,
    source_id: int,
    destination: str,
    process:str,
    **kwargs
):
    new_msg = msg_queue.objects.create(
        source = source,
        source_id = source_id,
        destination = destination,
        process = process,
        flag = 'N'
    )

    if 'routine' in kwargs:
        new_msg.routine = kwargs['routine']
    if 'arg1' in kwargs:
        new_msg.arg1 = kwargs['arg1']
    if 'arg2' in kwargs:
        new_msg.arg2 = kwargs['arg2']
    if 'arg3' in kwargs:
        new_msg.arg3 = kwargs['arg3']
    if 'arg4' in kwargs:
        new_msg.arg4 = kwargs['arg4']

    new_msg.save()
    return new_msg