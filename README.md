
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
                                    .
                                    .
       3. Convert Request           .
               v                    .
+------------------------------+    .
|        QueryProcessor        |    .
|  Takes natural-language text |    .
+------------------------------+    .
               |                    .
               | Calls LLM          .
               v                    .
+------------------------------+    .
|  LLM                         |    .
| Extracts query criteria      |    .
+------------------------------+    .
               |                    .
               | Returns JSON       .
               v                    .
+------------------------------+    .
|      Pydantic OrderQuery     |    .
|  - Keeps state clean         |....+ (Feeds into OrderFilter)
|  - Maps floats for alignment |
+------------------------------+