import ui
import http.server
import socketserver

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler

# Open int-Webview
w = ui.WebView()
w.load_url('http://127.0.0.1:8000/feedly.html')
w.present('panel')	

# Start Web Server
with socketserver.TCPServer(("", PORT), Handler) as httpd:
	print("Web Server start at port", PORT)
	httpd.serve_forever()
	
