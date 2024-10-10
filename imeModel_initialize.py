############################
# File imeModel_initialize #
############################


from serverConfig import create_conn


######################
# Internal Functions #
######################

# The code below initialize the iME original model in the following steps:
# 1- Download llama3.2v3B model from haystack.
# 2- Create iME model from the original llama3.2 model previously downloaded in the local server.
#    It is used to create a model from a Modelfile.

def _initializer(conn):
    conn.sudo('ollama run llama3.2')
    conn.sudo('ollama create iME -f ./Modelfile')
    conn.sudo('fastapi dev main.py')


def initializer(**kwargs):
    _initializer(create_conn())