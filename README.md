### Qualichain Mediator API project

## Install project

```bash
docker-compose up -d --build
```

Access Point: `http://127.0.0.1:5000`

**API CALLS**:
*  To execute a query : 
    
**URL**:http://127.0.0.1:5000/retrieve_data

**TYPE**: POST

**BODY**: {"query":"SPARQL Query String"}
 
**RETURN**: JSON

*  To submit data to the knowledge graph:

**URL**:http://127.0.0.1:5000/submit_data

**TYPE**: POST

**BODY**: {"text":"job_description"}
    
    