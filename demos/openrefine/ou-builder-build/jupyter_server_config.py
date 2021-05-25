


    
        
c.ServerApp.default_url = 'openrefine'
        
    

c.ServerProxy.servers = {
    
    'openrefine': {
        'command': ['/var/openrefine/openrefine-3.3/refine', '-i', '0.0.0.0', '-p', '{port}', '-d', '/home/ou-user/OpenRefine'],
        
        
        'timeout': 120,
        
    },
    
}
