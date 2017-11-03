"""
	file: wolf_module.py
	author: Ellis Wright
	language: python3.6
	description: Simple implementation of wolfram alpha api to return
	the results of queries to the site.

	NOTES: Return query is structured as follows.
	Result -> [Pods] -> [SubPods] -> "Text"
"""
import Python_Binding_1_1.wap.py

client = wolframalpha.Client('URQ5WU-K3TRKE2JHW')

def get_results(qry):
	"""
		String -> Array<Pods>
		Function takes a string  and sends it to wolfram alpha for
		processing. Then returns the pods recieved in return.
	"""
	res = client.query(qry)
	return [pod for pod in res.pods]#All pods are dictionary subclasses


if __name__ == "__main__":
	res = get_results(input("Enter a query: "))
	for pod in res:
		for sub in pod.subpods:
			print(sub.text)
