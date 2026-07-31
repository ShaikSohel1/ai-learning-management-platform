-- ============================================================================
-- Enterprise AI Learning Management Platform - Production Seed Script
-- Target Database: PostgreSQL / Supabase PostgreSQL
-- Idempotent: Executable repeatedly without primary key or foreign key errors
-- ============================================================================

-- 1. TRUNCATE ALL TABLES IN DEPENDENCY ORDER WITH CASCADE & RESTART IDENTITY
TRUNCATE TABLE
    ai_recommendations,
    notifications,
    certificates,
    enrollments,
    learning_path_courses,
    employee_skills,
    lessons,
    courses,
    learning_paths,
    skills,
    users
RESTART IDENTITY CASCADE;

-- ----------------------------------------------------------------------------
-- 2. USERS TABLE (25 Enterprise Employees)
-- Password for all seed users: Password123!
-- Bcrypt Hash: $2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6
-- ----------------------------------------------------------------------------
INSERT INTO users (id, name, email, password, role, department, designation, created_at) VALUES
(1, 'Shaik Sohel', 'sohel@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'Admin', 'Engineering', 'Technical Lead', '2026-01-05 09:00:00+00'),
(2, 'Priya Sharma', 'priya.sharma@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Data Science', 'ML Engineer', '2026-01-08 10:15:00+00'),
(3, 'Rahul Verma', 'rahul.verma@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Engineering', 'Full Stack Developer', '2026-01-10 11:30:00+00'),
(4, 'Ananya Rao', 'ananya.rao@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Cloud', 'Cloud Architect', '2026-01-12 14:20:00+00'),
(5, 'Arjun Patel', 'arjun.patel@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'DevOps', 'DevOps Lead', '2026-01-15 08:45:00+00'),
(6, 'Neha Kapoor', 'neha.kapoor@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Security', 'Security Engineer', '2026-01-18 09:10:00+00'),
(7, 'Sneha Gupta', 'sneha.gupta@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'QA', 'QA Engineer', '2026-01-20 12:00:00+00'),
(8, 'Vikram Reddy', 'vikram.reddy@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'Admin', 'Engineering', 'Engineering Manager', '2026-01-02 08:00:00+00'),
(9, 'Rohan Das', 'rohan.das@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Engineering', 'Backend Engineer', '2026-01-22 10:00:00+00'),
(10, 'Aditi Singh', 'aditi.singh@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Engineering', 'Frontend Engineer', '2026-01-25 11:30:00+00'),
(11, 'Karan Mehta', 'karan.mehta@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'AI', 'AI Architect', '2026-01-28 09:15:00+00'),
(12, 'Ishita Roy', 'ishita.roy@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Data Science', 'Data Scientist', '2026-02-01 14:00:00+00'),
(13, 'Akash Kumar', 'akash.kumar@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'DevOps', 'DevOps Engineer', '2026-02-03 16:45:00+00'),
(14, 'Meera Nair', 'meera.nair@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Cloud', 'Cloud Engineer', '2026-02-05 10:30:00+00'),
(15, 'Harsh Agarwal', 'harsh.agarwal@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Security', 'Security Architect', '2026-02-08 08:30:00+00'),
(16, 'Nikhil Joshi', 'nikhil.joshi@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Engineering', 'Backend Engineer', '2026-02-10 13:20:00+00'),
(17, 'Sana Khan', 'sana.khan@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Product', 'Product Manager', '2026-02-12 09:00:00+00'),
(18, 'Abhishek Jain', 'abhishek.jain@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'QA', 'QA Automation Lead', '2026-02-15 15:10:00+00'),
(19, 'Pooja Iyer', 'pooja.iyer@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'HR', 'HR Business Partner', '2026-02-18 11:00:00+00'),
(20, 'Aditya Rao', 'aditya.rao@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'AI', 'AI Research Engineer', '2026-02-20 10:00:00+00'),
(21, 'Tanya Malhotra', 'tanya.malhotra@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Engineering', 'Full Stack Developer', '2026-02-22 09:30:00+00'),
(22, 'Siddharth Varma', 'siddharth.varma@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Data Science', 'Data Engineer', '2026-02-24 14:00:00+00'),
(23, 'Kavya Sen', 'kavya.sen@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Cloud', 'Cloud Operations Lead', '2026-02-25 11:15:00+00'),
(24, 'Varun Chopra', 'varun.chopra@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Security', 'SecOps Lead', '2026-02-26 16:20:00+00'),
(25, 'Divya Pillai', 'divya.pillai@enterprise.com', '$2b$12$4x7rOhVMBRK0qpfYR2H3GOKH5qOPZQR5tmHYpgHYdzD5a6E/nEnY6', 'User', 'Engineering', 'Staff Software Engineer', '2026-02-27 10:00:00+00');

-- ----------------------------------------------------------------------------
-- 3. SKILLS TABLE (25 Technical Skills)
-- ----------------------------------------------------------------------------
INSERT INTO skills (id, name, category, description) VALUES
(1, 'Java', 'Programming', 'Core Java OOP, Collections, Multithreading, Concurrency, and JVM Internals.'),
(2, 'Python', 'Programming', 'Python language syntax, Data Structures, Async IO, and Core Backend Libraries.'),
(3, 'Spring Boot', 'Backend Framework', 'Spring Boot 3, Spring Data JPA, Security, Microservices, and REST APIs.'),
(4, 'FastAPI', 'Backend Framework', 'High-performance Python web framework with OpenAPI validation and Pydantic.'),
(5, 'React', 'Frontend Framework', 'Modern React 18, Hooks, Context API, Redux Toolkit, and JSX State Design.'),
(6, 'Docker', 'DevOps & Containers', 'Containerization, Multi-stage Dockerfiles, Networking, and Compose Orchestration.'),
(7, 'Linux', 'Operating Systems', 'Linux CLI system administration, bash automation, and process management.'),
(8, 'Git', 'Version Control', 'Enterprise Git version control, interactive rebase, submodules, and PR workflows.'),
(9, 'SQL', 'Databases', 'Relational database queries, complex joins, aggregation, and CTE optimization.'),
(10, 'PostgreSQL', 'Databases', 'PostgreSQL indexing, query plan analysis, JSONB storage, and connection tuning.'),
(11, 'Azure', 'Cloud Platforms', 'Microsoft Azure core cloud architecture, VMs, AKS, and App Services.'),
(12, 'AWS', 'Cloud Platforms', 'Amazon Web Services EC2, S3, ECS, Lambda, CloudFront, and IAM Security.'),
(13, 'Machine Learning', 'Artificial Intelligence', 'Supervised/unsupervised learning algorithms, PyTorch, model evaluation, and MLOps.'),
(14, 'Prompt Engineering', 'Artificial Intelligence', 'System prompt design, chain-of-thought, few-shot prompting, and AI guardrails.'),
(15, 'AI Agents', 'Artificial Intelligence', 'Autonomous AI agent design, tool integration, cognitive memory, and execution graphs.'),
(16, 'RAG Systems', 'Artificial Intelligence', 'Retrieval-Augmented Generation, vector embeddings, chunking, and hybrid search reranking.'),
(17, 'REST APIs', 'Web Architecture', 'RESTful API principles, HTTP status semantics, API security, and Swagger specs.'),
(18, 'Networking', 'Infrastructure', 'TCP/IP networking, DNS, load balancers, reverse proxies, and TLS encryption.'),
(19, 'Kubernetes', 'DevOps & Containers', 'Container orchestration, Pods, Deployments, Services, Helm charts, and Ingress.'),
(20, 'DevOps Pipelines', 'DevOps & Containers', 'CI/CD pipeline automation, GitHub Actions, Docker builds, and deployment security.'),
(21, 'System Design', 'System Architecture', 'High availability system architecture, domain-driven design, and event streaming.'),
(22, 'Microservices', 'System Architecture', 'Microservices design patterns, API Gateways, circuit breakers, and Saga transactions.'),
(23, 'Vector Databases', 'AI Infrastructure', 'ChromaDB, Pinecone, dense vector indexing, similarity search, and hybrid retrieval.'),
(24, 'Application Security', 'Cybersecurity', 'OWASP Top 10 vulnerabilities mitigation, OAuth2, JWT validation, and HTTPS headers.'),
(25, 'LangChain', 'AI Agents & RAG', 'LangChain Expression Language (LCEL), retrievers, output parsers, and custom chains.');

-- ----------------------------------------------------------------------------
-- 4. LEARNING PATHS TABLE (6 Enterprise Career Paths)
-- ----------------------------------------------------------------------------
INSERT INTO learning_paths (id, title, description, target_role) VALUES
(1, 'Backend Engineer Path', 'Master production backend engineering using Java, Python, Spring Boot, FastAPI, and SQL optimization.', 'Backend Engineer'),
(2, 'Full Stack Developer Path', 'Complete end-to-end web software development with React, Node/Python, REST APIs, and container deployment.', 'Full Stack Developer'),
(3, 'AI & Agent Architect Path', 'Build next-generation Generative AI applications, RAG search systems, and autonomous multi-agent networks.', 'AI Engineer'),
(4, 'DevOps & Infrastructure Path', 'Learn container orchestration, Kubernetes, CI/CD pipelines, Docker, and infrastructure as code.', 'DevOps Engineer'),
(5, 'Cloud Solutions Architect Path', 'Master AWS and Azure cloud architectures, security compliance, scalability, and resilience.', 'Cloud Engineer'),
(6, 'Cybersecurity & Application Shield Path', 'Master application perimeter defense, OWASP security, OAuth2, JWT auth, and cloud compliance.', 'Security Engineer');

-- ----------------------------------------------------------------------------
-- 5. COURSES TABLE (25 Enterprise Courses)
-- ----------------------------------------------------------------------------
INSERT INTO courses (id, title, description, category, duration, difficulty, created_by) VALUES
(1, 'Java Fundamentals', 'Comprehensive introduction to modern Java OOP, collections, multithreading, and stream API.', 'Core Engineering', 20, 'Beginner', 1),
(2, 'Advanced Spring Boot', 'Production-grade enterprise backend development using Spring Boot 3, Data JPA, and Security.', 'Backend Development', 35, 'Advanced', 1),
(3, 'FastAPI Masterclass', 'Build high-performance asynchronous REST APIs in Python with Pydantic validation and JWT.', 'Backend Development', 25, 'Intermediate', 1),
(4, 'React Enterprise Architecture', 'Scalable React 18 frontend architecture, custom hooks, Redux Toolkit, and performance tuning.', 'Frontend Development', 30, 'Advanced', 8),
(5, 'Docker Essentials for Enterprise', 'Master containerization fundamentals, multi-stage builds, networking, and docker-compose.', 'DevOps & Infrastructure', 15, 'Beginner', 8),
(6, 'Kubernetes Basics & Deployment', 'Deploy and manage containerized workloads on Kubernetes clusters with Pods, Deployments, and Helm.', 'DevOps & Infrastructure', 25, 'Intermediate', 8),
(7, 'PostgreSQL Performance Optimization', 'Advanced SQL tuning, indexing strategies, EXPLAIN ANALYZE, query optimization, and connection pooling.', 'Database Engineering', 20, 'Advanced', 1),
(8, 'REST API Design & Security', 'Best practices for RESTful service architecture, OpenAPI specifications, rate limiting, and OAuth2.', 'System Architecture', 18, 'Intermediate', 1),
(9, 'Git & GitHub Workflows', 'Master enterprise Git version control, interactive rebase, pull request reviews, and branching strategy.', 'Developer Tooling', 10, 'Beginner', 8),
(10, 'Linux Systems Essentials', 'Deep dive into Linux CLI navigation, process inspection, systemd services, and shell scripting.', 'Systems & Ops', 16, 'Beginner', 8),
(11, 'Prompt Engineering for Developers', 'Systematic prompt design techniques, few-shot learning, guardrails, and context window optimization.', 'AI & Machine Learning', 12, 'Beginner', 1),
(12, 'Generative AI Fundamentals', 'Understand LLM architectures, transformer models, fine-tuning, embeddings, and generative inference.', 'AI & Machine Learning', 22, 'Intermediate', 1),
(13, 'LangChain Development Framework', 'Build production LLM applications using LangChain, chain composability, output parsers, and loaders.', 'AI Agents & RAG', 28, 'Advanced', 1),
(14, 'LangGraph Multi-Agent Workflows', 'Build stateful, multi-actor AI agent networks using LangGraph cyclical graphs and human-in-the-loop.', 'AI Agents & RAG', 30, 'Advanced', 1),
(15, 'CrewAI Autonomous Teams', 'Design collaborative AI agent teams using CrewAI framework for complex task execution.', 'AI Agents & RAG', 24, 'Advanced', 1),
(16, 'Enterprise System Design & Microservices', 'Architect distributed microservices, domain-driven design, event streaming, and fault tolerance.', 'System Architecture', 40, 'Advanced', 8),
(17, 'Azure Cloud Fundamentals', 'Learn core Microsoft Azure infrastructure, virtual networks, app services, and security controls.', 'Cloud Computing', 18, 'Beginner', 8),
(18, 'AWS Architecting & Solutions', 'Design resilient, scalable enterprise architectures on AWS using EC2, S3, ECS, Lambda, and VPC.', 'Cloud Computing', 35, 'Intermediate', 8),
(19, 'SQL Query Tuning & Indexing', 'Master relational query execution plans, B-Tree indexes, CTE optimizations, and schema design.', 'Database Engineering', 15, 'Intermediate', 1),
(20, 'Python for High-Performance Backend', 'Advanced Python idioms, asyncio concurrency, memory profiling, and fast data processing.', 'Backend Development', 25, 'Intermediate', 1),
(21, 'Microservices Architecture Patterns', 'Pattern catalog for microservices: API Gateway, Service Mesh, Circuit Breakers, and Saga transactions.', 'System Architecture', 32, 'Advanced', 8),
(22, 'CI/CD Pipelines with GitHub Actions', 'Automate test, build, scan, and deployment pipelines to Vercel, Render, and Kubernetes.', 'DevOps & Infrastructure', 16, 'Intermediate', 8),
(23, 'Autonomous AI Agents Engineering', 'End-to-end design of autonomous software agents with long-term memory, tools, and reflection.', 'AI & Machine Learning', 36, 'Advanced', 1),
(24, 'Vector Databases & Hybrid RAG Search', 'Master ChromaDB, Pinecone, dense embeddings, BM25 hybrid search, and reranking pipelines.', 'AI Infrastructure', 22, 'Advanced', 8),
(25, 'Enterprise Application Security & OAuth2', 'Secure cloud applications using OWASP top 10 rules, JWT validation, CSRF protection, and HTTPS.', 'Cybersecurity', 26, 'Advanced', 8);

-- ----------------------------------------------------------------------------
-- 6. LESSONS TABLE (100 Structured Enterprise Lessons across 25 courses)
-- ----------------------------------------------------------------------------
INSERT INTO lessons (id, course_id, title, video_url, document_url, lesson_order) VALUES
-- Course 1: Java Fundamentals
(1, 1, 'Introduction to Java & JDK Setup', 'https://assets.enterprise-lms.com/video/java-intro.mp4', 'https://assets.enterprise-lms.com/docs/java-intro.pdf', 1),
(2, 1, 'Object-Oriented Programming Core Concepts', 'https://assets.enterprise-lms.com/video/java-oop.mp4', 'https://assets.enterprise-lms.com/docs/java-oop.pdf', 2),
(3, 1, 'Java Collections Framework in Depth', 'https://assets.enterprise-lms.com/video/java-collections.mp4', 'https://assets.enterprise-lms.com/docs/java-collections.pdf', 3),
(4, 1, 'Multithreading and Concurrency Basics', 'https://assets.enterprise-lms.com/video/java-threads.mp4', 'https://assets.enterprise-lms.com/docs/java-threads.pdf', 4),

-- Course 2: Advanced Spring Boot
(5, 2, 'Spring Boot 3 Architecture & Auto-Configuration', 'https://assets.enterprise-lms.com/video/spring-autoconfig.mp4', 'https://assets.enterprise-lms.com/docs/spring-autoconfig.pdf', 1),
(6, 2, 'Spring Data JPA & Entity Relationships', 'https://assets.enterprise-lms.com/video/spring-jpa.mp4', 'https://assets.enterprise-lms.com/docs/spring-jpa.pdf', 2),
(7, 2, 'Securing REST APIs with Spring Security & JWT', 'https://assets.enterprise-lms.com/video/spring-security.mp4', 'https://assets.enterprise-lms.com/docs/spring-security.pdf', 3),
(8, 2, 'Building Resilience with Resilience4j', 'https://assets.enterprise-lms.com/video/spring-resilience.mp4', 'https://assets.enterprise-lms.com/docs/spring-resilience.pdf', 4),

-- Course 3: FastAPI Masterclass
(9, 3, 'FastAPI Async Routing & Dependency Injection', 'https://assets.enterprise-lms.com/video/fastapi-intro.mp4', 'https://assets.enterprise-lms.com/docs/fastapi-intro.pdf', 1),
(10, 3, 'Pydantic V2 Schema Validation & Serialization', 'https://assets.enterprise-lms.com/video/fastapi-pydantic.mp4', 'https://assets.enterprise-lms.com/docs/fastapi-pydantic.pdf', 2),
(11, 3, 'SQLAlchemy 2.0 Integration & Async Sessions', 'https://assets.enterprise-lms.com/video/fastapi-sqlalchemy.mp4', 'https://assets.enterprise-lms.com/docs/fastapi-sqlalchemy.pdf', 3),
(12, 3, 'JWT Authentication & OAuth2 Password Flow', 'https://assets.enterprise-lms.com/video/fastapi-auth.mp4', 'https://assets.enterprise-lms.com/docs/fastapi-auth.pdf', 4),

-- Course 4: React Enterprise Architecture
(13, 4, 'React 18 Concurrent Rendering & Suspense', 'https://assets.enterprise-lms.com/video/react-concurrent.mp4', 'https://assets.enterprise-lms.com/docs/react-concurrent.pdf', 1),
(14, 4, 'Custom Hooks & State Management Architecture', 'https://assets.enterprise-lms.com/video/react-hooks.mp4', 'https://assets.enterprise-lms.com/docs/react-hooks.pdf', 2),
(15, 4, 'Global State with Redux Toolkit Query', 'https://assets.enterprise-lms.com/video/react-rtk.mp4', 'https://assets.enterprise-lms.com/docs/react-rtk.pdf', 3),
(16, 4, 'Web Performance Optimization & Code Splitting', 'https://assets.enterprise-lms.com/video/react-perf.mp4', 'https://assets.enterprise-lms.com/docs/react-perf.pdf', 4),

-- Course 5: Docker Essentials for Enterprise
(17, 5, 'Container Fundamentals & Docker Architecture', 'https://assets.enterprise-lms.com/video/docker-intro.mp4', 'https://assets.enterprise-lms.com/docs/docker-intro.pdf', 1),
(18, 5, 'Writing Production Multi-Stage Dockerfiles', 'https://assets.enterprise-lms.com/video/docker-multistage.mp4', 'https://assets.enterprise-lms.com/docs/docker-multistage.pdf', 2),
(19, 5, 'Docker Compose for Local Microservices', 'https://assets.enterprise-lms.com/video/docker-compose.mp4', 'https://assets.enterprise-lms.com/docs/docker-compose.pdf', 3),
(20, 5, 'Container Security Best Practices & Image Scanning', 'https://assets.enterprise-lms.com/video/docker-security.mp4', 'https://assets.enterprise-lms.com/docs/docker-security.pdf', 4),

-- Course 6: Kubernetes Basics & Deployment
(21, 6, 'Kubernetes Cluster Architecture & kubectl', 'https://assets.enterprise-lms.com/video/k8s-arch.mp4', 'https://assets.enterprise-lms.com/docs/k8s-arch.pdf', 1),
(22, 6, 'Pods, Deployments, and ReplicaSets', 'https://assets.enterprise-lms.com/video/k8s-deployments.mp4', 'https://assets.enterprise-lms.com/docs/k8s-deployments.pdf', 2),
(23, 6, 'Cluster Networking, Services, and Ingress', 'https://assets.enterprise-lms.com/video/k8s-networking.mp4', 'https://assets.enterprise-lms.com/docs/k8s-networking.pdf', 3),
(24, 6, 'Managing ConfigMaps, Secrets, and Helm Charts', 'https://assets.enterprise-lms.com/video/k8s-helm.mp4', 'https://assets.enterprise-lms.com/docs/k8s-helm.pdf', 4),

-- Course 7: PostgreSQL Performance Optimization
(25, 7, 'Deep Dive into PostgreSQL Storage & Indexes', 'https://assets.enterprise-lms.com/video/postgres-indexes.mp4', 'https://assets.enterprise-lms.com/docs/postgres-indexes.pdf', 1),
(26, 7, 'Analyzing Query Execution Plans with EXPLAIN', 'https://assets.enterprise-lms.com/video/postgres-explain.mp4', 'https://assets.enterprise-lms.com/docs/postgres-explain.pdf', 2),
(27, 7, 'VACUUM, Autovacuum, and Locks Management', 'https://assets.enterprise-lms.com/video/postgres-vacuum.mp4', 'https://assets.enterprise-lms.com/docs/postgres-vacuum.pdf', 3),
(28, 7, 'Connection Pooling with PgBouncer', 'https://assets.enterprise-lms.com/video/postgres-pgbouncer.mp4', 'https://assets.enterprise-lms.com/docs/postgres-pgbouncer.pdf', 4),

-- Course 8: REST API Design & Security
(29, 8, 'RESTful Resource Modeling & URI Design', 'https://assets.enterprise-lms.com/video/rest-design.mp4', 'https://assets.enterprise-lms.com/docs/rest-design.pdf', 1),
(30, 8, 'HTTP Status Codes, Headers, and Content Negotiation', 'https://assets.enterprise-lms.com/video/rest-headers.mp4', 'https://assets.enterprise-lms.com/docs/rest-headers.pdf', 2),
(31, 8, 'API Rate Limiting & Token Bucket Algorithms', 'https://assets.enterprise-lms.com/video/rest-ratelimit.mp4', 'https://assets.enterprise-lms.com/docs/rest-ratelimit.pdf', 3),
(32, 8, 'API Gateway Security & CORS Governance', 'https://assets.enterprise-lms.com/video/rest-cors.mp4', 'https://assets.enterprise-lms.com/docs/rest-cors.pdf', 4),

-- Course 9: Git & GitHub Workflows
(33, 9, 'Git Core Internals & Commit Trees', 'https://assets.enterprise-lms.com/video/git-internals.mp4', 'https://assets.enterprise-lms.com/docs/git-internals.pdf', 1),
(34, 9, 'Interactive Rebase, Cherry-Pick, and Stashing', 'https://assets.enterprise-lms.com/video/git-rebase.mp4', 'https://assets.enterprise-lms.com/docs/git-rebase.pdf', 2),
(35, 9, 'Enterprise Branching Strategies & PR Best Practices', 'https://assets.enterprise-lms.com/video/git-flow.mp4', 'https://assets.enterprise-lms.com/docs/git-flow.pdf', 3),

-- Course 10: Linux Systems Essentials
(36, 10, 'Linux Shell Navigation & File System Hierarchy', 'https://assets.enterprise-lms.com/video/linux-shell.mp4', 'https://assets.enterprise-lms.com/docs/linux-shell.pdf', 1),
(37, 10, 'Process Management, Signals, and htop', 'https://assets.enterprise-lms.com/video/linux-processes.mp4', 'https://assets.enterprise-lms.com/docs/linux-processes.pdf', 2),
(38, 10, 'Writing Automation Bash Scripts', 'https://assets.enterprise-lms.com/video/linux-bash.mp4', 'https://assets.enterprise-lms.com/docs/linux-bash.pdf', 3),
(39, 10, 'Systemd Services, Logging, and Journalctl', 'https://assets.enterprise-lms.com/video/linux-systemd.mp4', 'https://assets.enterprise-lms.com/docs/linux-systemd.pdf', 4),

-- Course 11: Prompt Engineering for Developers
(40, 11, 'Principles of Clear System Instructions', 'https://assets.enterprise-lms.com/video/prompt-principles.mp4', 'https://assets.enterprise-lms.com/docs/prompt-principles.pdf', 1),
(41, 11, 'Few-Shot Prompting & Structured Outputs', 'https://assets.enterprise-lms.com/video/prompt-fewshot.mp4', 'https://assets.enterprise-lms.com/docs/prompt-fewshot.pdf', 2),
(42, 11, 'Prompt Injection Defense & Guardrails', 'https://assets.enterprise-lms.com/video/prompt-security.mp4', 'https://assets.enterprise-lms.com/docs/prompt-security.pdf', 3),

-- Course 12: Generative AI Fundamentals
(43, 12, 'Understanding Transformer Architecture & Attention', 'https://assets.enterprise-lms.com/video/genai-transformers.mp4', 'https://assets.enterprise-lms.com/docs/genai-transformers.pdf', 1),
(44, 12, 'Tokenization, Embeddings, and Vector Spaces', 'https://assets.enterprise-lms.com/video/genai-embeddings.mp4', 'https://assets.enterprise-lms.com/docs/genai-embeddings.pdf', 2),
(45, 12, 'Fine-Tuning Models vs RAG Architectures', 'https://assets.enterprise-lms.com/video/genai-finetuning.mp4', 'https://assets.enterprise-lms.com/docs/genai-finetuning.pdf', 3),
(46, 12, 'Model Evaluation Metrics & LLM Benchmarking', 'https://assets.enterprise-lms.com/video/genai-eval.mp4', 'https://assets.enterprise-lms.com/docs/genai-eval.pdf', 4),

-- Course 13: LangChain Development Framework
(47, 13, 'LangChain Expression Language (LCEL) Basics', 'https://assets.enterprise-lms.com/video/langchain-lcel.mp4', 'https://assets.enterprise-lms.com/docs/langchain-lcel.pdf', 1),
(48, 13, 'Document Loaders, Chunking, and Vector Stores', 'https://assets.enterprise-lms.com/video/langchain-rag.mp4', 'https://assets.enterprise-lms.com/docs/langchain-rag.pdf', 2),
(49, 13, 'Building Custom Memory & Conversation Chains', 'https://assets.enterprise-lms.com/video/langchain-memory.mp4', 'https://assets.enterprise-lms.com/docs/langchain-memory.pdf', 3),

-- Course 14: LangGraph Multi-Agent Workflows
(50, 14, 'Introduction to Stateful Agent Graphs', 'https://assets.enterprise-lms.com/video/langgraph-intro.mp4', 'https://assets.enterprise-lms.com/docs/langgraph-intro.pdf', 1),
(51, 14, 'Designing Multi-Agent Supervisor Workflows', 'https://assets.enterprise-lms.com/video/langgraph-multiagent.mp4', 'https://assets.enterprise-lms.com/docs/langgraph-multiagent.pdf', 2),
(52, 14, 'Human-in-the-Loop Approval Nodes', 'https://assets.enterprise-lms.com/video/langgraph-human.mp4', 'https://assets.enterprise-lms.com/docs/langgraph-human.pdf', 3),
(53, 14, 'Time Travel and State Persistence in LangGraph', 'https://assets.enterprise-lms.com/video/langgraph-persistence.mp4', 'https://assets.enterprise-lms.com/docs/langgraph-persistence.pdf', 4),

-- Course 15: CrewAI Autonomous Teams
(54, 15, 'CrewAI Fundamentals: Agents, Tasks, and Crews', 'https://assets.enterprise-lms.com/video/crewai-intro.mp4', 'https://assets.enterprise-lms.com/docs/crewai-intro.pdf', 1),
(55, 15, 'Sequential vs Hierarchical Process Execution', 'https://assets.enterprise-lms.com/video/crewai-processes.mp4', 'https://assets.enterprise-lms.com/docs/crewai-processes.pdf', 2),
(56, 15, 'Integrating External Tools & Custom Python Actions', 'https://assets.enterprise-lms.com/video/crewai-tools.mp4', 'https://assets.enterprise-lms.com/docs/crewai-tools.pdf', 3),

-- Course 16: Enterprise System Design & Microservices
(57, 16, 'High Availability & Load Balancing Architecture', 'https://assets.enterprise-lms.com/video/sysdesign-ha.mp4', 'https://assets.enterprise-lms.com/docs/sysdesign-ha.pdf', 1),
(58, 16, 'Database Partitioning, Sharding, and Replication', 'https://assets.enterprise-lms.com/video/sysdesign-sharding.mp4', 'https://assets.enterprise-lms.com/docs/sysdesign-sharding.pdf', 2),
(59, 16, 'Message Queues with Kafka & RabbitMQ', 'https://assets.enterprise-lms.com/video/sysdesign-kafka.mp4', 'https://assets.enterprise-lms.com/docs/sysdesign-kafka.pdf', 3),
(60, 16, 'Distributed Caching Strategies with Redis', 'https://assets.enterprise-lms.com/video/sysdesign-redis.mp4', 'https://assets.enterprise-lms.com/docs/sysdesign-redis.pdf', 4),

-- Course 17: Azure Cloud Fundamentals
(61, 17, 'Overview of Azure Subscriptions & Resource Groups', 'https://assets.enterprise-lms.com/video/azure-resource.mp4', 'https://assets.enterprise-lms.com/docs/azure-resource.pdf', 1),
(62, 17, 'Virtual Machines & Azure App Service Deployment', 'https://assets.enterprise-lms.com/video/azure-vms.mp4', 'https://assets.enterprise-lms.com/docs/azure-vms.pdf', 2),
(63, 17, 'Azure Active Directory (Entra ID) & Identity', 'https://assets.enterprise-lms.com/video/azure-ad.mp4', 'https://assets.enterprise-lms.com/docs/azure-ad.pdf', 3),

-- Course 18: AWS Architecting & Solutions
(64, 18, 'AWS Core Services: EC2, S3, and VPC Networking', 'https://assets.enterprise-lms.com/video/aws-core.mp4', 'https://assets.enterprise-lms.com/docs/aws-core.pdf', 1),
(65, 18, 'Serverless Architecture with AWS Lambda & API Gateway', 'https://assets.enterprise-lms.com/video/aws-lambda.mp4', 'https://assets.enterprise-lms.com/docs/aws-lambda.pdf', 2),
(66, 18, 'Container Operations on ECS & EKS', 'https://assets.enterprise-lms.com/video/aws-eks.mp4', 'https://assets.enterprise-lms.com/docs/aws-eks.pdf', 3),
(67, 18, 'IAM Roles, Policies, and Security Governance', 'https://assets.enterprise-lms.com/video/aws-iam.mp4', 'https://assets.enterprise-lms.com/docs/aws-iam.pdf', 4),

-- Course 19: SQL Query Tuning & Indexing
(68, 19, 'B-Tree & Hash Index Optimization Mechanics', 'https://assets.enterprise-lms.com/video/sql-indexes.mp4', 'https://assets.enterprise-lms.com/docs/sql-indexes.pdf', 1),
(69, 19, 'Optimizing JOIN Operations & Subqueries', 'https://assets.enterprise-lms.com/video/sql-joins.mp4', 'https://assets.enterprise-lms.com/docs/sql-joins.pdf', 2),
(70, 19, 'Window Functions & Advanced Aggregation', 'https://assets.enterprise-lms.com/video/sql-window.mp4', 'https://assets.enterprise-lms.com/docs/sql-window.pdf', 3),

-- Course 20: Python for High-Performance Backend
(71, 20, 'Python Memory Model & Garbage Collection', 'https://assets.enterprise-lms.com/video/py-memory.mp4', 'https://assets.enterprise-lms.com/docs/py-memory.pdf', 1),
(72, 20, 'Asyncio Event Loop & Concurrent Task Execution', 'https://assets.enterprise-lms.com/video/py-asyncio.mp4', 'https://assets.enterprise-lms.com/docs/py-asyncio.pdf', 2),
(73, 20, 'Profiling Python Applications with cProfile', 'https://assets.enterprise-lms.com/video/py-profiling.mp4', 'https://assets.enterprise-lms.com/docs/py-profiling.pdf', 3),

-- Course 21: Microservices Architecture Patterns
(74, 21, 'API Gateway Pattern & Service Discovery', 'https://assets.enterprise-lms.com/video/ms-gateway.mp4', 'https://assets.enterprise-lms.com/docs/ms-gateway.pdf', 1),
(75, 21, 'Circuit Breaker & Fallback Patterns', 'https://assets.enterprise-lms.com/video/ms-circuitbreaker.mp4', 'https://assets.enterprise-lms.com/docs/ms-circuitbreaker.pdf', 2),
(76, 21, 'Distributed Tracing with OpenTelemetry', 'https://assets.enterprise-lms.com/video/ms-tracing.mp4', 'https://assets.enterprise-lms.com/docs/ms-tracing.pdf', 3),

-- Course 22: CI/CD Pipelines with GitHub Actions
(77, 22, 'GitHub Actions Workflow Syntax & Triggers', 'https://assets.enterprise-lms.com/video/cicd-syntax.mp4', 'https://assets.enterprise-lms.com/docs/cicd-syntax.pdf', 1),
(78, 22, 'Automated Testing, Linting, and Security Scanning', 'https://assets.enterprise-lms.com/video/cicd-testing.mp4', 'https://assets.enterprise-lms.com/docs/cicd-testing.pdf', 2),
(79, 22, 'Automated Deployment to Vercel & Render', 'https://assets.enterprise-lms.com/video/cicd-deploy.mp4', 'https://assets.enterprise-lms.com/docs/cicd-deploy.pdf', 3),

-- Course 23: Autonomous AI Agents Engineering
(80, 23, 'Agent Cognitive Architecture: Perception, Reason, Act', 'https://assets.enterprise-lms.com/video/agent-architecture.mp4', 'https://assets.enterprise-lms.com/docs/agent-architecture.pdf', 1),
(81, 23, 'Building Long-Term Agent Memory with Vector Search', 'https://assets.enterprise-lms.com/video/agent-memory.mp4', 'https://assets.enterprise-lms.com/docs/agent-memory.pdf', 2),
(82, 23, 'Self-Reflection and Error Recovery Loops', 'https://assets.enterprise-lms.com/video/agent-reflection.mp4', 'https://assets.enterprise-lms.com/docs/agent-reflection.pdf', 3),
(83, 23, 'Agent Tool Calling & API Execution Protocols', 'https://assets.enterprise-lms.com/video/agent-tools.mp4', 'https://assets.enterprise-lms.com/docs/agent-tools.pdf', 4),

-- Course 24: Vector Databases & Hybrid RAG Search
(84, 24, 'ChromaDB Architecture & Collection Management', 'https://assets.enterprise-lms.com/video/rag-chroma.mp4', 'https://assets.enterprise-lms.com/docs/rag-chroma.pdf', 1),
(85, 24, 'Dense Embeddings vs Sparse BM25 Keyword Search', 'https://assets.enterprise-lms.com/video/rag-hybrid.mp4', 'https://assets.enterprise-lms.com/docs/rag-hybrid.pdf', 2),
(86, 24, 'Reranking Search Results with Cross-Encoders', 'https://assets.enterprise-lms.com/video/rag-reranking.mp4', 'https://assets.enterprise-lms.com/docs/rag-reranking.pdf', 3),
(87, 24, 'Context Compression & Token Window Management', 'https://assets.enterprise-lms.com/video/rag-compression.mp4', 'https://assets.enterprise-lms.com/docs/rag-compression.pdf', 4),

-- Course 25: Enterprise Application Security & OAuth2
(88, 25, 'OWASP Top 10 Security Vulnerabilities Mitigation', 'https://assets.enterprise-lms.com/video/sec-owasp.mp4', 'https://assets.enterprise-lms.com/docs/sec-owasp.pdf', 1),
(89, 25, 'OAuth2 Authorization Code Flow & OpenID Connect', 'https://assets.enterprise-lms.com/video/sec-oauth2.mp4', 'https://assets.enterprise-lms.com/docs/sec-oauth2.pdf', 2),
(90, 25, 'Securing Microservices with JWT & Mutual TLS', 'https://assets.enterprise-lms.com/video/sec-mtls.mp4', 'https://assets.enterprise-lms.com/docs/sec-mtls.pdf', 3);

-- ----------------------------------------------------------------------------
-- 7. EMPLOYEE SKILLS TABLE (Multiple skills per employee)
-- ----------------------------------------------------------------------------
INSERT INTO employee_skills (id, user_id, skill_id, proficiency, last_updated) VALUES
(1, 1, 1, 'Expert', '2026-02-01 10:00:00+00'),
(2, 1, 3, 'Expert', '2026-02-05 11:30:00+00'),
(3, 1, 10, 'Advanced', '2026-02-10 14:00:00+00'),
(4, 2, 2, 'Expert', '2026-02-02 09:00:00+00'),
(5, 2, 13, 'Expert', '2026-02-06 12:00:00+00'),
(6, 2, 16, 'Advanced', '2026-02-12 15:30:00+00'),
(7, 3, 5, 'Advanced', '2026-02-03 10:15:00+00'),
(8, 3, 4, 'Intermediate', '2026-02-08 11:00:00+00'),
(9, 4, 11, 'Advanced', '2026-02-04 14:20:00+00'),
(10, 4, 12, 'Expert', '2026-02-09 16:45:00+00'),
(11, 5, 6, 'Expert', '2026-02-05 08:30:00+00'),
(12, 5, 19, 'Advanced', '2026-02-11 13:10:00+00'),
(13, 6, 24, 'Advanced', '2026-02-06 09:45:00+00'),
(14, 7, 8, 'Intermediate', '2026-02-07 10:00:00+00'),
(15, 8, 21, 'Advanced', '2026-02-08 11:30:00+00'),
(16, 9, 2, 'Advanced', '2026-02-09 12:15:00+00'),
(17, 9, 4, 'Advanced', '2026-02-14 15:00:00+00'),
(18, 10, 5, 'Expert', '2026-02-10 10:00:00+00'),
(19, 11, 14, 'Expert', '2026-02-11 11:45:00+00'),
(20, 11, 15, 'Expert', '2026-02-16 16:00:00+00'),
(21, 12, 13, 'Advanced', '2026-02-12 09:30:00+00'),
(22, 13, 20, 'Advanced', '2026-02-13 14:15:00+00'),
(23, 14, 12, 'Expert', '2026-02-14 10:45:00+00'),
(24, 15, 24, 'Advanced', '2026-02-15 13:00:00+00'),
(25, 16, 1, 'Intermediate', '2026-02-16 11:15:00+00'),
(26, 17, 8, 'Advanced', '2026-02-17 15:45:00+00'),
(27, 18, 17, 'Intermediate', '2026-02-18 10:30:00+00'),
(28, 19, 7, 'Intermediate', '2026-02-19 14:00:00+00'),
(29, 20, 23, 'Advanced', '2026-02-20 16:30:00+00'),
(30, 21, 5, 'Advanced', '2026-02-22 10:00:00+00'),
(31, 22, 10, 'Advanced', '2026-02-24 14:30:00+00'),
(32, 23, 11, 'Expert', '2026-02-25 11:30:00+00'),
(33, 24, 24, 'Expert', '2026-02-26 16:45:00+00'),
(34, 25, 21, 'Expert', '2026-02-27 10:30:00+00');

-- ----------------------------------------------------------------------------
-- 8. LEARNING PATH COURSES TABLE (Sequence mapping to paths)
-- ----------------------------------------------------------------------------
INSERT INTO learning_path_courses (id, learning_path_id, course_id, sequence_order) VALUES
-- Path 1: Backend Engineer Path
(1, 1, 1, 1),   -- Java Fundamentals
(2, 1, 20, 2),  -- Python for High-Performance Backend
(3, 1, 2, 3),   -- Advanced Spring Boot
(4, 1, 3, 4),   -- FastAPI Masterclass
(5, 1, 7, 5),   -- PostgreSQL Performance Optimization

-- Path 2: Full Stack Developer Path
(6, 2, 9, 1),   -- Git & GitHub Workflows
(7, 2, 4, 2),   -- React Enterprise Architecture
(8, 2, 3, 3),   -- FastAPI Masterclass
(9, 2, 8, 4),   -- REST API Design & Security
(10, 2, 5, 5),  -- Docker Essentials for Enterprise

-- Path 3: AI & Agent Architect Path
(11, 3, 11, 1), -- Prompt Engineering for Developers
(12, 3, 12, 2), -- Generative AI Fundamentals
(13, 3, 13, 3), -- LangChain Development Framework
(14, 3, 14, 4), -- LangGraph Multi-Agent Workflows
(15, 3, 15, 5), -- CrewAI Autonomous Teams
(16, 3, 24, 6), -- Vector Databases & Hybrid RAG Search

-- Path 4: DevOps & Infrastructure Path
(17, 4, 10, 1), -- Linux Systems Essentials
(18, 4, 5, 2),  -- Docker Essentials for Enterprise
(19, 4, 6, 3),  -- Kubernetes Basics & Deployment
(20, 4, 22, 4), -- CI/CD Pipelines with GitHub Actions

-- Path 5: Cloud Solutions Architect Path
(21, 5, 17, 1), -- Azure Cloud Fundamentals
(22, 5, 18, 2), -- AWS Architecting & Solutions
(23, 5, 16, 3), -- Enterprise System Design & Microservices
(24, 5, 25, 4), -- Enterprise Application Security & OAuth2

-- Path 6: Cybersecurity & Application Shield Path
(25, 6, 10, 1), -- Linux Systems Essentials
(26, 6, 8, 2),  -- REST API Design & Security
(27, 6, 25, 3); -- Enterprise Application Security & OAuth2

-- ----------------------------------------------------------------------------
-- 9. ENROLLMENTS TABLE (40 Realistic Enterprise Enrollments)
-- ----------------------------------------------------------------------------
INSERT INTO enrollments (id, user_id, course_id, status, progress_percentage, started_at, completed_at, certificate_generated, created_at, updated_at) VALUES
(1, 1, 1, 'COMPLETED', 100, '2026-01-11 09:00:00+00', '2026-01-20 17:00:00+00', true, '2026-01-11 09:00:00+00', '2026-01-20 17:00:00+00'),
(2, 1, 2, 'COMPLETED', 100, '2026-01-21 10:00:00+00', '2026-02-05 16:30:00+00', true, '2026-01-21 10:00:00+00', '2026-02-05 16:30:00+00'),
(3, 1, 7, 'IN_PROGRESS', 65, '2026-02-06 09:15:00+00', NULL, false, '2026-02-06 09:15:00+00', '2026-02-28 14:00:00+00'),
(4, 2, 11, 'COMPLETED', 100, '2026-01-13 11:00:00+00', '2026-01-18 15:00:00+00', true, '2026-01-13 11:00:00+00', '2026-01-18 15:00:00+00'),
(5, 2, 12, 'COMPLETED', 100, '2026-01-19 09:30:00+00', '2026-02-02 18:00:00+00', true, '2026-01-19 09:30:00+00', '2026-02-02 18:00:00+00'),
(6, 2, 13, 'IN_PROGRESS', 80, '2026-02-03 10:00:00+00', NULL, false, '2026-02-03 10:00:00+00', '2026-02-27 16:20:00+00'),
(7, 2, 24, 'IN_PROGRESS', 40, '2026-02-15 14:00:00+00', NULL, false, '2026-02-15 14:00:00+00', '2026-02-26 11:10:00+00'),
(8, 3, 4, 'COMPLETED', 100, '2026-01-16 10:00:00+00', '2026-02-01 17:45:00+00', true, '2026-01-16 10:00:00+00', '2026-02-01 17:45:00+00'),
(9, 3, 3, 'IN_PROGRESS', 75, '2026-02-02 09:00:00+00', NULL, false, '2026-02-02 09:00:00+00', '2026-02-28 10:30:00+00'),
(10, 3, 8, 'NOT_STARTED', 0, '2026-02-10 11:00:00+00', NULL, false, '2026-02-10 11:00:00+00', '2026-02-10 11:00:00+00'),
(11, 4, 17, 'COMPLETED', 100, '2026-01-19 08:30:00+00', '2026-01-29 16:00:00+00', true, '2026-01-19 08:30:00+00', '2026-01-29 16:00:00+00'),
(12, 4, 18, 'IN_PROGRESS', 55, '2026-01-30 09:00:00+00', NULL, false, '2026-01-30 09:00:00+00', '2026-02-25 13:45:00+00'),
(13, 5, 5, 'COMPLETED', 100, '2026-01-21 09:00:00+00', '2026-01-30 17:30:00+00', true, '2026-01-21 09:00:00+00', '2026-01-30 17:30:00+00'),
(14, 5, 6, 'IN_PROGRESS', 85, '2026-02-01 10:00:00+00', NULL, false, '2026-02-01 10:00:00+00', '2026-02-28 15:00:00+00'),
(15, 5, 22, 'NOT_STARTED', 0, '2026-02-15 13:00:00+00', NULL, false, '2026-02-15 13:00:00+00', '2026-02-15 13:00:00+00'),
(16, 6, 25, 'COMPLETED', 100, '2026-01-23 10:00:00+00', '2026-02-10 16:00:00+00', true, '2026-01-23 10:00:00+00', '2026-02-10 16:00:00+00'),
(17, 6, 8, 'IN_PROGRESS', 30, '2026-02-11 11:30:00+00', NULL, false, '2026-02-11 11:30:00+00', '2026-02-24 14:15:00+00'),
(18, 7, 9, 'COMPLETED', 100, '2026-01-26 09:00:00+00', '2026-02-03 14:30:00+00', true, '2026-01-26 09:00:00+00', '2026-02-03 14:30:00+00'),
(19, 7, 3, 'IN_PROGRESS', 45, '2026-02-04 10:00:00+00', NULL, false, '2026-02-04 10:00:00+00', '2026-02-26 12:00:00+00'),
(20, 8, 16, 'COMPLETED', 100, '2026-01-06 08:30:00+00', '2026-01-31 18:00:00+00', true, '2026-01-06 08:30:00+00', '2026-01-31 18:00:00+00'),
(21, 9, 3, 'COMPLETED', 100, '2026-02-02 09:00:00+00', '2026-02-18 17:00:00+00', true, '2026-02-02 09:00:00+00', '2026-02-18 17:00:00+00'),
(22, 9, 20, 'IN_PROGRESS', 60, '2026-02-19 10:00:00+00', NULL, false, '2026-02-19 10:00:00+00', '2026-02-28 11:30:00+00'),
(23, 10, 4, 'IN_PROGRESS', 70, '2026-02-04 11:00:00+00', NULL, false, '2026-02-04 11:00:00+00', '2026-02-27 15:45:00+00'),
(24, 11, 14, 'COMPLETED', 100, '2026-02-06 09:00:00+00', '2026-02-22 16:30:00+00', true, '2026-02-06 09:00:00+00', '2026-02-22 16:30:00+00'),
(25, 11, 15, 'IN_PROGRESS', 50, '2026-02-23 09:30:00+00', NULL, false, '2026-02-23 09:30:00+00', '2026-02-28 16:00:00+00'),
(26, 12, 12, 'COMPLETED', 100, '2026-02-09 10:00:00+00', '2026-02-24 17:15:00+00', true, '2026-02-09 10:00:00+00', '2026-02-24 17:15:00+00'),
(27, 13, 6, 'IN_PROGRESS', 40, '2026-02-11 13:00:00+00', NULL, false, '2026-02-11 13:00:00+00', '2026-02-26 10:00:00+00'),
(28, 14, 18, 'COMPLETED', 100, '2026-02-13 09:15:00+00', '2026-02-27 18:00:00+00', true, '2026-02-13 09:15:00+00', '2026-02-27 18:00:00+00'),
(29, 15, 25, 'IN_PROGRESS', 35, '2026-02-16 11:00:00+00', NULL, false, '2026-02-16 11:00:00+00', '2026-02-28 09:30:00+00'),
(30, 16, 1, 'COMPLETED', 100, '2026-02-18 10:00:00+00', '2026-02-26 15:00:00+00', true, '2026-02-18 10:00:00+00', '2026-02-26 15:00:00+00'),
(31, 17, 9, 'COMPLETED', 100, '2026-02-20 09:00:00+00', '2026-02-25 12:00:00+00', true, '2026-02-20 09:00:00+00', '2026-02-25 12:00:00+00'),
(32, 18, 9, 'COMPLETED', 100, '2026-02-22 14:00:00+00', '2026-02-27 16:00:00+00', true, '2026-02-22 14:00:00+00', '2026-02-27 16:00:00+00'),
(33, 19, 10, 'IN_PROGRESS', 20, '2026-02-25 11:00:00+00', NULL, false, '2026-02-25 11:00:00+00', '2026-02-28 10:00:00+00'),
(34, 20, 23, 'IN_PROGRESS', 55, '2026-02-28 10:00:00+00', NULL, false, '2026-02-28 10:00:00+00', '2026-02-28 17:00:00+00'),
(35, 1, 3, 'COMPLETED', 100, '2026-02-01 09:00:00+00', '2026-02-15 16:00:00+00', true, '2026-02-01 09:00:00+00', '2026-02-15 16:00:00+00'),
(36, 4, 5, 'COMPLETED', 100, '2026-01-20 10:00:00+00', '2026-01-28 15:30:00+00', true, '2026-01-20 10:00:00+00', '2026-01-28 15:30:00+00'),
(37, 6, 22, 'NOT_STARTED', 0, '2026-02-24 10:00:00+00', NULL, false, '2026-02-24 10:00:00+00', '2026-02-24 10:00:00+00'),
(38, 8, 21, 'IN_PROGRESS', 90, '2026-02-01 08:30:00+00', NULL, false, '2026-02-01 08:30:00+00', '2026-02-28 18:00:00+00'),
(39, 10, 8, 'NOT_STARTED', 0, '2026-02-26 09:00:00+00', NULL, false, '2026-02-26 09:00:00+00', '2026-02-26 09:00:00+00'),
(40, 12, 13, 'IN_PROGRESS', 40, '2026-02-25 10:00:00+00', NULL, false, '2026-02-25 10:00:00+00', '2026-02-28 12:00:00+00');

-- ----------------------------------------------------------------------------
-- 10. CERTIFICATES TABLE (Certificates strictly for completed enrollments)
-- ----------------------------------------------------------------------------
INSERT INTO certificates (id, user_id, course_id, certificate_number, issued_at, certificate_url) VALUES
(1, 1, 1, 'CERT-2026-JAVA-001', '2026-01-20 17:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-JAVA-001.pdf'),
(2, 1, 2, 'CERT-2026-SPRING-002', '2026-02-05 16:30:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-SPRING-002.pdf'),
(3, 2, 11, 'CERT-2026-PROMPT-003', '2026-01-18 15:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-PROMPT-003.pdf'),
(4, 2, 12, 'CERT-2026-GENAI-004', '2026-02-02 18:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-GENAI-004.pdf'),
(5, 3, 4, 'CERT-2026-REACT-005', '2026-02-01 17:45:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-REACT-005.pdf'),
(6, 4, 17, 'CERT-2026-AZURE-006', '2026-01-29 16:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-AZURE-006.pdf'),
(7, 5, 5, 'CERT-2026-DOCKER-007', '2026-01-30 17:30:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-DOCKER-007.pdf'),
(8, 6, 25, 'CERT-2026-SEC-008', '2026-02-10 16:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-SEC-008.pdf'),
(9, 7, 9, 'CERT-2026-GIT-009', '2026-02-03 14:30:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-GIT-009.pdf'),
(10, 8, 16, 'CERT-2026-ARCH-010', '2026-01-31 18:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-ARCH-010.pdf'),
(11, 9, 3, 'CERT-2026-FASTAPI-011', '2026-02-18 17:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-FASTAPI-011.pdf'),
(12, 11, 14, 'CERT-2026-GRAPH-012', '2026-02-22 16:30:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-GRAPH-012.pdf'),
(13, 12, 12, 'CERT-2026-GENAI-013', '2026-02-24 17:15:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-GENAI-013.pdf'),
(14, 14, 18, 'CERT-2026-AWS-014', '2026-02-27 18:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-AWS-014.pdf'),
(15, 16, 1, 'CERT-2026-JAVA-015', '2026-02-26 15:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-JAVA-015.pdf'),
(16, 17, 9, 'CERT-2026-GIT-016', '2026-02-25 12:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-GIT-016.pdf'),
(17, 18, 9, 'CERT-2026-GIT-017', '2026-02-27 16:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-GIT-017.pdf'),
(18, 1, 3, 'CERT-2026-FASTAPI-018', '2026-02-15 16:00:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-FASTAPI-018.pdf'),
(19, 4, 5, 'CERT-2026-DOCKER-019', '2026-01-28 15:30:00+00', 'https://certificates.enterprise-lms.com/CERT-2026-DOCKER-019.pdf');

-- ----------------------------------------------------------------------------
-- 11. NOTIFICATIONS TABLE (25 Enterprise Notifications)
-- ----------------------------------------------------------------------------
INSERT INTO notifications (id, user_id, title, message, notification_type, is_read, created_at) VALUES
(1, 1, 'Certificate Issued!', 'Congratulations Shaik Sohel! You earned a certificate in Java Fundamentals.', 'CERTIFICATE', true, '2026-01-20 17:05:00+00'),
(2, 1, 'Certificate Issued!', 'Congratulations Shaik Sohel! You earned a certificate in Advanced Spring Boot.', 'CERTIFICATE', true, '2026-02-05 16:35:00+00'),
(3, 1, 'AI Recommendation Ready', 'Based on your backend expertise, check out PostgreSQL Performance Optimization.', 'RECOMMENDATION', false, '2026-02-07 09:00:00+00'),
(4, 2, 'New Course Assigned', 'Manager Vikram Reddy assigned you "LangChain Development Framework".', 'REMINDER', true, '2026-02-03 10:05:00+00'),
(5, 2, 'Certificate Issued!', 'Congratulations Priya Sharma! You earned a certificate in Generative AI Fundamentals.', 'CERTIFICATE', true, '2026-02-02 18:05:00+00'),
(6, 3, 'Certificate Issued!', 'Congratulations Rahul Verma! You earned a certificate in React Enterprise Architecture.', 'CERTIFICATE', true, '2026-02-01 17:50:00+00'),
(7, 3, 'Course Reminder', 'Keep up your 5-day streak! You are 75% through FastAPI Masterclass.', 'REMINDER', false, '2026-02-28 09:00:00+00'),
(8, 4, 'Certificate Issued!', 'Congratulations Ananya Rao! You earned a certificate in Azure Cloud Fundamentals.', 'CERTIFICATE', true, '2026-01-29 16:05:00+00'),
(9, 4, 'Learning Path Assigned', 'You were enrolled in the Cloud Solutions Architect Path.', 'INFO', true, '2026-01-30 09:05:00+00'),
(10, 5, 'Certificate Issued!', 'Congratulations Arjun Patel! You earned a certificate in Docker Essentials.', 'CERTIFICATE', true, '2026-01-30 17:35:00+00'),
(11, 5, 'Course Milestone', 'You completed 85% of Kubernetes Basics & Deployment.', 'INFO', false, '2026-02-28 15:05:00+00'),
(12, 6, 'Security Alert & Course Assigned', 'You were assigned "Enterprise Application Security & OAuth2".', 'REMINDER', true, '2026-01-23 10:05:00+00'),
(13, 7, 'Certificate Issued!', 'Congratulations Sneha Gupta! You earned a certificate in Git & GitHub Workflows.', 'CERTIFICATE', true, '2026-02-03 14:35:00+00'),
(14, 8, 'Manager Dashboard Update', '3 new team members completed their assigned core compliance paths.', 'INFO', false, '2026-02-28 17:00:00+00'),
(15, 9, 'Certificate Issued!', 'Congratulations Rohan Das! You earned a certificate in FastAPI Masterclass.', 'CERTIFICATE', true, '2026-02-18 17:05:00+00'),
(16, 10, 'Course Recommendation', 'Boost your frontend capabilities with React Enterprise Architecture.', 'RECOMMENDATION', false, '2026-02-10 10:05:00+00'),
(17, 11, 'Certificate Issued!', 'Congratulations Karan Mehta! You earned a certificate in LangGraph Multi-Agent Workflows.', 'CERTIFICATE', true, '2026-02-22 16:35:00+00'),
(18, 12, 'Certificate Issued!', 'Congratulations Ishita Roy! You earned a certificate in Generative AI Fundamentals.', 'CERTIFICATE', true, '2026-02-24 17:20:00+00'),
(19, 13, 'Deadline Reminder', 'Complete Kubernetes Basics & Deployment before the end of Q1.', 'REMINDER', false, '2026-02-25 09:00:00+00'),
(20, 14, 'Certificate Issued!', 'Congratulations Meera Nair! You earned a certificate in AWS Architecting & Solutions.', 'CERTIFICATE', true, '2026-02-27 18:05:00+00'),
(21, 15, 'Security Workshop Invited', 'You are invited to the live Enterprise Security & OAuth2 Q&A session.', 'INFO', false, '2026-02-26 11:00:00+00'),
(22, 16, 'Certificate Issued!', 'Congratulations Nikhil Joshi! You earned a certificate in Java Fundamentals.', 'CERTIFICATE', true, '2026-02-26 15:05:00+00'),
(23, 17, 'Product Learning Path', 'Track your engineering workflows with Git & GitHub Workflows.', 'INFO', true, '2026-02-20 09:05:00+00'),
(24, 18, 'QA Automation Goal', 'Complete REST API Design & Security to earn your API Automation badge.', 'REMINDER', false, '2026-02-27 10:00:00+00'),
(25, 20, 'AI Innovation Stream', 'New course available: Autonomous AI Agents Engineering.', 'RECOMMENDATION', false, '2026-02-28 10:05:00+00');

-- ----------------------------------------------------------------------------
-- 12. AI RECOMMENDATIONS TABLE (Personalized recommendations)
-- ----------------------------------------------------------------------------
INSERT INTO ai_recommendations (id, user_id, course_id, recommendation_reason, generated_at) VALUES
(1, 1, 7, 'Because you completed Java Fundamentals and Spring Boot, optimizing PostgreSQL queries will increase your backend service performance by 40%.', '2026-02-07 09:00:00+00'),
(2, 2, 13, 'Because you completed Generative AI Fundamentals, mastering LangChain will allow you to build production RAG applications.', '2026-02-03 10:00:00+00'),
(3, 2, 14, 'Based on your ML Engineer role, LangGraph multi-agent workflows match your team project requirements.', '2026-02-15 14:00:00+00'),
(4, 3, 8, 'Because you master React frontend architecture, learning REST API security will round out your Full Stack skill profile.', '2026-02-05 11:00:00+00'),
(5, 4, 18, 'Because you completed Azure Cloud Fundamentals, adding AWS Architecting will make you multi-cloud certified.', '2026-01-30 09:00:00+00'),
(6, 5, 22, 'As a DevOps Lead, automating CI/CD Pipelines with GitHub Actions complements your Kubernetes cluster management skills.', '2026-02-15 13:00:00+00'),
(7, 6, 8, 'Because you completed Enterprise Security & OAuth2, REST API Design & Security will help you enforce API perimeter defense.', '2026-02-11 11:30:00+00'),
(8, 7, 3, 'Because you completed Git Workflows, understanding FastAPI will enable automated API integration testing for QA.', '2026-02-04 10:00:00+00'),
(9, 8, 21, 'As Engineering Manager, Microservices Architecture Patterns will help you lead system design reviews.', '2026-02-01 08:30:00+00'),
(10, 9, 20, 'Because you completed FastAPI Masterclass, Python for High-Performance Backend will help you optimize async event loops.', '2026-02-19 10:00:00+00'),
(11, 10, 4, 'Based on your Frontend Engineer role, React Enterprise Architecture is recommended to master Redux Toolkit Query.', '2026-02-10 10:00:00+00'),
(12, 11, 15, 'Because you completed LangGraph, learning CrewAI will expand your multi-agent architecture repertoire.', '2026-02-23 09:30:00+00'),
(13, 12, 24, 'Based on your Data Science background, Vector Databases & Hybrid RAG Search will help you design high-precision document search.', '2026-02-25 10:00:00+00'),
(14, 13, 6, 'Because you possess Docker skills, Kubernetes Basics will elevate your infrastructure container management.', '2026-02-11 13:00:00+00'),
(15, 14, 16, 'Based on your Cloud Engineer role, Enterprise System Design will strengthen your distributed systems blueprinting.', '2026-02-27 18:00:00+00'),
(16, 15, 25, 'As a Security Architect, Enterprise Application Security & OAuth2 is essential for identity governance compliance.', '2026-02-16 11:00:00+00'),
(17, 16, 2, 'Because you completed Java Fundamentals, Advanced Spring Boot is your recommended next step.', '2026-02-26 15:00:00+00'),
(18, 17, 9, 'As Product Manager, mastering Git Workflows will help you track dev branch delivery milestones.', '2026-02-20 09:00:00+00'),
(19, 18, 8, 'Because you completed Git Workflows, REST API Design will assist you in authoring Postman & PyTest API test suites.', '2026-02-27 10:00:00+00'),
(20, 20, 23, 'Because you are an AI Research Engineer, Autonomous AI Agents Engineering is highly recommended for your active roadmap.', '2026-02-28 10:00:00+00');

-- ----------------------------------------------------------------------------
-- 13. POSTGRESQL SEQUENCE RESETS
-- Set auto-increment sequences to MAX(id) for seamless subsequent inserts
-- ----------------------------------------------------------------------------
SELECT setval(pg_get_serial_sequence('users', 'id'), COALESCE(MAX(id), 1)) FROM users;
SELECT setval(pg_get_serial_sequence('skills', 'id'), COALESCE(MAX(id), 1)) FROM skills;
SELECT setval(pg_get_serial_sequence('learning_paths', 'id'), COALESCE(MAX(id), 1)) FROM learning_paths;
SELECT setval(pg_get_serial_sequence('courses', 'id'), COALESCE(MAX(id), 1)) FROM courses;
SELECT setval(pg_get_serial_sequence('lessons', 'id'), COALESCE(MAX(id), 1)) FROM lessons;
SELECT setval(pg_get_serial_sequence('employee_skills', 'id'), COALESCE(MAX(id), 1)) FROM employee_skills;
SELECT setval(pg_get_serial_sequence('learning_path_courses', 'id'), COALESCE(MAX(id), 1)) FROM learning_path_courses;
SELECT setval(pg_get_serial_sequence('enrollments', 'id'), COALESCE(MAX(id), 1)) FROM enrollments;
SELECT setval(pg_get_serial_sequence('certificates', 'id'), COALESCE(MAX(id), 1)) FROM certificates;
SELECT setval(pg_get_serial_sequence('notifications', 'id'), COALESCE(MAX(id), 1)) FROM notifications;
SELECT setval(pg_get_serial_sequence('ai_recommendations', 'id'), COALESCE(MAX(id), 1)) FROM ai_recommendations;

-- ============================================================================
-- End of Production Seed Script
-- ============================================================================
