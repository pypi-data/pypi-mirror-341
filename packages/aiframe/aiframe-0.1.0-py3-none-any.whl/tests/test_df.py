import pandas as pd

# Dataset to test
test_df = pd.DataFrame(
    {
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["New York", "Los Angeles", "Chicago"],
        "description": [
            "Alice is a software engineer.",
            "Bob is a data scientist.",
            "Charlie is a product manager.",
        ],
    }
)

# Add 10 more rows
additional_rows = pd.DataFrame(
    [
        {
            "name": "Diana",
            "age": 28,
            "city": "San Francisco",
            "description": "Diana is a UX designer.",
        },
        {
            "name": "Ethan",
            "age": 32,
            "city": "Seattle",
            "description": "Ethan is a DevOps engineer.",
        },
        {
            "name": "Fiona",
            "age": 27,
            "city": "Austin",
            "description": "Fiona is a QA specialist.",
        },
        {
            "name": "George",
            "age": 40,
            "city": "Denver",
            "description": "George is an IT consultant.",
        },
        {
            "name": "Hannah",
            "age": 29,
            "city": "Boston",
            "description": "Hannah is a backend developer.",
        },
        {
            "name": "Ian",
            "age": 33,
            "city": "Portland",
            "description": "Ian is a machine learning engineer.",
        },
        {
            "name": "Julia",
            "age": 26,
            "city": "Atlanta",
            "description": "Julia is a frontend developer.",
        },
        {
            "name": "Kevin",
            "age": 31,
            "city": "Miami",
            "description": "Kevin is a cybersecurity analyst.",
        },
        {
            "name": "Laura",
            "age": 34,
            "city": "Philadelphia",
            "description": "Laura is a cloud architect.",
        },
        {
            "name": "Mark",
            "age": 36,
            "city": "Phoenix",
            "description": "Mark is a technical writer.",
        },
    ]
)

# Concatenate
test_df = pd.concat([test_df, additional_rows], ignore_index=True)
