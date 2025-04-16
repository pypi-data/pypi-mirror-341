import io
import json
from contextlib import redirect_stdout
import sys
import traceback

def capture_click_output(ctx, command, **kwargs):
    """Utility to invoke a click command and capture its output."""
    f = io.StringIO()
    with redirect_stdout(f):
        try:
            ctx.invoke(command, **kwargs)
            exit_code = 0
        except SystemExit as e:
            exit_code = e.code
    output =  f.getvalue()

    if exit_code != 0:
        raise Exception(json.loads(output)["error"])

    try:
        return json.loads(output) if output else None
    except Exception as e:
        raise Exception(f"Error parsing JSON output: {e, output}")