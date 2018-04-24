# Atlas API for Python

Easily send requests and work with native types for responses.

E.g.:

```python
from atlas_api import atlas_request
atlas_request.ATLAS_API_KEY = 'your API key here'

q = atlas_request('bananas', start_date='3 months ago', end_date='now', channels=['twitter', 'images'])

for day in q.sentiment():
	print(day.date, day.positive_subject_sentences)
```

The parameters to atlas_request match those listed under Query Parameters in the API documentation. If the type is a list, you can use a python list.

The endpoints are functions (e.g. q.sentiment() in the example above.) All query-based endpoints listed in the documentation are available here.

API Documentation: https://docs.google.com/document/d/1-G4AVbttUY4v5Q84zorL1y9Zjsj-oK4bFFT0mcv42yM/edit?usp=sharing