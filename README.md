        - event handling in langGraph

                  WORKER
                    │
                    │ writer(...)
                    ▼
             ┌──────────────┐
             │    EVENT     │
             │              │
             │ "processing  │
             │  started"    │
             └───────┬──────┘
                     │
                     ▼
              graph.stream()
                     │
                     ▼
              handle_event()
                     │
                     ▼
                  print()
