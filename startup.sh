docker create -p 9200:9200 --expose 9200 -p 9300:9300 --expose 9300 --name "elasticsearch" --env "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.8.0
docker start elasticsearch

sleep 35
echo 'Creating schema...'
curl -X PUT http://localhost:9200/person \
-H 'Content-Type: application/json' \
-d '{
  "mappings": {
    "dynamic": "strict",
    "properties": {
      "name": {"first": {"type": "text"}, "last": {"type": "text"}},
      "email": {"type": "text"},
      "dob": {"type": "date"},
      "ac-number": {"type": "integer"}
    }
  }
}'

echo
echo 'Creating test data...'
curl -X POST http://localhost:9200/example/_doc \
-H 'Content-Type: application/json' \
-d '{"name": {"first": "John", "last": "Dodge"}, "email": "test2@example.org", "dob": "2019-12-12", "ac-number": 12345}'
echo
curl -X POST http://localhost:9200/example/_doc \
-H 'Content-Type: application/json' \
-d '{"name": {"first": "James", "last": "Dodge"}, "email": "test2@example.org", "dob": "2020-01-01", "ac-number": 54321}'
echo
echo 'Done!'