import hashlib
import hmac
import base64
from datetime import datetime

contentLength = '62'
contentType = 'application/xml'
storageKey = ''

# Setting x-ms-date header with the current date in UTC
headers = {
    'x-ms-date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
    'x-ms-version': '2015-02-21'
}

def format_headers(headers):
    return '\n'.join([f"{header}:{headers.get(header)}" for header in headers])

# Simulating pm.request.url.toString() and extracting path, acc, res, queryParams
url = 'https://tenant.queue.core.windows.net/queue-name/messages?visibilitytimeout=30&timeout=30'
path = url.split('?')[0]
acc = path.split('://')[1].split('.')[0]
res = path.split('.net/')[1]

query_params = {}
query_string = url.split('?')[1] if '?' in url else None
if query_string:
    for pair in query_string.split('&'):
        key_value = pair.split('=')
        key = key_value[0]
        value = key_value[1] if len(key_value) > 1 else ''
        if key not in query_params:
            query_params[key] = []
        query_params[key].append(value)

sorted_query_params = '\n'.join([f"{key}:{','.join(sorted(query_params[key]))}" for key in sorted(query_params)])

# Constructing CanonicalizedResource
canonicalized_resource = f"\n/{acc}/{res}\n{sorted_query_params}"

# Constructing StringToSign
string_to_sign = f"POST\n\n\n{contentLength}\n\n{contentType}\n\n\n\n\n\n\n" + \
                 format_headers(headers) + \
                 canonicalized_resource

# Encoding StringToSign to UTF-8
utf8_encoded_string = string_to_sign.encode('utf-8')
decoded_storage_key = base64.b64decode(storageKey)

# Creating an HMAC object with SHA256 hash and computing the signature
hmac_obj = hmac.new(decoded_storage_key, utf8_encoded_string, hashlib.sha256)
signature = base64.b64encode(hmac_obj.digest()).decode()

# Constructing Authorization header value
authorization_header = f"SharedKey {acc}:{signature}"

# Adding Authorization header to the request headers
headers['Authorization'] = authorization_header

# Adding content type and content length to the request headers
headers['Content-Type'] = contentType
# headers['Content-Length'] = contentLength

import requests
response = requests.post(url, headers=headers, data='<QueueMessage><MessageText>test 2</MessageText></QueueMessage>')

#printing the resulting response
print("\n\nResponse:")
print(response.status_code)
print(response.text)
