## Scaling a Company Similarity API

### Setting Up an API Endpoint

Right now, we have a working tool that takes a company description and finds the top _n_ most similar companies from a database, but it’s not set up for real-world usage at scale. One of the first things we need is a proper **API endpoint** capable of receiving requests, processing them, and returning results.

We can use **FastAPI** or **Flask** for the handling server but we should run it under a production-grade server like **Uvicorn** or **Gunicorn** so it can handle multiple incoming requests in parallel. If a serverless approach fits better, **AWS Lambda** can host the API, but we must keep an eye on memory limits and execution time, especially if we’re dealing with a large dataset or heavy processing.

### Scaling Data Processing

The current approach with **Pandas** works well for smaller projects and prototypes, but it doesn’t always scale to millions of rows. Switching to **PySpark** will let us distribute the workload across multiple nodes, helping us avoid performance bottlenecks.

### Generating Company Descriptions

Generating company descriptions can be the most expensive step, particularly if we rely on **GPT-based models**. The general workflow involves fetching each company’s website, extracting html text with **BeautifulSoup**, applying **TF-IDF**, company name and **sic** which are sent to **GPT-4o-mini** to produce a concise description (for 5000 companies the cost was ~1 dollar).

We can run this job on a weekly or monthly basis. **AWS EventBridge, cron jobs, or AWS Batch** are all ways to schedule these large-scale operations in a manageable way.

### Storing and Querying Embeddings

Once the descriptions are generated, we create **embeddings** and store them in a database that supports **vector queries**. **PostgreSQL with the pgvector extension** is a common choice, but specialized vector databases like **Pinecone or Milvus** can also work if we need faster searching and can handle the extra operational overhead.

In a typical scenario, once the API receives a description from a user, it either creates or retrieves its embedding, then queries the database for the most similar vectors. The query returns the top matches, which the API sends back as **JSON**.

### Ensuring Reliability

We’ll need proper **testing and continuous integration** to maintain reliability. Unit tests can validate smaller pieces of functionality—like confirming that **website scraping** or **text embeddings** are working as expected. Integration tests can confirm that the entire process, from receiving a request to returning results, is functioning correctly.

We should also consider **load testing** to make sure our setup can handle enough concurrent requests for production needs. When we combine automated testing with a **CI/CD pipeline**, every time new code is committed, the pipeline can run tests, build **Docker images**, and deploy them to production automatically (or with a manual approval step). **AWS CodePipeline, GitHub Actions, or GitLab CI** can handle this part of the workflow.

### Monitoring and Performance Tracking

Because embeddings don’t change much once they’re generated—unless we scrape new text or switch to a new model—we don’t have to monitor them for drift on a daily basis. However, we do want to keep an eye on **system performance** through **logs and metrics**, making sure that requests are responded to in a reasonable time and that we aren’t hitting API rate limits.

**AWS CloudWatch** or a similar monitoring tool can track **memory usage, CPU load, and error rates**. If we ever see unusual spikes or slowdowns, we can review the logs and figure out whether we’re calling GPT too often, if the **Spark job** is overloading the system, or if the **database** can’t handle the current query load.

### Deployment Strategy

By **containerizing** everything with **Docker**, we can deploy the service on **AWS ECS or EKS** if we prefer a managed container orchestration environment. If we’re using **Lambda**, we’ll package the code differently, but the logic stays the same.

The scheduling tool (like a **cron job or AWS EventBridge**) can periodically check for new companies in our database, scrape their websites, generate summaries, produce embeddings, and store them so they’re ready when a user makes a similarity query.

### Conclusion

Ultimately, this approach gives us a **consistent, tested, and scalable system**. It’s built to refresh data as needed, handle potentially large numbers of parallel requests, and keep costs in check by batching **GPT-based description generation**. Once it’s up and running, we’ll have a **smooth workflow** that can evolve as our data grows or as we refine the **model for generating descriptions**.
