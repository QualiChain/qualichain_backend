from application.clients.qualichain_analyzer import QualiChainAnalyzer

qc_a = QualiChainAnalyzer()
print(qc_a.create_job_index().reason)