from boto3 import resource
from json import dumps,loads

s3 = resource("s3")

obj = s3.Object("food-data2", "food_data.json")
data = loads(obj.get()["Body"].read())


def lambda_handler(event, context):
    httpMethod = event.get('httpMethod', 'GET')
    if httpMethod != 'GET':
        if httpMethod == 'OPTIONS':
            return builtResponse(300)
        else:
            return builtResponse(400, 'ERROR: route only accepts GET requests!')
    else:
        params = event['queryStringParameters']
        if not params:
            return builtResponse(500, 'ERROR: "f" or "i" parameter required!')
        if "f" in params:
            f = params["f"]
            d = params["d"] if "d" in params else None
            c = params.get("c", None)
            k = int(params["k"]) if "k" in params else None
            response = [record for record in data if f in record["Tags"]]
            if d:
                response = [record for record in response if d.lower() in record["Diet Keywords"]]
            if c:
                response = [record for record in response if c.lower() in record["Cuisine Keywords"]]
            if k:
                try:
                    response = [record for record in response if record["Calories"] <= k]
                except:
                    pass
            return builtResponse(200,dumps(response))
            
        elif "i" in params:
            ingredients = params["i"].split(",")
            response = [record for record in data if all(ingredient in record["Ingredients"] for ingredient in ingredients)]
            d = params.get("d", None)
            c = params.get("c", None)
            k = int(params["k"]) if "k" in params else None
            if d:
                response = [record for record in response if d.lower() in record["Diet Keywords"]]
            if c:
                response = [record for record in response if c.lower() in record["Cuisine Keywords"]]
            if k:
                try:
                    response = [record for record in response if record["Calories"] <= k]
                except:
                    pass
            return builtResponse(200,dumps(response))

        else:
            return builtResponse(500, 'ERROR: "f" or "i" parameter required!') 
        

def builtResponse(statusCode, responseBody=None):
    response = {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET'
        },
        'statusCode': statusCode
    }
    if responseBody:
        response['body'] = responseBody
    return response
