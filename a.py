from pyngrok import ngrok

# Open a tunnel to your Django app (running on port 8000)
http_tunnel = ngrok.connect(8000)
print(f"Public URL: {http_tunnel.public_url}")  # This prints the ngrok URL
