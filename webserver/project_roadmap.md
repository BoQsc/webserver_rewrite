# Project Roadmap: Webserver Rewrite (Final)

## Project Overview

This project aims to build a feature-complete, modern Python web server that incorporates the best ideas from the old project while using a clean, maintainable, and scalable architecture.

## Project Philosophy

This rewrite operates under a specific philosophy for the current development cycle:

*   **Rejection of Modern Frameworks:** We are intentionally not using existing modern web frameworks. The goal is to build our own foundational components from the ground up, using only the standard library, to create a system that is perfectly tailored to our needs and philosophy.
*   **Strict Adherence to Standard Library:** The entire project will be implemented using only Python's standard library. No third-party libraries are to be used. This constraint forces a deep understanding of the standard library's capabilities and limitations.
    *   **Exception:** The `cryptography` library is a permitted exception. It is considered essential for handling the complexities of SSL certificate management and is not feasible to replicate from scratch.
*   **Simplicity and Clarity as Core Values:** When faced with a design choice, the simpler and clearer solution will be preferred. This is to ensure the codebase is easy to understand, maintain, and build upon.

These constraints apply to the whole project for this rewrite. The goal is to create a robust and well-understood foundation, which may be followed by a future rewrite in another programming language or with a different architecture to support a larger number of users.

## Guiding Principles

*   **Modular Architecture:** A clean, maintainable structure of independent, reusable modules.
*   **Extensible via Plugins:** A well-defined plugin system for adding new features.
*   **Asynchronous Services:** Use `asyncio` for background services and other non-HTTP tasks to ensure high performance and scalability.
*   **Simplicity and Clarity:** Prioritize clear, straightforward implementations, using Python's standard library wherever possible to minimize complexity and avoid reinventing the wheel.
*   **Developer-Friendly:** An intuitive and easy-to-use API, including features like decorator-based routing and hot-reloading.
*   **Robust Observability:** Comprehensive logging, metrics, and status monitoring.
*   **Production-Ready:** Focus on stability, error handling, and deployment utilities.

---

## Phase 1: The Core Server

This phase focuses on building the essential, core components of the web server.

-   [ ] **Project Scaffolding:**
    -   [ ] Set up a clean project structure with a `webserver` package.
-   [ ] **Core Server Engine:**
    -   [ ] Develop a core server engine using Python's standard `http.server` and `socketserver` for simplicity and clarity. This provides a stable, synchronous, multi-threaded foundation for HTTP/HTTPS serving with SNI support.
-   [ ] **Structured Configuration:**
    -   [ ] Implement a clean, dataclass-based configuration system with validation for network, SSL, DDNS, UPnP, web server, monitoring, and security settings. This includes dynamic defaults, path resolution, and security-focused parameters like HSTS, rate limiting, and client request size/timeout limits.
-   [ ] **Centralized Logging:**
    -   [ ] Set up a comprehensive logging system with rotating file handlers for main, error, and access logs, structured log formatters, and component-specific loggers for fine-grained control.
-   [ ] **Standardized Error Handling:**
    -   [ ] Implement a `StandardizedError` class with categories (e.g., NETWORK, FILE_IO) and severities (LOW, MEDIUM, HIGH, CRITICAL), a central `ErrorHandler` for consistent logging, robust error response generation (JSON), and integration with `unicode_safety` for robust character encoding handling. Includes a `safe_execute` utility for defensive programming.
-   [ ] **Metrics Collection & Health Monitoring:**
    -   [ ] Implement a `MetricsCollector` for detailed application-level metrics (method, path, status, response time, client IP, user agent, sizes). This includes time-window aggregation, response time histograms (P50, P95, P99), and path normalization.
    -   [ ] Develop an `InfrastructureStatusManager` for tracking component statuses, running configurable health checks (using standard library only), determining overall system health (healthy, warning, degraded), and including external/local IP discovery and alerting integration. This will focus on application-level and basic system status, excluding detailed resource usage (CPU, memory, disk I/O) due to the 'no third-party libraries' constraint.
-   [ ] **Port Conflict Detection:**
    -   [ ] Integrate utilities for detecting and reporting port conflicts, including process identification (using standard library tools like `subprocess` to call `netstat` or `tasklist` as a fallback), actionable error messages, and suggestions for alternative ports.
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
-   [ ] **WebSocket Support (Deferred):**
    -   [ ] This feature is deferred for the current rewrite. Implementing the WebSocket protocol without third-party libraries is a significant undertaking that conflicts with the project's emphasis on simplicity. If this feature becomes critical in the future, the recommended approach would be to make an exception for the `websockets` library rather than building a custom implementation.
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

## Phase 5: Future Considerations

This section outlines potential future directions for the project, beyond the scope of the current rewrite.

*   **High-Performance Rewrite:** For supporting a significantly larger number of concurrent users, a future version of this project could be rewritten in a language like **Rust** or **Go**. This would provide a higher level of performance and more granular control over system resources.
*   **Fully Asynchronous Architecture:** A future rewrite could adopt a fully asynchronous architecture from the ground up, potentially using a different language's ecosystem (e.g., Tokio for Rust, or Go's native concurrency).
*   **API-Driven Frontend:** The frontend could be built as a separate, API-driven application, potentially using a modern JavaScript framework, which would communicate with the web server via a RESTful or GraphQL API.
*   **Containerization and Orchestration:** For easier deployment and scalability, the project could be containerized using Docker and managed with an orchestration tool like Kubernetes.