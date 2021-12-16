import logging
import os
import boto3
from botocore.exceptions import ClientError
import pika
import json

def create_presigned_url(object_name):
    """Generate a presigned URL to share an S3 object with a capped expiration of 60 seconds

    :param object_name: string
    :return: Presigned URL as string. If error, returns None.
    """
    s3_client = boto3.client('s3',
                             region_name=os.environ.get('S3_PERSISTENCE_REGION'),
                             config=boto3.session.Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    try:
        bucket_name = os.environ.get('S3_PERSISTENCE_BUCKET')
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=60*1)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
    
def rabbitmq_test(cmd_type,data):
    credentials = pika.PlainCredentials('advaint_mq', 'advaint101')
    parameters = pika.ConnectionParameters('54.188.246.255',
    		                               5672,
    		                               '/',
    		                               credentials)
        #connection = pika.BlockingConnection(pika.ConnectionParameters(host='13.126.152.234'))
        
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    #channel.queue_declare(queue='customer_1', durable=True)
    channel.exchange_declare(exchange='exchange_1', exchange_type='topic', durable=True)
    #sys.argv[1]
    #"allonoff.1.advaint"
    ##if len(sys.argv) > 2 else 'anonymous.info'
    #message = ' '.join(sys.argv[2:]) or 'Hello World!'
    """
    message = json.dumps({"zone_id":None,
                       
                       "event_id":1,
                       "output_type_id":1,
                      
                       "parameter":1
                       })
    """
    if cmd_type=="scene":
        routing_key =  "scene.1.advaint"
        message = json.dumps({"scene_id":data[0], "parameter":data[1], "zone_id":data[2]})
    elif cmd_type=="device":
        routing_key =  "allonoff.1.advaint"
        message = json.dumps({"event_id":data[0], "output_type_id":None, "parameter":data[1], "zone_id":data[2]})
    elif cmd_type=="types":
        routing_key =  "allonoff.1.advaint"
        message = json.dumps({"zone_id":data[2],"output_type_id":data[0],"event_id":None, "parameter":data[1]})
    channel.basic_publish(
        exchange='exchange_1', routing_key=routing_key, body=message)
    print(" [x] Sent %r:%r" % (routing_key, message))
    connection.close()
    

    