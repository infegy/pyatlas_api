# Atlas API for Python

Easily send requests and work with native types for responses.

E.g.:

```python
from atlas_api import atlas_request
atlas_request.ATLAS_API_KEY = 'your API key here'

q = atlas_request('bananas', start_date='3 months ago', end_date='now', channels=['twitter', 'images'])

for day in q.sentiment():
	print day.date.isostr(), day.positive_subject_sentences
```