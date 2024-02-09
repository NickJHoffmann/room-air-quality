import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from room_air_quality.config import ServerSettings

def main():
    s = ServerSettings()
    client = influxdb_client.InfluxDBClient(url=s.influxdb_url, token=s.influxdb_token.get_secret_value(), org=s.influxdb_org)

    bucket="Test Bucket"

    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    for value in range(5):
        point = (
            Point("measurement1")
            .tag("tagname1", "tagvalue1")
            .field("field1", value)
        )
        write_api.write(bucket=bucket, org="Test Org", record=point)
        print(f"Writing point: {point.to_line_protocol()}")
        time.sleep(1) # separate points by 1 second

    query_api = client.query_api()

    query = """from(bucket: "Test Bucket")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "measurement1")
    |> mean()"""
    tables = query_api.query(query, org="Test Org")

    for table in tables:
        for record in table.records:
            print(record)



if __name__ == "__main__":
    main()
