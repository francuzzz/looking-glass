# Looking Glass

Looking Glass is a Flask-based web application that allows executing network commands (ping, traceroute) from the server and displaying results in a user-friendly web interface.

## Features
- Send ICMP requests (ping) to a specified address.
- Perform traceroute to track packet routes.
- Measure latency (ping) from the browser to the server.
- Simple Bootstrap-based web interface for ease of use.

## Installation and Setup
### Requirements
- Python 3.8+
- Flask

### Installation
```sh
# Clone the repository
git clone https://github.com/francuzzz/looking-glass.git
cd looking-glass

# Install dependencies
pip install -r requirements.txt
```

### Running the Server
```sh
python app.py
```

The application will be available at: http://localhost:5000

## File Structure
```
looking-glass/
├── templates/
│   └── index.html  # HTML interface
├── app.py         # Main Flask server code
├── requirements.txt # Dependency list
├── README.md      # Project description
```

## Security
- It is recommended to run this application only in a trusted environment.
- The code uses `subprocess.run`, which may be vulnerable to injections. Future improvements should include command filtering.

## Example Nginx Configuration
```nginx
server {
    server_name YOUR_DOMAIN.TLD;

    listen IP:443 ssl;
    listen IP:443 quic;

    ssl_certificate "CERT.crt";
    ssl_certificate_key "KEY.key";
    add_header Strict-Transport-Security "max-age=31536000" always;

    http2 on;

    ssl_protocols TLSv1.2 TLSv1.3;
    add_header Alt-Svc 'h3=":443"; ma=86400';

    charset utf-8;

    gzip on;
    gzip_proxied expired no-cache no-store private auth;
    gzip_types text/css text/xml application/javascript text/plain application/json image/svg+xml image/x-icon;
    gzip_comp_level 1;

    location / {
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /execute {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    server_name YOUR_DOMAIN.TLD;
    listen IP:80;
    return 301 https://$host$request_uri;
}
```

## Systemd Service Configuration
```ini
[Unit]
Description=Looking Glass
After=network.target

[Service]
User=look
Group=look
WorkingDirectory=/var/www/look/data/www/YOUR_DOMAIN.TLD
ExecStart=/var/www/look/data/venv/bin/gunicorn --workers 2 --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

## License
This project is distributed under the MIT License.

## Contact
Author: [Your Name](https://github.com/yourusername)


