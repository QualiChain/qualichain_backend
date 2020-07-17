from application.clients.qualichain_analyzer import QualiChainAnalyzer

qc_a = QualiChainAnalyzer()

body = {
    "title": "software engineer",
    "jobDescription": "Software Engineer skilled in Python",
    "level": "entry level",
    "date": "2020-02-02",
    "startDate": "2020-02-02",
    "endDate": "2020-02-02",
    "creatorId": 1,
    "specialization": "software engineering",
    "country": "Greece",
    "state": "Ahaia",
    "city": "Patras",
    "employer": "Citrix",
    "employmentType": "full time"
}

print(qc_a.store_job(**body))
# print(qc_a.create_job_index().reason)
