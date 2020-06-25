// ES service URL
const host = 'localhost'
const port = 9200

// Read ES properties
fs = require('fs');
fs.readFile('./es/properties.json',
    'utf8', function (err,data) {
        if (err) {
        return console.log(err);
        }
        processReport(JSON.parse(data));
    });

// Process ES query
function processReport(properties) {
    // Define ES client properties
    const url = 'http://' + host + ':' + port + '/';
    var elasticsearch = require('elasticsearch');
    var client = new elasticsearch.Client({
        host: url,
        log: 'trace',
        auth: {
            username: properties.user_id,
            password: properties.password
        }
    });

    // Process query
    client.search({
        index: properties.index,
        body: properties.query_dsl
    }).then(function(body) {
        if (!body) {
            console.log('No response body!');
        } else {
            outputData(properties.export, body.hits.hits);
        }
    }, function(err) {
        console.trace(err.message);
    });
}

// Output response to CSV
function outputData(headers, response) {
    var fs = require('fs');
    var stream = fs.createWriteStream('output.csv');
    var str = 'Hits: ' + Object.keys(response).length + '\n' + headers.valueOf() + '\n';
    
    // Format response for CSV
    if (!response) {
        console.log('No response!');
    } else {
        response.forEach(hit => {
            var temp = '';
            headers.forEach(attribute => {
                var paths = attribute.split(".");
                var value;
                paths.forEach(path=>{
                    value = typeof value == 'object' ? value[path] : hit._source[path];
                });
                temp += (typeof value == 'undefined' ? "Invalid property" : value) + ',';
            });
            temp = temp.slice(0, -1) + '\n';
            str += temp;
        });
        stream.write(str);
    }
    stream.end();
}