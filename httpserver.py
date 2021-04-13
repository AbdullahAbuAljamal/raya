import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import csv
from datetime import datetime
from azure.storage.blob import ContainerClient
import os
i = 0

def datalister( string ):
	switch = -1
	elements = []
	for i in range(0, len(string)):
		if string[i] == "'":
			switch = switch * (-1)
			for j in range(i + 1, len(string)):
				if (string[j] == "'") & (switch == 1):
					elements.append(string[i + 1:j])
					# print(string[i+1:j])

					break
	return elements



def CSVwriter(weathFile, accelsFile,touchsFile,lightFile,elements):
	with open(touchsFile, mode='w') as employee_file:
		writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["time", "reading"])
		for i in range(0, len(elements)):
			if elements[i] == "touches":
				for j in range(i, len(elements)):
					if elements[j] == "value":
						writer.writerow([elements[j + 3], elements[j + 1]])
					if elements[j] == "accels":
						break

	with open(weathFile, mode='w') as employee_file:
		writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["time", "temperature", "humidity", "pressure"])
		for i in range(0, len(elements)):
			if elements[i] == "weathers":
				for j in range(i, len(elements)):
					if elements[j] == "temperature":
						writer.writerow([elements[j + 7], elements[j + 1], elements[j + 3], elements[j + 5]])
					if elements[j] == "lights":
						break

	with open(lightFile, mode='w') as employee_file:
		writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["time", "reading"])
		for i in range(0, len(elements)):
			if elements[i] == "lights":
				for j in range(i, len(elements)):
					if elements[j] == "light":
						writer.writerow([elements[j + 3], elements[j + 1]])

	with open(accelsFile, mode='w') as employee_file:
		writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["type", "x", "y", "z"])
		for i in range(0, len(elements)):
			if elements[i] == "accels":
				for j in range(i, len(elements)):
					if elements[j] == "y":
						writer.writerow([elements[j + 5], elements[j + 9], elements[j + 1], elements[j + 3]])
					if elements[j] == "weathers":
						break



class S(BaseHTTPRequestHandler):


    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        logging.info(
            "GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers)
        )
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def get_files(self, dirName):
        with os.scandir(dirName) as entries:
            for entry in entries:
                if entry.is_file() and not entry.name.startswith('.'):
                    yield entry

    def upload(self, files, connection_string, container_name):
        container_client = ContainerClient.from_connection_string(connection_string, container_name)
        print("uploading")
        for file in files:
            blob_client = container_client.get_blob_client(file.name)
            with open(file.path, "rb") as data:
                blob_client.upload_blob(data)
                print(f'{file.name} uploaded')

    def do_POST(self):
        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        data = parse_qs(post_data.decode(),keep_blank_values=1)
        stringData = str(data)
        global i
        csv_file = "/home/abdzallah/Data/data" + "test" + ".csv"
        i = i + 1
        weathFile = "/home/abdzallah/Data/weathData" + str(i) + ".csv"
        accelsFile = "/home/abdzallah/Data/accelData" + str(i) + ".csv"
        touchsFile = "/home/abdzallah/Data/touchesRecord" + str(i) + ".csv"
        lightFile = "/home/abdzallah/Data/lightData" + str(i) + ".csv"
        dataElements = DataLister(stringData)
        CSVwriter(weathFile, accelsFile,touchsFile,lightFile,dataElements)
#        with open(csv_file , 'w', newline='') as file:
#             writer = csv.writer(file, quoting=csv.QUOTE_ALL,delimiter=';')
#             writer.writerows(valueslist)
#             for i in range(0,len(xx)):
 #                w = csv.DictWriter(file,xx[i].keys())
  #               w.writerow(xx[i])
   #     files = self.get_files('/home/abdzallah/Data')
    #    self.upload(files,"DefaultEndpointsProtocol=https;AccountName=abdzallah;AccountKey=6Z2LBZjx7YJjhpzF8VRer0SREGSSHFPN5kpO10HRoV5xfk+0m2STWc06jTsrOCYQVIt1095VChtL7qJ9jy0Duw==;EndpointSuffix=core.windows.net","nayan")


        logging.info(
                "POST request,\nPath: %s\nHeaders:\n%s\n\nType: \n %s\nBody:\n%s\n",
            str(self.path),
            str(self.headers),
            type(stringdata),
            stringdata
        )

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
