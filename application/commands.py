"""
This Python script is used to execute admin commands for QualiChain Backend
"""
import logging
import sys


sys.path.append('../')

from application.clients.qualichain_analyzer import QualiChainAnalyzer

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

log = logging.getLogger(__name__)

log.info("Initialize Index for Jobs")
analyzer = QualiChainAnalyzer()
analyzer.create_job_index()
