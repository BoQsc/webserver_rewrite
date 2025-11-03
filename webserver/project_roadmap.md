# Project Roadmap: Webserver Rewrite (Final)

## Project Overview

This project aims to build a feature-complete, modern Python web server that incorporates the best ideas from the old project while using a clean, maintainable, and scalable architecture.

## Guiding Principles

*   **Modular Architecture:** A clean, maintainable structure of independent, reusable modules.
*   **Extensible via Plugins:** A well-defined plugin system for adding new features.
*   **High Performance:** A fully asynchronous design using `asyncio`.
*   **Developer-Friendly:** An intuitive and easy-to-use API, including features like decorator-based routing and hot-reloading.
*   **Robust Observability:** Comprehensive logging, metrics, and status monitoring.
*   **Production-Ready:** Focus on stability, error handling, and deployment utilities.

---

## Phase 1: The Core Server

This phase focuses on building the essential, core components of the web server.

-   [ ] **Project Scaffolding:**
    -   [ ] Set up a clean project structure with a `webserver` package.
-   [ ] **Core Server Engine:**
    -   [ ] Develop a basic, asynchronous HTTP/HTTPS server with SNI (Server Name Indication) support for handling multiple SSL certificates on a single IP address.
-   [ ] **Structured Configuration:**
    -   [ ] Implement a clean, dataclass-based configuration system with validation for network, SSL, DDNS, UPnP, web server, monitoring, and security settings. This includes dynamic defaults, path resolution, and security-focused parameters like HSTS, rate limiting, and client request size/timeout limits.
-   [ ] **Centralized Logging:**
    -   [ ] Set up a comprehensive logging system with rotating file handlers for main, error, and access logs, structured log formatters, and component-specific loggers for fine-grained control.
-   [ ] **Standardized Error Handling:**
    -   [ ] Implement a `StandardizedError` class with categories (e.g., NETWORK, FILE_IO) and severities (LOW, MEDIUM, HIGH, CRITICAL), a central `ErrorHandler` for consistent logging, robust error response generation (JSON), and integration with `unicode_safety` for robust character encoding handling. Includes a `safe_execute` utility for defensive programming.
-   [ ] **Metrics Collection & Health Monitoring:**
    -   [ ] Implement a `MetricsCollector` for detailed request metrics (method, path, status, response time, client IP, user agent, sizes) and system resource metrics (CPU, memory, disk I/O, network I/O, active threads, open files). This includes time-window aggregation, response time histograms (P50, P95, P99), path normalization, and a health status calculation based on metrics and thresholds.
    -   [ ] Develop an `InfrastructureStatusManager` for tracking component statuses, running configurable health checks, determining overall system health (healthy, warning, degraded), and including external/local IP discovery and alerting integration.
-   [ ] **Port Conflict Detection:**
    -   [ ] Integrate utilities for detecting and reporting port conflicts, including process identification (using `psutil` and `netstat`/`tasklist` fallback), actionable error messages, and suggestions for alternative ports.
-   [ ] **Routing System:**
    -   [ ] Implement a flexible, decorator-based routing system (e.g., `@app.route('/path')`) with support for path parameter extraction and module-specific route registries.

---

## Phase 2: Essential Features

This phase focuses on adding the most important features to the core server.

-   [ ] **Middleware Pipeline:**
    -   [ ] Implement a middleware system for processing requests and responses.
-   [ ] **Static File Serving:**
    -   [ ] Add the ability to serve static files with caching and security considerations, leveraging a `RawResponse` utility for efficient content delivery.
-   [ ] **HTML Processor (Server-Side Templating):**
    -   [ ] Implement a templating engine for dynamic HTML generation, supporting variables, components, loops, and conditionals, and integrating with modular page handlers.
-   [ ] **WebSocket Support:**
    -   [ ] Implement an asyncio-based, threaded WebSocket server with WSS (secure WebSocket) support and application integration for handling real-time communication.
