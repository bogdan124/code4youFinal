##from docker import Client
##cli = Client(base_url='unix://var/run/docker.sock')
##container = cli.create_container(image='python', command='/bin/sleep 30')
##print(container['Id'])

from io import BytesIO
from docker import Client
import commands


##sudo docker rmi $(sudo docker images --filter 'dangling=true' -q --no-trunc)

class print_code_results:
	def __init__(self,url_folder_language):
		cli = Client(base_url='unix://var/run/docker.sock')
		response = cli.build(path=url_folder_language,rm=True,nocache=True)
		for i in response:
			j=i[30:]
		id_container=j[:12]
		self.id_container=id_container		
	def show_result(self):
		return_result=commands.getstatusoutput("sudo docker run "+self.id_container)
		commands.getstatusoutput("sudo docker rm $(sudo docker ps -a -q)")
		commands.getstatusoutput("sudo docker rmi $(sudo docker images --filter 'dangling=true' -q --no-trunc)")
		return return_result







##for i in response2:
##	this_d=list(i.values())
##print(this_d[11])
##print(inspect_container(this_d))

