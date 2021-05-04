{% if packs and 'tutorial-server' in packs %}
c.ServerApp.default_url = 'tutorial-server'

c.ServerProxy.servers = {
    'tutorial-server': {
        'command': [ 'python', '-m' 'tutorial_server', '--config=/etc/tutorial-server/production.ini', '--port={port}', '--basepath={base_url}tutorial-server/', ],
        'absolute_url': True,
    }
}
{% endif %}

{% if web_apps %}
    {% for app in web_apps %}
        {% if app.default %}
c.ServerApp.default_url = '{{ app.path }}'
        {% endif %}
    {% endfor %}

c.ServerProxy.servers = {
    {% for app in web_apps %}
    '{{ app.path }}': {
        'command': {{ app.cmdline }},
        {% if app.port %}
        'port': app.port,
        {% endif %}
        {% if app.timeout %}
        'timeout': {{ app.timeout }},
        {% endif %}
    },
    {% endfor %}
}
{% endif %}
