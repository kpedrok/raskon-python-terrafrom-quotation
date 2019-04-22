import json

json_data = json.dumps({
    "result": [
        {
            "run": [
                {
                    "action": "stop"
                },
                {
                    "action": "start"
                },
                {
                    "action": "start"
                }
            ],
            "find": "true"
        }
    ]
})

item_dict = json.loads(json_data)
print (len(item_dict['result'][0]['run']))
