import subprocess

# Lista de spiders para executar
spiders = ["ingressos_spider", "sympla_spider", "ticketmaster_spider"]

for spider in spiders:
    subprocess.run(["scrapy", "crawl", spider])