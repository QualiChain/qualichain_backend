### Qualichain Mediator API project

## Install project

```bash
docker-compose up -d --build
```

Access Point: `http://127.0.0.1:5000`

## API CALLS:
*  To execute a query : 
    
**URL**: http://127.0.0.1:5000/retrieve_data

**TYPE**: POST

**BODY**: {"query":"SPARQL Query String"}
 
**RETURN**: JSON

**Example**:

```http request
POST /retrieve_data HTTP/1.1
Host: qualichain.epu.ntua.gr:5000
Content-Type: application/json

{
    "query": "prefix saro: <http://w3id.org/saro/> prefix qc: <http://w3id.org/qualichain/> prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT  ?entity ?type   WHERE {   ?entity rdf:type ?type.  {?entity saro:relatedTo saro:java. }  UNION  {?entity qc:refersToExperience saro:java. }  }"
}
```

*  To submit data to the knowledge graph:

**URL**:http://127.0.0.1:5000/submit_data

**TYPE**: POST

**BODY**: {"text":"job_description"}

**Example**:

```http request
POST /submit_data HTTP/1.1
Host: qualichain.epu.ntua.gr:5000
Content-Type: application/json

{
	"text": "supervised learning, sas, web applications, meshing, dba"
}

```


## Database Interaction

1. `python manage.py db init`
2. `python manage.py db migrate`
3. `python manage.py db upgrade`

## Mediator API Endpoints Collection

You can access Mediator API endpoints from this [link](https://www.getpostman.com/collections/b1bf94313a901d799181)

## Run Content Loaders
1. Load Saro skills:
    + cd /application
    + `python loaders/ttl_loaders.py`
2. Load NTUA Courses
    + cd /application
    + `python loader/load_courses.py`
