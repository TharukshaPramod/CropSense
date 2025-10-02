# predictor/worker.py
import pika, json, os, subprocess

def on_message(ch, method, properties, body):
    msg = json.loads(body)
    features_path = msg.get("features_path")
    print("Received features_ready:", features_path)
    subprocess.run(["python", "predictor/train.py"], check=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    params = pika.URLParameters(url)
    conn = pika.BlockingConnection(params)
    ch = conn.channel()
    ch.queue_declare(queue="features_ready", durable=True)
    ch.basic_qos(prefetch_count=1)
    ch.basic_consume("features_ready", on_message)
    print("Waiting for features_ready messages...")
    ch.start_consuming()

if __name__ == "__main__":
    main()
