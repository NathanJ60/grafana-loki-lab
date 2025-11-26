#!/usr/bin/env python3
import random
import time
import os
from datetime import datetime
from faker import Faker

fake = Faker()

LOG_FILE = os.environ.get('LOG_FILE', '/logs/app.log')
LOG_LEVELS = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LEVEL_WEIGHTS = [10, 50, 20, 15, 5]

INFO_MESSAGES = [
    lambda: f"User {fake.user_name()} logged in successfully",
    lambda: f"Request processed in {random.randint(10, 500)}ms",
    lambda: f"New session started for user {fake.user_name()}",
    lambda: f"API call to {fake.uri_path()} completed",
    lambda: f"Cache hit for key {fake.uuid4()[:8]}",
    lambda: f"Database query executed in {random.randint(1, 100)}ms",
    lambda: f"File {fake.file_name()} uploaded successfully",
    lambda: f"Email sent to {fake.email()}",
    lambda: f"Payment processed for order #{random.randint(10000, 99999)}",
    lambda: f"User {fake.user_name()} updated their profile",
]

DEBUG_MESSAGES = [
    lambda: f"Checking authentication for token {fake.uuid4()[:12]}...",
    lambda: f"Loading configuration from {fake.file_path()}",
    lambda: f"Memory usage: {random.randint(100, 800)}MB",
    lambda: f"Active connections: {random.randint(1, 100)}",
    lambda: f"Cache size: {random.randint(1000, 50000)} entries",
    lambda: f"Processing batch {random.randint(1, 100)} of {random.randint(100, 200)}",
]

WARNING_MESSAGES = [
    lambda: f"High memory usage detected: {random.randint(80, 95)}%",
    lambda: f"Slow query detected: {random.randint(500, 2000)}ms",
    lambda: f"Rate limit approaching for IP {fake.ipv4()}",
    lambda: f"Deprecated API endpoint called: {fake.uri_path()}",
    lambda: f"Connection pool running low: {random.randint(1, 5)} available",
    lambda: f"Retry attempt {random.randint(1, 3)} for external service",
    lambda: f"Session expiring soon for user {fake.user_name()}",
]

ERROR_MESSAGES = [
    lambda: f"Failed to connect to database: Connection refused",
    lambda: f"Authentication failed for user {fake.user_name()}",
    lambda: f"Invalid request payload from {fake.ipv4()}",
    lambda: f"Timeout waiting for response from {fake.domain_name()}",
    lambda: f"File not found: {fake.file_path()}",
    lambda: f"Permission denied for resource {fake.uri_path()}",
    lambda: f"API rate limit exceeded for client {fake.uuid4()[:8]}",
    lambda: f"Failed to parse JSON: Unexpected token at position {random.randint(1, 100)}",
    lambda: f"External service unavailable: {fake.domain_name()}",
]

CRITICAL_MESSAGES = [
    lambda: f"SYSTEM FAILURE: Database cluster unreachable",
    lambda: f"CRITICAL: Out of memory - emergency shutdown initiated",
    lambda: f"FATAL: Disk space exhausted on /var/log",
    lambda: f"SECURITY ALERT: Multiple failed login attempts from {fake.ipv4()}",
    lambda: f"CRITICAL: SSL certificate expired for {fake.domain_name()}",
    lambda: f"FATAL: Unhandled exception in main thread",
]

MESSAGES = {
    'DEBUG': DEBUG_MESSAGES,
    'INFO': INFO_MESSAGES,
    'WARNING': WARNING_MESSAGES,
    'ERROR': ERROR_MESSAGES,
    'CRITICAL': CRITICAL_MESSAGES,
}


def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def generate_log_line():
    level = random.choices(LOG_LEVELS, weights=LEVEL_WEIGHTS, k=1)[0]
    message_func = random.choice(MESSAGES[level])
    message = message_func()
    return f"[{get_timestamp()}] {level} - {message}"


def simulate_incident():
    """Generate a burst of errors to simulate an incident"""
    print("Simulating incident burst...")
    for _ in range(random.randint(20, 50)):
        level = random.choice(['ERROR', 'CRITICAL'])
        message_func = random.choice(MESSAGES[level])
        message = message_func()
        log_line = f"[{get_timestamp()}] {level} - {message}"
        write_log(log_line)
        time.sleep(random.uniform(0.05, 0.2))


def write_log(log_line):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + '\n')
    print(log_line)


def main():
    print(f"Starting log generator, writing to {LOG_FILE}")
    log_count = 0

    while True:
        log_line = generate_log_line()
        write_log(log_line)
        log_count += 1

        if log_count % 100 == 0 and random.random() < 0.3:
            simulate_incident()

        sleep_time = random.uniform(0.5, 3.0)
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
