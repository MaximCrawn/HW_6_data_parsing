from urllib.parse import unquote

encoded_url = "https://plus.unsplash.com/premium_photo-1682629632657-4ac307921295?q=80&w=726&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
decoded_url = unquote(encoded_url)
print(decoded_url)
