def basic(opts_str: str = ""):
    return f"""from fasthtml.common import *

app,rt = fast_app{opts_str}

@rt('/')
def get(): return Div(P("Hello, world!!"))

serve()"""