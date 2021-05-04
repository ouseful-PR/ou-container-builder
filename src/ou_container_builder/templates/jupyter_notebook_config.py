c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.notebook_dir = '/home/ou-user/{{ module.code }}-{{ module.presentation }}'
c.NotebookApp.open_browser = False
c.NotebookApp.quit_button = False
c.JupyterHub.shutdown_on_logout
c.NotebookApp.iopub_data_rate_limit = 10000000
c.MappingKernelManager.cull_idle_timeout = 1200
c.MappingKernelManager.cull_interval = 10
{% if jupyter_notebook and 'default_url' in jupyter_notebook %}
c.NotebookApp.default_url = '{{ jupyter_notebook['default_url'] }}'
{% endif %}

{% if packs and 'tutorial-server' in packs %}
c.ServerProxy.servers = {
    'tutorial-server': {
        'command': [ 'python', '-m' 'tutorial_server', '--config=/etc/tutorial-server/production.ini', '--port={port}', '--basepath={base_url}tutorial-server/', ],
        'absolute_url': True,
    }
}
{% endif %}

{% if web_apps %}
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
