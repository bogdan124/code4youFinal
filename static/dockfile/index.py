##https://www.programcreek.com/python/example/107511/docker.DockerClient
import docker
client = docker.from_env()
container = client.images.build()
print (container)