-   [ ] **Hot-Reloading for Development:**
    -   [ ] Implement a module watcher that automatically reloads changed Python files in development, enhancing developer experience by invalidating `sys.modules` and decorator registries, and handling submodule and subdomain handler re-registration.

---

## Phase 3: Advanced Features & Services (Plugin-Based)

This phase focuses on adding more advanced features and services to the server, primarily through a plugin system.

-   [ ] **Plugin System:**
    -   [ ] Design and implement a plugin system that can dynamically discover and load new features and subdomains, including automatic registration of handlers and services, and support for dynamic content sources (e.g., `public_pages_handler`).
-   [ ] **Subdomain Management:**
    -   [ ] Implement a mechanism for handling requests to different subdomains and routing them to specific handlers, integrated with the plugin system. This will include dynamic discovery of subdomains based on marker files and hot-reloading of subdomain configurations.
-   [ ] **Core Service Plugins:**
    -   [ ] **DDNS Plugin:** Implement a Dynamic DNS update service (e.g., Namecheap integration) with reliable external IP discovery (using multiple services), subdomain awareness (updating base domain and SSL-enabled subdomains), and a monitoring loop.
    -   [ ] **UPnP Plugin:** Implement a UPnP port forwarding service with SSDP discovery, SOAP communication for port mapping, mapping verification and refresh, and conflict resolution.
    -   [ ] **SSL Management Plugin:** Implement a comprehensive SSL certificate management service (e.g., Let's Encrypt integration) with automated renewal, ACME challenge coordination (HTTP-01), `cryptography` library integration for parsing, self-signed certificate fallback, dynamic SSL config hot-reloading through marker files, DNS propagation awareness (including attention files and retry mechanisms), per-domain failure tracking, ACME rate limit handling, certificate chain splitting, and HTTPS restart triggering.

---

## Phase 4: Application Layer & Production Readiness

This phase focuses on building the features necessary for creating full-fledged web applications and preparing the server for production.

-   [ ] **AsyncJSONStore (Database):**
    -   [ ] Implement a high-performance, asynchronous JSON database with:
        -   **Unified API:** A single, high-level API integrating all database components.
        -   **Atomic File Writes & WAL:** Crash-safe atomic file operations and Write-Ahead Logging for ACID compliance and durability.
        -   **Multi-Level Caching:** L1 (in-memory), L2 (LRU), and L3 (memory-mapped files) with file modification time validation and size-based eviction.
        -   **Advanced Locking:** Hierarchical (collection/record/field), read-write locks, deadlock detection and resolution, and fair queuing.
        -   **Transaction Management:** Full ACID properties, WAL recovery, and checkpointing.
        -   **Advanced Indexing:** Hash, B-Tree, and Full-Text indexes with automatic detection, persistence, and query optimization.
        -   **Backup & Recovery:** Full, incremental, and differential backups with compression, encryption (optional), verification, and retention policies.
        -   **Connection Pooling:** Manages thousands of concurrent connections with limits per total, per IP, and per user.
        -   **Rate Limiting & Throttling:** Token bucket algorithm for rate limiting and resource-based throttling (CPU, memory, disk usage).
        -   **Database Monitoring & Alerting:** Detailed metrics, performance profiling, alert rules, and health scoring for database operations.
-   [ ] **Built-in Authentication:**
    -   [ ] Implement a secure, custom authentication system (e.g., PBKDF2+HMAC).
-   [ ] **RESTful API Framework:**
    -   [ ] Build a framework on top of the core server that makes it easy to create RESTful APIs, leveraging the decorator-based routing system for clean API definitions and path parameter extraction.
-   [ ] **Comprehensive Testing:**
    -   [ ] Write unit and integration tests for all features and plugins.
-   [ ] **Documentation:**
    -   [ ] Create detailed documentation for the server, its features, and the plugin system.
-   [ ] **Deployment & Process Management:**
    -   [ ] Provide scripts and best practices for deploying the server, including a watchdog for health monitoring, auto-recovery, and graceful shutdown mechanisms.

---