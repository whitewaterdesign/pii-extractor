logs_with_labels = [
    (
        {
            "timestamp": "2026-01-24T09:12:03.114Z",
            "level": "INFO",
            "service": {"name": "api-gateway", "version": "2.8.1", "environment": "prod"},
            "host": {"hostname": "edge-01", "ip": "10.12.0.11"},
            "log": {"logger": "http.access", "thread": "http-nio-8080-exec-7"},
            "trace": {"trace_id": "4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c", "span_id": "0a1b2c3d4e5f6789"},
            "correlation_id": "corr-8f2b6f2c4a",
            "http": {
                "method": "GET",
                "path": "/v1/health",
                "status_code": 200,
                "client_ip": "10.0.4.20",
                "user_agent": "kube-probe/1.27",
                "latency_ms": 4,
            },
            "user": {"id": "u-1029", "role": "system"},
            "event": {"type": "healthcheck", "outcome": "success", "entity": "service", "entity_id": "api-gateway"},
            "security": {"auth_method": "none", "mfa": None},
            "data_classification": "internal",
            "message": "Health check ok",
            "extra": {"region": "eu-west"},
        },
        [],
    ),

    # 2) EMAIL_ADDRESS (appears only in message)
    (
        {
            "timestamp": "2026-01-24T09:12:10.552Z",
            "level": "INFO",
            "service": {"name": "auth-service", "version": "1.14.0", "environment": "prod"},
            "host": {"hostname": "auth-03", "ip": "10.12.3.19"},
            "log": {"logger": "auth.audit", "thread": "worker-12"},
            "trace": {"trace_id": "a1b2c3d4e5f60718293a4b5c6d7e8f90", "span_id": "1122334455667788"},
            "correlation_id": "corr-1a9c0f77bd",
            "http": {"method": "POST", "path": "/v1/auth/password-reset", "status_code": 202, "client_ip": "10.0.7.31", "user_agent": "internal-client/4.2", "latency_ms": 31},
            "user": {"id": "u-7741", "role": "user"},
            "event": {"type": "password_reset", "outcome": "requested", "entity": "account", "entity_id": "u-7741"},
            "security": {"auth_method": "password", "mfa": False},
            "data_classification": "confidential",
            "message": "Password reset requested for sam.ritchie@example.co.uk",
            "extra": {"rate_limited": False},
        },
        [[("EMAIL_ADDRESS", "sam.ritchie@example.co.uk")]],
    ),

    # 3) No labelled data
    (
        {
            "timestamp": "2026-01-24T09:12:18.003Z",
            "level": "WARN",
            "service": {"name": "orders-service", "version": "3.3.0", "environment": "prod"},
            "host": {"hostname": "orders-02", "ip": "10.12.5.22"},
            "log": {"logger": "orders.controller", "thread": "http-nio-8080-exec-2"},
            "trace": {"trace_id": "0f0e0d0c0b0a09080706050403020100", "span_id": "99aabbccddeeff00"},
            "correlation_id": "corr-64d3a1c2ee",
            "http": {"method": "GET", "path": "/v1/orders/recent", "status_code": 504, "client_ip": "10.0.6.10", "user_agent": "internal-client/4.2", "latency_ms": 30000},
            "user": {"id": "u-2081", "role": "user"},
            "event": {"type": "order_list", "outcome": "timeout", "entity": "order", "entity_id": None},
            "security": {"auth_method": "token", "mfa": None},
            "data_classification": "internal",
            "message": "Upstream timeout while listing recent orders",
        },
        [],
    ),

    # 4) NAME + SURNAME (only in message)
    (
        {
            "timestamp": "2026-01-24T09:12:24.881Z",
            "level": "INFO",
            "service": {"name": "user-service", "version": "5.0.2", "environment": "prod"},
            "host": {"hostname": "users-01", "ip": "10.12.2.10"},
            "log": {"logger": "users.audit", "thread": "http-nio-8080-exec-9"},
            "trace": {"trace_id": "1234567890abcdef1234567890abcdef", "span_id": "0102030405060708"},
            "correlation_id": "corr-2b7c1e9ad4",
            "http": {"method": "POST", "path": "/v1/users", "status_code": 201, "client_ip": "10.0.9.44", "user_agent": "internal-client/4.2", "latency_ms": 58},
            "user": {"id": "u-3007", "role": "admin"},
            "event": {"type": "user_create", "outcome": "success", "entity": "user", "entity_id": "u-9912"},
            "security": {"auth_method": "sso", "mfa": True},
            "data_classification": "confidential",
            "message": "New user created: Thomas Reed",
        },
        [[("NAME", "Thomas"), ("SURNAME", "Reed")]],
    ),

    # 5) POSTCODE (only in endpoint path)
    (
        {
            "timestamp": "2026-01-24T09:12:31.420Z",
            "level": "INFO",
            "service": {"name": "address-service", "version": "1.9.4", "environment": "prod"},
            "host": {"hostname": "addr-02", "ip": "10.12.6.18"},
            "log": {"logger": "address.lookup", "thread": "http-nio-8080-exec-4"},
            "trace": {"trace_id": "abcdefabcdefabcdefabcdefabcdefabcd", "span_id": "deadbeefcafef00d"},
            "correlation_id": "corr-7c5f0c3b11",
            "http": {"method": "GET", "path": "/v1/postcodes/SW1A 1AA", "status_code": 200, "client_ip": "10.0.8.12", "user_agent": "internal-client/4.2", "latency_ms": 22},
            "user": {"id": "u-5510", "role": "user"},
            "event": {"type": "postcode_lookup", "outcome": "success", "entity": "postcode", "entity_id": "lookup"},
            "security": {"auth_method": "token", "mfa": None},
            "data_classification": "internal",
            "message": "Postcode lookup succeeded",
        },
        [[("POSTCODE", "SW1A 1AA")]],
    ),

    # 6) No labelled data
    (
        {
            "timestamp": "2026-01-24T09:12:39.091Z",
            "level": "DEBUG",
            "service": {"name": "billing-service", "version": "2.1.0", "environment": "prod"},
            "host": {"hostname": "bill-01", "ip": "10.12.7.13"},
            "log": {"logger": "billing.reconcile", "thread": "scheduler-1"},
            "trace": {"trace_id": "ffeeddccbbaa00998877665544332211", "span_id": "0011223344556677"},
            "correlation_id": "corr-0c1e2a9f77",
            "http": {"method": "POST", "path": "/v1/billing/reconcile", "status_code": 200, "client_ip": "10.0.0.1", "user_agent": "scheduler/1.0", "latency_ms": 140},
            "user": {"id": "u-1029", "role": "system"},
            "event": {"type": "reconcile", "outcome": "started", "entity": "billing", "entity_id": "batch"},
            "security": {"auth_method": "m2m", "mfa": None},
            "data_classification": "internal",
            "message": "Reconciliation job started",
        },
        [],
    ),

    # 7) NHS_NUMBER (only in message)
    (
        {
            "timestamp": "2026-01-24T09:12:45.660Z",
            "level": "WARN",
            "service": {"name": "records-service", "version": "0.8.9", "environment": "prod"},
            "host": {"hostname": "rec-01", "ip": "10.12.9.21"},
            "log": {"logger": "records.access", "thread": "http-nio-8080-exec-6"},
            "trace": {"trace_id": "0a0b0c0d0e0f10111213141516171819", "span_id": "aabbccddeeff0011"},
            "correlation_id": "corr-3aa1d9c0f2",
            "http": {"method": "GET", "path": "/v1/records/search", "status_code": 404, "client_ip": "10.0.2.77", "user_agent": "internal-client/4.2", "latency_ms": 19},
            "user": {"id": "u-2230", "role": "clinician"},
            "event": {"type": "record_search", "outcome": "not_found", "entity": "record", "entity_id": "search"},
            "security": {"auth_method": "sso", "mfa": True},
            "data_classification": "restricted",
            "message": "No record found for NHS number 485 722 9031",
        },
        [[("NHS_NUMBER", "485 722 9031")]],
    ),

    # 8) PHONE_NUMBER (only in message)
    (
        {
            "timestamp": "2026-01-24T09:12:53.118Z",
            "level": "INFO",
            "service": {"name": "support-service", "version": "1.3.7", "environment": "prod"},
            "host": {"hostname": "support-02", "ip": "10.12.10.5"},
            "log": {"logger": "support.ticket", "thread": "http-nio-8080-exec-1"},
            "trace": {"trace_id": "1122aabb3344ccdd5566eeff77889900", "span_id": "8899aabbccddeeff"},
            "correlation_id": "corr-51d0c2a9a0",
            "http": {"method": "POST", "path": "/v1/support/tickets", "status_code": 201, "client_ip": "10.0.3.12", "user_agent": "internal-client/4.2", "latency_ms": 73},
            "user": {"id": "u-4401", "role": "user"},
            "event": {"type": "ticket_create", "outcome": "success", "entity": "ticket", "entity_id": "t-9011"},
            "security": {"auth_method": "token", "mfa": None},
            "data_classification": "confidential",
            "message": "Callback number captured: +44 7911 234567",
        },
        [[("PHONE_NUMBER", "+44 7911 234567")]],
    ),

    # 9) VEHICLE_REGISTRATION (only in endpoint path)
    (
        {
            "timestamp": "2026-01-24T09:13:01.004Z",
            "level": "INFO",
            "service": {"name": "fleet-service", "version": "4.6.0", "environment": "prod"},
            "host": {"hostname": "fleet-01", "ip": "10.12.11.9"},
            "log": {"logger": "fleet.lookup", "thread": "http-nio-8080-exec-3"},
            "trace": {"trace_id": "99887766554433221100ffeeddccbbaa", "span_id": "1020304050607080"},
            "correlation_id": "corr-9ab0d1c2e3",
            "http": {"method": "GET", "path": "/v1/vehicles/AB12 CDE", "status_code": 200, "client_ip": "10.0.5.90", "user_agent": "internal-client/4.2", "latency_ms": 15},
            "user": {"id": "u-6102", "role": "user"},
            "event": {"type": "vehicle_lookup", "outcome": "success", "entity": "vehicle", "entity_id": "lookup"},
            "security": {"auth_method": "token", "mfa": None},
            "data_classification": "internal",
            "message": "Vehicle lookup completed",
        },
        [[("VEHICLE_REGISTRATION", "AB12 CDE")]],
    ),

    # 10) BANK_SORT_CODE (only in message)
    (
        {
            "timestamp": "2026-01-24T09:13:08.730Z",
            "level": "ERROR",
            "service": {"name": "payments-service", "version": "7.0.1", "environment": "prod"},
            "host": {"hostname": "pay-02", "ip": "10.12.12.14"},
            "log": {"logger": "payments.validate", "thread": "http-nio-8080-exec-8"},
            "trace": {"trace_id": "cafebabef00ddeadbeefcafebabef00d", "span_id": "5566778899aabbcc"},
            "correlation_id": "corr-4c8d2e1f00",
            "http": {"method": "POST", "path": "/v1/payments/validate", "status_code": 400, "client_ip": "10.0.9.7", "user_agent": "internal-client/4.2", "latency_ms": 28},
            "user": {"id": "u-7008", "role": "user"},
            "event": {"type": "payment_validate", "outcome": "failed", "entity": "payment", "entity_id
