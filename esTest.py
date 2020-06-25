import os, json, requests
from elasticsearch import Elasticsearch

def main():
    host = 'localhost'
    port = 9200

    # Get properties for query
    props = loadProperties()

    # Check if ES is running
    url = 'http://' + props['user_id'] + ':' + props['password'] + '@' + host + ':' + str(port)
    res = requests.get(url)
    if res.status_code == 200:
        # ES is running: query for results
        output = search(host, port, props)
        # Write results to CSV file
        text_file = open("output.csv", "w")
        n = text_file.write(output)
        text_file.close()
    else:
        print('Bad connection status:' + res.status_code)
    print("Done!")

def loadProperties():
    data = ''
    if os.name == 'nt': # Windows
        with open ("es\\properties.json", "r") as file:
            data = file.read().replace('\n', '')
    elif os.name == 'posix': # Linux/Mac
        with open ("./es/properties.json", "r") as file:
            data = file.read().replace('\n', '')
    else:
        print('OS type not currently used!')
        exit()
    return json.loads(data)

# elasticsearch function
def search(host, port, props):
    # Connect to host and query
    es = Elasticsearch([{'host': host, 'port': str(port)}], http_auth=(props['user_id'], props['password']))
    results = (es.search(index=props["index"], body=props["query_dsl"]))['hits']['hits']
    data = 'Hits: ' + str(len(results)) + '\n' + ','.join(props['export']) + '\n'

    # Check for matches in response
    if len(results) != 0:
        for hit in results:
            temp = ''
            # Find needed values through exports
            for attributes in props['export']:
                paths = attributes.split('.')
                value = None
                # Loop through nested paths (if present)
                for path in paths:
                    value = value.get(path) if type(value) == dict else hit['_source'].get(path)
                # Concatinate value if not 'None'
                temp += str(value) + ',' if value != None else 'Invalid Property,'
            index = temp.rfind(",")
            data += temp[:index] + '\n'
    return data

if __name__ == "__main__":
    main()