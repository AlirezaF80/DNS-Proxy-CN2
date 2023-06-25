import time

class cache:
    def __init__(self, hostname):
        self.cache = {}
        self.hostname = hostname

    def add_record(self, hostname, ip_address, ttl):
        expiration_time = time.time() + ttl
        self.cache[hostname] = (ip_address, expiration_time)
        self.save_hostname_to_file(hostname)

    def get_record(self, hostname):
        if hostname in self.cache:
            ip_address, expiration_time = self.cache[hostname]
            if expiration_time > time.time():
                return ip_address
            else:
                del self.cache[hostname]
        return None

    def remove_record(self, hostname):
        if hostname in self.cache:
            del self.cache[hostname]
            self.remove_hostname_from_file(hostname)

    def clear_cache(self):
        self.cache = {}
        self.clear_hostname_file()

    def save_hostname_to_file(self, hostname):
        with open(f"{self.hostname}_hostnames.txt", "a") as file:
            file.write(hostname + "\n")

    def remove_hostname_from_file(self, hostname):
        filename = f"{self.hostname}_hostnames.txt"
        with open(filename, "r") as file:
            lines = file.readlines()
        with open(filename, "w") as file:
            for line in lines:
                if line.strip() != hostname:
                    file.write(line)

    def clear_hostname_file(self):
        filename = f"{self.hostname}_hostnames.txt"
        with open(filename, "w") as file:
            pass

    def main(self):
        # Create an instance of the Cache class
        Cache = cache("example")

        Cache.add_record("example.com", "192.168.0.1", 60)
        print(Cache.get_record("example.com"))  # Expected output: 192.168.0.1

        Cache.add_record("example2.com", "192.168.0.2", 60)
        print(Cache.get_record("example2.com"))  # Expected output: 192.168.0.2

        Cache.remove_record("example2.com")
        print(Cache.get_record("example2.com"))  # Expected output: None

        Cache.clear_cache()
        print(Cache.get_record("example.com"))  # Expected output: None

    if __name__ == "__main__":
        main()