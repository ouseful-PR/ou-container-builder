{% if packs and 'tutorial-server' in packs %}
c.ServerApp.default_url = 'tutorial-server'

c.ServerProxy.servers = {
    'tutorial-server': {
        'command': [ 'python', '-m' 'tutorial_server', '--config=/etc/tutorial-server/production.ini', '--port={port}', '--basepath={base_url}tutorial-server/', ],
        'absolute_url': True,
    }
}
{% endif %}
