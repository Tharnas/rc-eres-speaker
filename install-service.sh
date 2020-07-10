#!/bin/bash

cat > /lib/systemd/system/rc-eres.service<<EOF
[Unit]
Description=RC ERES speaker Service
After=multi-user.target

[Service]
Type=idle
WorkingDirectory=$(pwd)
ExecStart=/usr/bin/python3 -m eres
User=pi

[Install]
WantedBy=multi-user.target
EOF

systemctl start rc-eres.service
systemctl enable rc-eres.service
