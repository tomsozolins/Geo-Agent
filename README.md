## Fetches data from Zabbix and indexes to Elasticsearch Maps index
--------------------------------------------
CLONE GIT REPOSITORY
# git clone https://github.com/tomsozolins/geo-agent.git
--------------------------------------------

DOCKER SWARM GEO AGENT STACK DEPLOYMENT

# docker-compose -f docker-compose-geo-agent.yaml build
# docker-compose -f docker-compose-geo-agent.yaml push
# docker stack deploy --compose-file docker-compose-geo-agent.yaml geo_agent_stack

