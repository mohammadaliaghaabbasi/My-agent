import urllib.request
url = "https://api.telegram.org/bot8760014581:AAFb8j7tR6r_0uLqup9SjqT_7tM-tf3LRRs/deleteWebhook?drop_pending_updates=true"
print(urllib.request.urlopen(url).read().decode())
