from application.clients.qualichain_analyzer import QualiChainAnalyzer

qc_a = QualiChainAnalyzer()
print(qc_a.search_job(**{'title':'Data Scientist'}))
# print(qc_a.create_job_index().reason)