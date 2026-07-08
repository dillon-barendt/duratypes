from duratypes.integrations.faststream import message_ttl_headers, retry_headers

if __name__ == "__main__":
    print(message_ttl_headers("15m"))
    print(retry_headers("30s"))
