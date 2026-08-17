# AI Engineer Coding Challenge Submission

An intelligent, context-aware information extraction agent built with LangChain and Pydantic to parse, structure, and filter unstructured customer order data.

## Architecture & Design Choices
- **Data Isolation (Chunking):** Process raw orders iteratively to target arbitrary context-window overflow and enforce safety against large payload memory limits.
- **Pydantic Pipeline Enforcements:** Sanitizes LLM artifacts.
- **Structural Resilience:** Implements an automated self-correcting retry loop inside the `OrderProcessor` to overcome potential LLM anomalies.

## Getting Started

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### 2. Configure Credentials
Configure OpenRouter settings in src/constrain_llm/config/settings.py, e.g.,
```
OPENROUTER_API_KEY=your_key_here
LLM_PROVIDER = "openrouter"
LLM_MODEL = "openai/gpt-oss-120b:exacto"
```
***Note:*** set OpenRouter API key set as Linux shell variable: export OPENAI_API_KEY=<your-key>

### 3. Run the Application
Start the mock API in one terminal:
```bash
python dummy_customer_api.py
```
Run the agent pipeline in another terminal:
```bash
python main.py
```


Program Diagram:



                    ========================================
                    main(): NATURAL LANGUAGE QUERY HANDLING   
                    ========================================

                       +----------------------------------+
                       |              main()              |
                       |  Orchestrates the whole pipeline |
                       +----------------------------------+
                                        |
      1. Fetch Data                     | 2. Parse Raw Text
            v                           v
+-----------------------+    +----------------------------------+

|      CustomerAPI      |    |          OrderProcessor          |
|  Fetches raw order    |    |  Iterates through raw entries    |
|  strings from source  |    +----------------------------------+
+-----------------------+                     |

            |                                 | Calls LLM via OpenRouter
            | (RawOrdersResponse)             v
            |                        +----------------------------------+
            |                        |     LLM                          |
            |                        | Extracts raw values to fit schema|
            |                        +----------------------------------+
            |                                 |
            |                                 | Returns structured text
            |                                 v
            |                        +----------------------------------+
            |                        |          Pydantic Order +        |
            |                        |       Structural Validation      |
            |                        +----------------------------------+
            |                                 |
            |                                 | Validated Order Object
            v                                 v
+-----------------------------------------------------------------------+
|                             ParsedOrders                              |
|             (Collection of Validated Orders & Issues)                 |
+-----------------------------------------------------------------------+
                                    |
                                    | 4. Filter compiled dataset
                                    v
+-----------------------------------------------------------------------+
|                             OrderFilter                               |
|       Compares Orders against parameters using list comprehension     |
|   Checks: order.state == query.state AND min_total <= order.total ... |
+-----------------------------------------------------------------------+
                                    |
                                    | 5. Output filtered results
                                    v
                         +----------------------+
                         |    Display Results   |
                         |  Prints matching     |
                         |  orders to terminal  |
                         +----------------------+



            ==================================================
            SEPARATE PIPELINE: NATURAL LANGUAGE QUERY HANDLING
            ==================================================
                                    |
                                    |
       3| Convert Request           |
               v                    |
+------------------------------+    |
|        QueryProcessor        |    |
|  Takes natural-language text |    |
+------------------------------+    |
               |                    |
               | Calls LLM          |
               v                    |
+------------------------------+    |
|  LLM                         |    |
| Extracts query criteria      |    |
+------------------------------+    |
               |                    |
               | Returns JSON       |
               v                    |
+------------------------------+    |
|      Pydantic OrderQuery     |    |
|  - Keeps state clean         |--- + (Feeds into OrderFilter)
|  - Maps floats for alignment |
+------------------------------+